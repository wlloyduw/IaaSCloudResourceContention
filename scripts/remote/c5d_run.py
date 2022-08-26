#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# crontab command interface design
#c5d_run.py [benchmark][setId] [vmId] [runs]

import json
import sys
import os
from collections import OrderedDict
import csv
import re


def main(args):
    config = loadConfigure("/home/ubuntu/SCRIPT/scripts/remote/config.json")
    benchmark = args[0]
    setId = args[1]
    vmId = args[2]
    runs = int(args[3])
    cmd = config["benchmarks"][benchmark]
    entry = Entry(config["datadir"], benchmark, setId, vmId, cmd)

    for i in range(runs):
        rawperf = os.popen(cmd).read()
        perf = {}
        if benchmark == "sysbench":
            perf = Parser.sysbenchParse(rawperf)
        elif benchmark == "pgbench":
            perf = Parser.pgbenchParse(rawperf)
        elif benchmark == "sysbenchio":
            perf = Parser.sysbenchioParse(rawperf)
        else:
            print("benchmark didn't match")

        entry.row.update(perf)
        print(entry.row)
        entry.appendToFile()
    pass


def loadConfigure(filepath):
    with open(filepath, 'r') as fin:
        config = json.loads(fin.read())
        return config


class Entry:
    def __init__(self, path, benchmark, setId, vmId, cmd):
        self.csvfile = path + benchmark + '.csv'
        # table schema
        self.row = OrderedDict(
            [("setId", None), ("vmId", None), ("cmd", None)])
        # mkdir, create file, write header
        if not os.path.isfile(self.csvfile):
            needHeader = True
            print("creating header...")
            os.system("mkdir %s" % path)

        with open(self.csvfile, 'a') as fout:
            writer = csv.DictWriter(fout, fieldnames=self.row)
            try:
                if needHeader:
                    writer.writeheader()
            except NameError:
                print("don't need a header")

        self.row["vmId"] = vmId
        self.row["setId"] = setId
        self.row["cmd"] = cmd

    def appendToFile(self):
        with open(self.csvfile, 'a') as fout:
            writer = csv.DictWriter(fout, fieldnames=self.row)
            writer.writerow(self.row)


class Parser:
    result = {}

    @classmethod
    def sysbenchParse(self, rawperf):
        try:
            for line in rawperf.split('\n'):
                if line.find('total time:') != -1:
                    totalTime = re.search(r'total time:\s*(.*)', line).group(1)
                    Parser.result['total-time(s)'] = totalTime
        except (AttributeError, IndexError):
            os.popen("mkdir RE_ERROR!!!")
        return Parser.result

    @classmethod
    def pgbenchParse(self, rawperf):
        try:
            for line in rawperf.split('\n'):
                if line.find('excluding connections establishing') != -1:
                    transactions = re.search(r'(\d*\.\d*)', line).group(1)
                    Parser.result['transactions(per s)'] = transactions
        except (AttributeError, IndexError):
            os.popen("mkdir RE_ERROR!!!")
        return Parser.result

    @classmethod
    def sysbenchioParse(self, rawperf):
        try:
            for line in rawperf.split('\n'):
                if line.find('Total transferred') != -1:
                    computationTime = re.search(
                        r'(\d*\.\d*)Mb/sec', line).group(1)
                    Parser.result['transferred(Mb/sec)'] = computationTime
        except (AttributeError, IndexError):
            os.popen("mkdir RE_ERROR!!!")
        return Parser.result


if __name__ == "__main__":
    main(sys.argv[1:])
