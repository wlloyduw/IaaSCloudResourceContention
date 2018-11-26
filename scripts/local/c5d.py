#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import json
from shutil import copyfile
from dateutil.relativedelta import relativedelta as delta
from datetime import datetime
import os
import sys
### PATHS ###
PEM_PATH = "~/.ssh/as0.pem"
### CUSTOM CONFIGURATIONs ###
LAUNCH_DELAY = 3  # after LAUNCH_DELAY then start experiment on slave nodes, in minutes
CYCLES_PER_SET = 10  # k cycles per set.
REVERSE_FLAG = True  # False : do experiment incrementally; TRUE: decremental
EXPERIMENT_ID = int(datetime.timestamp(datetime.now()))
#
TIME = []
#
# instances should be taged as   key:iperfRole value=client
# return a list of instance' IP


def getIpPool(file):
    command = r'aws ec2 describe-instances --filters "Name=tag:iperfRole,Values=client" "Name=instance-state-name,Values=running"'
    command += r' | grep PublicIpAddress | cut -d":" -f 2 | cut -d"," -f 1 | cut -d"\"" -f 2'

    response = os.popen(command).read().strip().split('\n')
    with open(file, 'w') as f:
        for ip in response:
            f.write('ubuntu@' + ip + '\n')
    print("ClientList:", response)
    return response

## build a list of command wrote to clients' crontab file that contains raw command needed pass to iperf_slave.py  ##


def cronBuilder(starttime, clientSeq, total):
    # assume clientSeq 0 based
    def cronHelper(time, benchmark):
        # CHANGE crontab lines here, if needed #c5d_run.py [benchmark] [setId] [vmId] [runs]
        crontabCmd = "%s %s %s * * ubuntu python3  ~/SCRIPT/scripts/remote/c5d_run.py %s %s %s %s\n" % (
            str(time.minute), str(time.hour), str(time.day),
            benchmark, setId, vmId,  CYCLES_PER_SET)
        return crontabCmd

    launch_time = starttime + delta(minutes=int(LAUNCH_DELAY))
    cmdList = []
    setsOffset = 0
    with open("/home/ubuntu/SCRIPT/scripts/remote/config.json", 'r') as fin:
        config = json.loads(fin.read())
    for i in range(total):  # each sets
        setId, vmId = i + 1, clientSeq + 1
        benchmarkOffset = 0
        for benchmark in config["types"]:  # each benchmark
            if REVERSE_FLAG is False and clientSeq <= i:
                cmdList.append(cronHelper(
                    launch_time + delta(minutes=(setsOffset + benchmarkOffset)), benchmark))
            if REVERSE_FLAG is True and clientSeq >= i:
                cmdList.append(cronHelper(
                    launch_time + delta(minutes=(setsOffset + benchmarkOffset)), benchmark))
            benchmarkOffset += (int(config["timecost"]
                                    [benchmark])*CYCLES_PER_SET / 60) + 1
        setsOffset += benchmarkOffset
    TIME.append([launch_time, datetime.now() +
                 delta(minutes=setsOffset)])
    return cmdList


# set up inastance through pssh
def configureInstances(iplist):
    print("configurIperfClient()")
    starttime = datetime.utcnow()
    # for each Instance
    seq = 0
    for instance in iplist:
        cmdList = cronBuilder(starttime, seq, len(iplist))
        seq += 1
        # new a copy of crontab from back-up
        copyfile("crontab.bak", "crontab")
        with open("crontab", "a") as f:
            f.write("\n".join(cmdList))
        # copy crontab to slave nodes
        print("Sending crontab to IP:%s" % (instance))
        print(os.popen("scp -i %s crontab %s:~/" %
                       (PEM_PATH, "ubuntu@" + instance)).read())

    # for all clients, simultaneously
    # CHANGE initiation method here, if neeeded
    cmd = "'sudo cp ~/crontab /etc/crontab && sudo chown root.root /etc/crontab && sudo service cron reload'"
    print(psshExcute("hostfile_pssh", cmd))  # preparations for cron
    cmd = ''' 'eval "$(ssh-agent)" && ssh-add -k ~/.ssh/git_capstone && rm -rf Capstone SCRIPT &&
        git clone git@github.com:khaosminded/Capstone.git && mv Capstone SCRIPT' '''
    print(psshExcute("hostfile_pssh", cmd)
          )  # git clone, slave nodes needed to have git-hub private key
    return seq


def psshExcute(addrfile, command):
    pssh = "pssh -i -h %s -x '-i %s' %s" % (addrfile, PEM_PATH, command)
    return "###PSSH CALL:%s\n" % (command) + os.popen(pssh).read()


def main(argv):
    ipfile = 'hostfile_pssh'
    ipPool = getIpPool(ipfile)
    setsTotal = configureInstances(ipPool)
    print("initiating pgbench")
    psshExcute(
        ipfile, "sudo bash /home/ubuntu/SCRIPT/scripts/remote/init_pg_on_localdisk.bash &")

    for period in TIME:
        print("\n" + period[0].ctime()+"=>"+period[1].ctime())
    print("\nExperiment will end at :" + TIME[-1][1].ctime())
    print("\ntotal sets: %s" % setsTotal)


if __name__ == "__main__":
    main(sys.argv[1:])
