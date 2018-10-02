#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import datetime
# Assume iperf server is taged as <Key:iperfRole,Value:server>
# Assume iperf client is taged as <Key:iperfRole,Value:client>

commandList = list()
C2Smap = dict()


def getClientPool():
    command = r'aws ec2 describe-instances --filters "Name=tag:iperfRole,Values=client" "Name=instance-state-name,Values=running"'
    command += r' | grep PublicIpAddress | cut -d":" -f 2 | cut -d"," -f 1 | cut -d"\"" -f 2'

    response = os.popen(command).read().strip().split('\n')
    with open('iperfClients', 'w') as f:
        for ip in response:
            f.write('ubuntu@' + ip + '\n')
    print("ClientList:", response)
    return response


def getServerPool():
    command = r'aws ec2 describe-instances --filters "Name=tag:iperfRole,Values=server" "Name=instance-state-name,Values=running"'
    command += r' | grep PublicIpAddress | cut -d":" -f 2 | cut -d"," -f 1 | cut -d"\"" -f 2'

    response = os.popen(command).read().strip().split('\n')
    with open('iperfServers', 'w') as f:
        for ip in response:
            f.write('ubuntu@' + ip + '\n')
    print("ServerList:", response)
    return response


def createIperfPair():
    global C2Smap
    Clients = getClientPool()
    Severs = getServerPool()
    C2Smap = dict(zip(Clients, Severs))
    print("Pairs:", C2Smap)


def launchIperfServer():
    command = r'pssh -i -h iperfServers -x "-i ~/.ssh/as0.pem" iperf -s --daemon'
    response = os.popen(command).read()
    print("launchIperfServer()", response)


def configurIperfClient():
    global C2Smap
    global commandList
    for (client, server) in C2Smap.items():
        command = "pssh -i -H %s -x '-i ~/.ssh/as0.pem' iperf -c %s --dualtest --window 416k --time 15 " % (
            "ubuntu@" + client, server)
        commandList.append(command)


def main(argv):
    createIperfPair()

    launchIperfServer()
    configurIperfClient()

    for cmd in commandList:
        print("cmd = %s" % cmd)
        print(os.popen(cmd).read())


if __name__ == "__main__":
    main(sys.argv[1:])
