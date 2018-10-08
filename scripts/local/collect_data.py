#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import os
import csv
import sys
import threading


def download(hostfile):
    with open(hostfile, 'r') as f:
        hostlist = f.read()
        hostlist = hostlist.strip().split('\n')
    datadir = ':~/SCRIPT/scripts/remote/data ../../cleandata/'
    command = 'scp -i as0.pem -r '
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
    try:
        download(argv[0])
    except OSError:
        print("OSError : make sure the hostfile is correct")
    collecter('newdata.csv')


if __name__ == "__main__":
    main(sys.argv[1:])
