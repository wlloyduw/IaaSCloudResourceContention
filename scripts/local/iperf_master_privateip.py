#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta as delta
from shutil import copyfile
# EXPERIMENT DESCRIPTION
# experiment contains several sets of running
# each set do CYCLES_PER_SET cycles iperf and involve X VMs simultaneously
# X can be incremental, or decremental
# Assume iperf server is taged as <Key:iperfRole,Value:server>
# Assume iperf client is taged as <Key:iperfRole,Value:client>

### PATHS ###
PEM_PATH = "~/.ssh/as0.pem"
### CUSTOM CONFIGURATIONs ###
LAUNCH_DELAY = 3  # after LAUNCH_DELAY then start experiment on slave nodes, in minutes
CYCLES_PER_SET = 11  # k cycles per set.
CYCLE_DURATION = 15  # limit max time per cycle if applicable, in seconds
# sleep time between each set within a experiment, in minutes
SETS_INTERVAL = (CYCLE_DURATION * CYCLES_PER_SET) / 60 + 1
REVERSE_FLAG = False  # False : do experiment incrementally; TRUE: decremental
EXPERIMENT_ID = int(datetime.timestamp(datetime.now()))


# return a list of clients' IP
def getClientPool():
    command = r'aws ec2 describe-instances --filters "Name=tag:iperfRole,Values=client" "Name=instance-state-name,Values=running"'
    command += r' | grep "                                    \"PrivateIpAddress\""  | cut -d":" -f 2 | cut -d"," -f 1 | cut -d"\"" -f 2'

    response = os.popen(command).read().strip().split('\n')
    with open('iperfClients', 'w') as f:
        for ip in response:
            f.write('ubuntu@' + ip + '\n')
    print("ClientList:", response)

#    command = r'aws ec2 describe-instances --filters "Name=tag:iperfRole,Values=client" "Name=instance-state-name,Values=running"'
#    command += r' | grep PublicIpAddress | cut -d":" -f 2 | cut -d"," -f 1 | cut -d"\"" -f 2'

#    response = os.popen(command).read().strip().split('\n')
#    with open('iperfClientsPub', 'w') as f:
#        for ip in response:
#            f.write('ubuntu@' + ip + '\n')
#    print("ClientList:", response)

    return response


# return a list of servers' IP
def getServerPool():
    command = r'aws ec2 describe-instances --filters "Name=tag:iperfRole,Values=server" "Name=instance-state-name,Values=running"'
    command += r' | grep "                                    \"PrivateIpAddress\""  | cut -d":" -f 2 | cut -d"," -f 1 | cut -d"\"" -f 2'

    response = os.popen(command).read().strip().split('\n')
    with open('iperfServers', 'w') as f:
        for ip in response:
            f.write('ubuntu@' + ip + '\n')
    print("ServerList:", response)

#    command = r'aws ec2 describe-instances --filters "Name=tag:iperfRole,Values=server" "Name=instance-state-name,Values=running"'
#    command += r' | grep PublicIpAddress | cut -d":" -f 2 | cut -d"," -f 1 | cut -d"\"" -f 2'

#    response = os.popen(command).read().strip().split('\n')
#    with open('iperfServersPub', 'w') as f:
#        for ip in response:
#            f.write('ubuntu@' + ip + '\n')
#    print("ServerList:", response)

    return response


## pair up <client,server> ##
def createIperfPair():
    print("\ncreateIperfPair()")
    Clients = getClientPool()
    Severs = getServerPool()
    C2S_MAP = dict(zip(Clients, Severs))
    print("Pairs:", C2S_MAP)
    return C2S_MAP


# set up IperfServer through pssh
def launchIperfServer():
    print("\nlaunchIperfServer()")
    cmd = "iperf3 -s --daemon &"
    print(psshExcute('iperfServers', cmd))


## build a list of command wrote to clients' crontab file that contains raw command needed pass to iperf_slave.py  ##
def cronBuilder(serverAddr, clientSeq, total):
    # assume clientSeq 0 based
    def cronHelper(time):
        # CHANGE iperf-client config here, if needed
        benchmarkCmd = "iperf3 -c %s --window 416k --time %s -p 5201 -f k" % (serverAddr, CYCLE_DURATION)
        
        # CHANGE crontab lines here, if needed
        crontabCmd = "%s %s %s * * ubuntu python3  ~/SCRIPT/scripts/remote/iperf_slave.py -c %s -i %s -x '%s' -s %s -v %s\n" % (
            str(time.minute), str(time.hour), str(time.day),
            CYCLES_PER_SET, EXPERIMENT_ID, benchmarkCmd, setId, vmId)
        # TODO pass setId, vmId to slave
        return crontabCmd

    utc_time = datetime.utcnow()
    launch_time = utc_time + delta(minutes=int(LAUNCH_DELAY))
    cmdList = []

    for i in range(total):
        setId, vmId = i + 1, clientSeq + 1
        if REVERSE_FLAG is False and clientSeq <= i:
            cmdList.append(cronHelper(
                launch_time + delta(minutes=int(SETS_INTERVAL) * i)))
        if REVERSE_FLAG is True and clientSeq >= i:
            cmdList.append(cronHelper(
                launch_time + delta(minutes=int(SETS_INTERVAL) * i)))

    return cmdList


# set up IperfClient through pssh
def configurIperfClient(C2S_MAP):
    print("configurIperfClient()")
    # for each client
    seq = 0
    for clientAddr, serverAddr in C2S_MAP.items():
        cmdList = cronBuilder(serverAddr, seq, len(C2S_MAP))
        seq += 1
        # new a copy of crontab from back-up
        copyfile("crontab.bak", "crontab")
        with open("crontab", "a") as f:
            f.write("\n".join(cmdList))
        # copy crontab to slave nodes
        print("Sending crontab to IP:%s" % (clientAddr))
        print(os.popen("scp -i %s -o StrictHostKeyChecking=no crontab %s:~/" %
                       (PEM_PATH, "ubuntu@" + clientAddr)).read())

    # for all clients, simultaneously
    # CHANGE initiation method here, if neeeded
    cmd = "'sudo cp ~/crontab /etc/crontab && sudo chown root.root /etc/crontab && sudo service cron reload'"
    print(psshExcute("iperfClients", cmd))  # preparations for cron
    cmd = ''' 'eval "$(ssh-agent)" && ssh-add -k ~/.ssh/git_capstone && rm -rf IaasCloudResourceContention_stream SCRIPT && 
        git clone https://github.com/maddygithub123/IaasCloudResourceContention_stream.git && mv IaasCloudResourceContention_stream SCRIPT' '''
        # old
        #git clone git@github.com:khaosminded/IaaSCloudResourceContention.git && mv Capstone SCRIPT' '''
    print(psshExcute("iperfClients", cmd)
          )  # git clone, slave nodes needed to have git-hub private key
    return seq


def psshExcute(addrfile, command):
    pssh = "pssh -i -h %s -x '-o StrictHostKeyChecking=no -i %s' %s" % (addrfile, PEM_PATH, command)
    print (pssh)
    return "###PSSH CALL:%s\n" % (command) + os.popen(pssh).read()


def main(argv):
    C2S_MAP = createIperfPair()
    launchIperfServer()
    setsTotal = configurIperfClient(C2S_MAP)

    endTimeCounter = LAUNCH_DELAY + setsTotal * SETS_INTERVAL  # in minutes
    endTime = datetime.now() + delta(minutes=int(endTimeCounter))
    print("\nExperiment will end at :" + datetime.ctime(endTime))
    print("\nuse collect_data.py to collect data at that time")


if __name__ == "__main__":
    main(sys.argv[1:])
