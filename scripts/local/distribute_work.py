#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import os
import getopt
import sys
sys.path.append('..')
from remote import const
import datetime
from dateutil.relativedelta import relativedelta
import threading


def pssh(minute='*', hour='*', day='*', cycles='1', benchmark='pgbench'):
    # chaos, legacy, hard to modify, but excute fast
    # in some aspect, pssh=pssh_v2+cloneGitRepo
    shellscript = r'''
	set -f
	id=$(date -u +%s)
	_task='''+"'"+minute+" "+hour+" "+day+''' * * ubuntu python3  ~/SCRIPT/scripts/remote/run.py -c '''+cycles+' -t '+benchmark+''' -i '$id
	task=\\'$_task\\'
	psshcommand='set -f && eval "$(ssh-agent -s)" && ssh-add -k ~/.ssh/git_capstone && rm -rf Capstone SCRIPT && git clone https://github.com/wlloyduw/Capstone.git && mv Capstone SCRIPT && cd ~/SCRIPT && cp /etc/crontab . && echo '$task' >> crontab && sudo mv crontab /etc/crontab && sudo chown root.root /etc/crontab && sudo service cron reload'
	pssh -i -h hostfile_pssh -x "-o StrictHostKeyChecking=no -i ~/.ssh/as0.pem" $psshcommand
	'''
    respond = os.popen(shellscript).read()
    print(respond)


def pssh_v2(target_time=datetime.datetime.utcnow()+relativedelta(minutes=5), cycles='10', interval=15, benchmark='pgbench', reverseFlag=False, vmgen='c3'):
    # override pssh when doing 1to16 dedicated host experiment
    # copy each 'crontab' to its instance
    os.system('cp crontab.bak crontab')
    exp_id = os.popen('date -u +%s').read()

    def getPsshcommand(minute, hour, day, HOST_STRING):
        return '''
		set -f
		psshcommand='set -f && echo "''' + minute + " " + hour + " " + day + ''' * * ubuntu python3  ~/SCRIPT/scripts/remote/run.py -c ''' + cycles+' -t '+benchmark + ' -i ' + exp_id + '''" >> crontab'
		pssh -i -H "''' + HOST_STRING + '''" -x "-o StrictHostKeyChecking=no -i ~/.ssh/as0.pem" $psshcommand
		'''

    # copy ./crontab to every instance:~/. in hostlist
    hostlist = []
    with open('hostfile_pssh', 'r') as f:
        hostlist = f.read()
        hostlist = hostlist.strip().split('\n')
    datadir = ':~/'
    command = 'scp -i ~/.ssh/as0.pem -r ./crontab '
    threadlist = []
    for host in hostlist:
        wholecommand = command+host+datadir

        def func(i):
            def run():
                os.system(i)
            return threading.Thread(target=run, name=i)
        threadlist.append(func(wholecommand))
    for threads in threadlist:
        threads.start()
    for threads in threadlist:
        threads.join()

    # -H --host=HOST_STRING
    # No.1 instance has exactly 1 work, No.2 has 2 ... No.16 has 16 newline in crontab
    for i in range(len(hostlist)):
        HOST_STRING = ''
        if reverseFlag == True:
            for host in hostlist[:i+1]:  # reverse 1VM->16VMs
                HOST_STRING += host+' '
        else:
            for host in hostlist[i:]:
                HOST_STRING += host+' '  # positive 16VMs->1VM

        shell = getPsshcommand(str(target_time.minute), str(
            target_time.hour), str(target_time.day), HOST_STRING)
        #print(shell)
        tmp = os.popen(shell).read()
        print(tmp)
        # add interval to each line of crontab
        target_time += relativedelta(minutes=interval)

    # on each instance, mv ~/crontab to /etc/crontab & change the user to root
    shell = r'''
	psshcommand='sudo mv ~/crontab /etc/crontab && sudo chown root.root /etc/crontab && 
	sudo service cron reload'

	pssh -i -h hostfile_pssh -x "-o StrictHostKeyChecking=no -i ~/.ssh/as0.pem" $psshcommand
	'''
    respond = os.popen(shell).read()

    #if True:
    #    return
    if benchmark in ('pgbench'):
        print("make sure your instance type is: " + vmgen)
        init_data_dir = r'''
		psshcommand='sudo bash /home/ubuntu/SCRIPT/scripts/remote/init_pg_on_localdisk''' + vmgen + '''.bash'

		pssh -i -h hostfile_pssh -x "-o StrictHostKeyChecking=no -i ~/.ssh/as0.pem" $psshcommand
		'''
        respond = os.popen(init_data_dir).read()
        print(respond)


def cloneGitRepo():
    shell = r'''
	psshcommand='eval "$(ssh-agent -s)" && ssh-add -k ~/.ssh/git_capstone && rm -rf Capstone SCRIPT &&
	git clone https://github.com/wlloyduw/Capstone.git && mv Capstone SCRIPT'

	pssh -i -h hostfile_pssh -x "-o StrictHostKeyChecking=no -i ~/.ssh/as0.pem" $psshcommand
	'''
    respond = os.popen(shell).read()
    print(respond)


def getPublicIpPool():
    getPublicIp = r'aws ec2 describe-instances | grep PublicIpAddress | cut -d":" -f 2 | cut -d"," -f 1 | cut -d"\"" -f 2 '
    ipList = os.popen(getPublicIp).read()
    ipList = ipList.strip().split('\n')
    with open('hostfile_pssh', 'w') as f:
        for n in range(len(ipList)):
            ipList[n] = 'ubuntu@'+ipList[n]+'\n'
            f.write(ipList[n])


def main(argv):
    notice = '''#distribute_work.py# 
	-h : help
	-r :dedicated host reverse_mode 1to16 (16to1 by default)
	-b <choose a benchmark>
	-t/c <minute:hour:day in UTC>/<minutes count down> 
	-n <num of works> 
        -g aws ec2 vm generation, specify: c3, c5, c5d, z1d
	-d <dedicated host mode interval> (*must be last argument in list*)
	'''
    if len(argv) == 0:
        print(notice)
        sys.exit()
    try:
        opts, args = getopt.getopt(argv, "hrt:c:n:d:b:g:")
    except getopt.GetoptError:
        print(notice)
        sys.exit(2)

    # default parameter
    minute, hour, day, cycles = '0，15，30，45', '*', '*', '10'
    target_time = None
    iterative_interval = 1
    benchmark = None
    reverseFlag = False
    # CLI input handler
    for opt, arg in opts:
        if opt in ("-b"):
            benchmark = arg
        if opt in ("-r"):
            reverseFlag = True
    if benchmark not in const.supportedBenchmarks.keys():
        print('illegal benchmark\n'+notice)
        sys.exit()

    for opt, arg in opts:
        if opt == '-h':
            print('help:\n '+notice)
            sys.exit()

        elif opt in ("-t"):
            minute = arg.strip().split(':')[0]
            hour = arg.strip().split(':')[1]
            day = arg.strip().split(':')[2]
            if int(hour) not in range(24) or int(minute) not in range(60) or int(day) not in range(31):
                print('illegal time input')
                sys.exit()

        elif opt in ("-c"):
            if int(arg) not in range(360):
                print('count down need to be less than 360 min')
                sys.exit()
            utc_datetime = datetime.datetime.utcnow()
            target_time = utc_datetime+relativedelta(minutes=int(arg))
            minute, hour, day = str(target_time.minute), str(
                target_time.hour), str(target_time.day)
        elif opt in ('-n'):
            cycles = arg
        elif opt in ('-g'):
            vmgen = arg
        elif opt in ('-d'):
            # dedicated host mode
            iterative_interval = int(arg)
            getPublicIpPool()
            cloneGitRepo()
            pssh_v2(target_time, cycles, iterative_interval,
                    benchmark, reverseFlag, vmgen)
            sys.exit()

    getPublicIpPool()
    pssh(minute, hour, day, cycles, benchmark)


if __name__ == "__main__":
    main(sys.argv[1:])
