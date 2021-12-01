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
    print("in pssh")
    shellscript = r'''
	set -f
	id=$(date -u +%s)
	_task='''+"'"+minute+" "+hour+" "+day+''' * * ubuntu python3  ~/SCRIPT/scripts/remote/run.py -c '''+cycles+' -t '+benchmark+''' -i '$id
	task=\\'$_task\\'
	psshcommand='set -f && eval "$(ssh-agent -s)" && ssh-add -k ~/.ssh/git_capstone && rm -rf IaaSCloudResourceContention && git clone https://github.com/maddygithub123/IaaSCloudResourceContention.git && mv IaaSCloudResourceContention SCRIPT && cd ~/SCRIPT && cp /etc/crontab . && echo '$task' >> crontab && sudo mv crontab /etc/crontab && sudo chown root.root /etc/crontab && sudo service cron reload'
	pssh -i -h hostfile_pssh -x "-o StrictHostKeyChecking=no -i ~/.ssh/as0.pem" $psshcommand
	'''
    respond = os.popen(shellscript).read()
    print(respond)


def pssh_v2(target_time=datetime.datetime.utcnow()+relativedelta(minutes=5), cycles='10', interval=15, benchmark='pgbench', reverseFlag=False, vmgen='c3', stopFlag=False):
    print("in pssh2")
    # override pssh when doing 1to16 dedicated host experiment
    # copy each 'crontab' to its instance
    os.system('cp crontab.bak crontab')
    exp_id = os.popen('date -u +%s').read()

    def getPsshcommand(minute, hour, day, HOST_STRING, setid, stopVM):
        return '''
		set -f
		psshcommand='set -f && echo "''' + minute + " " + hour + " " + day + ''' * * ubuntu python3  ~/SCRIPT/scripts/remote/run.py -c ''' + cycles+' -t '+benchmark + stopVM + ' -i ' + str(exp_id).strip() + '-' + str(setid) + ' | logger -t testharness' + '''" >> crontab'
		pssh -i -H "''' + HOST_STRING + '''" -x "-o StrictHostKeyChecking=no -i ~/.ssh/as0.pem" $psshcommand
		'''

    def getStopcommand(minute, hour, day, HOST_STRING, setid):
        return '''
		set -f
		psshcommand='set -f && echo \"''' + minute + " " + hour + " " + day + ''' * * ubuntu aws ec2 stop-instances --instance-ids $(curl http://169.254.169.254/latest/meta-data/instance-id 2>/dev/null) | logger -t testharness\" >> crontab'
		pssh -i -H "''' + HOST_STRING + '''" -x "-o StrictHostKeyChecking=no -i ~/.ssh/as0.pem" $psshcommand
		'''
    #ORIG CMD --> psshcommand='set -f && echo "''' + minute + " " + hour + " " + day + ''' * * ubuntu python3  ~/SCRIPT/scripts/remote/run.py -c ''' + cycles+' -t '+benchmark + ' -i ' + exp_id + ' | logger -t testharness' + '''" >> crontab'
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
    skip=0
    for i in range(len(hostlist)):
        HOST_STRING = ''
        if reverseFlag == True:
            for host in hostlist[:i+1]:  # reverse 1VM->16VMs
                HOST_STRING += host+' '
        else:
            skip=1
            for host in hostlist[i:]:
                if skip == 0:
                    HOST_STRING += host+' '  # positive 16VMs->1VM
                else:
                    #schedule one VM to stop each time
                    print("stop vm:" + hostlist[i]) 
                    if stopFlag == True:
                        shell = getPsshcommand(str(target_time.minute), str(
                            target_time.hour), str(target_time.day), hostlist[i], i, " -s")
                    else:
                        shell = getPsshcommand(str(target_time.minute), str(
                            target_time.hour), str(target_time.day), hostlist[i], i, "")

                    #print(shell)
                    #print(HOST_STRING)
                    tmp = os.popen(shell).read()
                    print(tmp)
                    skip=0

        shell = getPsshcommand(str(target_time.minute), str(
            target_time.hour), str(target_time.day), HOST_STRING, i, "")
        #print(shell)
        #print(HOST_STRING)
        tmp = os.popen(shell).read()
        print(tmp)

        # Schedule instances to stop
        #if stopFlag == True:
        #    print('stop VM:' + hostlist[i])
        #    print(len(hostlist))
        #    print(i)
         
        #    shutdown_time = target_time + relativedelta(minutes=1)
        #    shell = getStopcommand(str(shutdown_time.minute), str(
        #        shutdown_time.hour), str(shutdown_time.day), hostlist[i], i)
        #    #print(shell)
        #    tmp = os.popen(shell).read()
        #    print(tmp)
        #else:
        #    print('no request to stop VMs')

        # add interval to each line of crontab
        target_time += relativedelta(minutes=interval)
        skip=skip+1

    # on each instance, mv ~/crontab to /etc/crontab & change the user to root
    shell = r'''
	psshcommand='sudo mv ~/crontab /etc/crontab && sudo chown root.root /etc/crontab && 
	sudo chmod 644 /etc/crontab && sudo service cron reload'

	pssh -i -h hostfile_pssh -x "-o StrictHostKeyChecking=no -i ~/.ssh/as0.pem" $psshcommand
	'''
    respond = os.popen(shell).read()

    #if True:
    #    return
    if benchmark in ('pgbench'):
        print("make sure your instance type is: " + vmgen)
        init_data_dir = r'''
		psshcommand='sudo bash /home/ubuntu/SCRIPT/scripts/remote/init_pg_on_localdisk''' + vmgen + '''.bash'

		pssh -i -h hostfile_pssh -t 0 -x "-o StrictHostKeyChecking=no -i ~/.ssh/as0.pem" $psshcommand
		'''
        respond = os.popen(init_data_dir).read()
        print(respond)

    # Refresh all keys
    print("refreshing credentials on instances")
    refresh_keys = r'''
 	psshcommand='~/.ssh/* /home/ubuntu/.ssh/*'

	parallel-scp -h hostfile_pssh -t 0 -x "-o StrictHostKeyChecking=no -i ~/.ssh/as0.pem" ~/.aws/credentials /home/ubuntu/.aws/credentials
	'''
    respond = os.popen(refresh_keys).read()
    #print(refresh_keys)
    print(respond)


def cloneGitRepo():
    shell = r'''
	psshcommand='eval "$(ssh-agent -s)" && ssh-add -k ~/.ssh/git_capstone && rm -rf IaaSCloudResourceContention SCRIPT &&
	git clone https://github.com/maddygithub123/IaaSCloudResourceContention.git && mv IaaSCloudResourceContention SCRIPT' 

	pssh -i -h hostfile_pssh -x "-o StrictHostKeyChecking=no -i ~/.ssh/as0.pem" $psshcommand
	'''
    respond = os.popen(shell).read()
    print(respond)

def getPublicIpPool():
    getPublicIp = r'aws ec2 describe-instances --filters "Name=instance-state-code,Values=16" | grep PublicIpAddress | cut -d":" -f 2 | cut -d"," -f 1 | cut -d"\"" -f 2 '
    ipList = os.popen(getPublicIp).read()
    ipList = ipList.strip().split('\n')
    with open('hostfile_pssh', 'w') as f:
        for n in range(len(ipList)):
            ipList[n] = 'ubuntu@'+ipList[n]+'\n'
            f.write(ipList[n])


def main(argv):
    notice = '''#distribute_work.py# 
	-h : help
        -s stop instances after test (experimental, use before everything but -b)
	-r :dedicated host reverse_mode 1to16 (16to1 by default)
	-b <choose a benchmark>
	-t/c <minute:hour:day in UTC>/<minutes count down> 
	-n <num of works> 
        -g aws ec2 vm generation, specify: c3, c5, c5d, z1d, m5d
	-d <dedicated host mode interval> (*must be last argument in list*)
	'''
    if len(argv) == 0:
        print(notice)
        sys.exit()
    try:
        opts, args = getopt.getopt(argv, "shrt:c:n:d:b:g:")
    except getopt.GetoptError:
        print(notice)
        sys.exit(2)

    # default parameter values
    minute, hour, day, cycles = '0，15，30，45', '*', '*', '10'
    target_time = None
    iterative_interval = 1
    benchmark = None
    reverseFlag = False
    stopFlag = False
    vmgen = 'c3'
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

        elif opt in ("-s"):
            print('stop VM flag has been included...')
            stopFlag = True

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
                    benchmark, reverseFlag, vmgen, stopFlag)
            sys.exit()

    getPublicIpPool()
    print('No -d flag...!')
    pssh(minute, hour, day, cycles, benchmark)


if __name__ == "__main__":
    main(sys.argv[1:])
