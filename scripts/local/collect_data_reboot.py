#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import os
import csv
import sys
import threading


def getPublicIpPool():
    getPublicIp = r'aws ec2 describe-instances --filters "Name=instance-state-code,Values=16" | grep PublicIpAddress | cut -d":" -f 2 | cut -d"," -f 1 | cut -d"\"" -f 2 '
    ipList = os.popen(getPublicIp).read()
    ipList = ipList.strip().split('\n')
    with open('hostfile_pssh', 'w') as f:
        for n in range(len(ipList)):
            ipList[n] = 'ubuntu@'+ipList[n]+'\n'
            f.write(ipList[n])


def download(hostfile):
    print(hostfile)
    with open(hostfile, 'r') as f:
        hostlist = f.read()
        hostlist = hostlist.strip().split('\n')
    datadir = ':~/SCRIPT/scripts/remote/data ../../cleandata/'
    command = 'scp -i ~/.ssh/as0.pem -o StrictHostKeyChecking=no -r '
    for host in hostlist:
        wholecommand = command+host+datadir+host
        os.system(wholecommand)


def collecter(filename):
    a = os.popen('ls ../../cleandata/./').read()
    a = a.strip().split('\n')
    needHeader = False
    if not os.path.isfile('../../cleandata/'+filename):
        needHeader = True
    f = open('../../cleandata/'+filename, 'a')
    writer = csv.writer(f)
    for eachdir in a:
        if 'ubuntu' in eachdir:
            # print(eachdir)
            path = '../../cleandata/'+eachdir+'/'
            path += os.listdir(path)[0]
            with open(path, 'r') as f:
                reader = csv.reader(f)
                if needHeader is True:
                    needHeader = False
                    writer.writerow(next(reader))
                else:
                    next(reader)
                for row in reader:
                    writer.writerow(row)
    f.close()
    os.system('rm -r ../../cleandata/ubuntu*')


def main(argv):
    getPublicIpPool()
    try:
        download(argv[0])
    except IndexError:
        print("IndexError : Make sure the hostfile is correct\n collect_data.py <hostfile>")
    collecter('newdata.csv')


if __name__ == "__main__":
    main(sys.argv[1:])
