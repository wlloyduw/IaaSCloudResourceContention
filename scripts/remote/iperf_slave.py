#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import csv
import getopt
from collections import OrderedDict

# multiple slave node will be called by their own crontab at same time
# synchronization is support with combination of crontab and NTP
# schedule running of iperf
# parse iperf output into scratch sheet

# cli input will be like: iperf_slave.py -c 3 -i 1538867113 -x 'iperf -c 35.170.79.70 --dualtest --window 416k --time 15 ' -s 1 -v 1


class IperfEntry:
    # like a static field in Java?
    DATA_PATH = '/home/ubuntu/SCRIPT/scripts/remote/data/'

    def __init__(self, experimentID, cmd):

        # table schema
        self.row = OrderedDict([('instanceID', None), ('instanceType', None), ('experimentID', None), ("interval", None),
                                ("bandwidthUpload", None), ("bandwitdhDownload", None), ("setId", None), ("vmId", None), ("cmd", None)])

        # mkdir, create file, write header
        if not os.path.isfile(IperfEntry.DATA_PATH + 'iperf.csv'):
            needHeader = True
            print("creating header...")
            os.system("mkdir %s" % IperfEntry.DATA_PATH)

        with open(IperfEntry.DATA_PATH + 'iperf.csv', 'a') as fout:
            writer = csv.DictWriter(fout, fieldnames=self.row)
            try:
                if needHeader:
                    writer.writeheader()
            except NameError:
                print("don't need a header")

        ec2metadata = os.popen('ec2metadata').read()
        self.row["instanceType"] = re.search(
            r'instance-type: (\w*\.\w*)', ec2metadata).group(1)
        self.row["instanceID"] = re.search(
            r'instance-id: (.*)\n', ec2metadata).group(1)
        self.row["experimentID"] = experimentID
        self.row["cmd"] = cmd

    def setBandwidthUpload(self, bandwidthUpload):
        self.row["bandwidthUpload"] = bandwidthUpload
        return self

    def setBandwitdhDownload(self, bandwitdhDownload):
        self.row["bandwitdhDownload"] = bandwitdhDownload
        return self

    def setSetId(self, setId):
        self.row["setId"] = setId
        return self

    def setVmId(self, vmId):
        self.row["vmId"] = vmId
        return self

    def setInterval(self, interval):
        self.row["interval"] = interval
        return self

    def appendToFile(self):
        with open(IperfEntry.DATA_PATH + 'iperf.csv', 'a') as fout:
            writer = csv.DictWriter(fout, fieldnames=self.row)
            writer.writerow(self.row)


def main(argv):
    helpstr = '# cli input will be like: -c <cycles> -i <exp id> -x <iperf config> -s <setId> -v <vmId>'

    try:
        opts, args = getopt.getopt(argv, "hc:i:x:s:v:")
    except getopt.GetoptError:
        print(helpstr)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(helpstr)
            sys.exit()
        elif opt in ("-i"):
            expId = arg
        elif opt in ("-c"):
            cycle = arg
        elif opt in ("-x"):
            cmd = arg
        elif opt in ("-s"):
            setId = arg
        elif opt in ("-v"):
            vmId = arg
    entry = IperfEntry(expId, cmd)

    for i in range(int(cycle)):
        print("running cycle %s" % (i + 1))
        result = os.popen(cmd).read()
        entry.setSetId(setId).setVmId(vmId)

        # CHANGE parsing logic here, if needed
        result = result.strip().split('\n')
        result = result[-2:]
        try:
            upload = re.search(r'-(.*?sec)\s*(.*?Bytes)\s*(.*?sec)', result[0])
            download = re.search(
                r'-(.*?sec)\s*(.*?Bytes)\s*(.*?sec)', result[1])

            entry.setBandwidthUpload(upload.group(3))\
                .setBandwitdhDownload(download.group(3))\
                .setInterval(upload.group(1))
        except (AttributeError, IndexError):
            os.popen("mkdir RE_ERROR!!!")

        entry.appendToFile()


if __name__ == "__main__":
    main(sys.argv[1:])
# TODO debug
