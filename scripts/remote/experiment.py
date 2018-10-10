#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
run.py a experiment.py  with options; 
data should be collect every run, otherwise it will be overwrite;
'''

import re
import csv
import const
import os
import time
from collections import OrderedDict


class parser(object):
    # kw need experimentID testOption
    def __init__(self, benchmark, string, **kw):
        self.string = string.split('\n')
        self.benchmark = benchmark
        self.kw = kw
        ec2metadata = os.popen('ec2metadata').read()
        self.kw['instanceType'] = re.search(
            r'instance-type: (\w*\.\w*)', ec2metadata).group(1)
        self.kw['instanceID'] = re.search(
            r'instance-id: (.*)\n', ec2metadata).group(1)

    def y_cruncher(self):
        needHeader = False
        if not os.path.isfile(const.datadir+'y_cruncher.csv'):
            needHeader = True
        os.system("mkdir "+const.datadir)
        with open(const.datadir+'y_cruncher.csv', 'a') as fout:
            row = OrderedDict([('instanceID', None), ('experimentID', None), ('instanceType', None),
                               ('memoryInfo', None), ('processorInfo',
                                                      None), ('sysTopology', None),
                               ('osVersion', None), ('testStartTime',
                                                     None), ('availableMemory', None),
                               ('isMultiThread', None), ('cpuUtilization',
                                                         None), ('multiCoreEfficiency', None),
                               ('computationTime', None), ('benchmarkTime',
                                                           None), ('wallTime', None)
                               ])
            # benchmarkTime = computationTime + I/O operation overhead
            writer = csv.DictWriter(fout, fieldnames=row)
            if needHeader:
                writer.writeheader()
            row['instanceType'] = self.kw['instanceType']
            row['instanceID'] = self.kw['instanceID']
            row['experimentID'] = self.kw['experimentID']
            row['wallTime'] = self.kw['duration']
            # row['testOption']=self.kw['testOption']

            for line in self.string:

                if line.find('Multi-core Efficiency') != -1:
                    obj = re.search(r'(\d*\.\d* %)', line)
                    row['multiCoreEfficiency'] = obj.group(1)
                if line.find('CPU Utilization') != -1:
                    obj = re.search(r'(\d*\.\d* %)', line)
                    row['cpuUtilization'] = obj.group(1)
                if line.find('Multi-Threading') != -1:
                    obj = re.search(r'\[01;36m(\w*)', line)
                    row['isMultiThread'] = obj.group(1)
                if line.find('Available Memory') != -1:
                    obj = re.search(r'1;33m(.*?B)', line)
                    row['availableMemory'] = obj.group(1)
                if line.find('Version') != -1:
                    obj = re.search(r'(\s+)(.*)', line)
                    row['osVersion'] = obj.group(2)
                if line.find('Topology') != -1:
                    obj = re.search(r'(\s+)(.*)', line)
                    row['sysTopology'] = obj.group(2)
                if line.find('Processor(s):') != -1:
                    obj = re.search(r'(\s+)(.*)', line)
                    row['processorInfo'] = obj.group(2)
                if line.find('Usable Memory') != -1:
                    obj = re.search(r'\((.*?B)', line)
                    row['memoryInfo'] = obj.group(1)
                if line.find('Start Time') != -1:
                    obj = re.search(
                        r'Start Time: .*?(01;33m)(.*)(\[01;37m)', line)
                    row['testStartTime'] = obj.group(2)
                if line.find('Wall Time') != -1:
                    obj = re.search(r'(\d*\.\d*).*seconds', line)
                    row['benchmarkTime'] = obj.group(1)
                if line.find('Total Computation') != -1:
                    obj = re.search(r'(\d*\.\d*).*seconds', line)
                    row['computationTime'] = obj.group(1)
                # TODO more attributes

            writer.writerow(row)

    def pgbench(self):
        needHeader = False
        if not os.path.isfile(const.datadir+'pgbench.csv'):
            needHeader = True
        os.system("mkdir "+const.datadir)
        with open(const.datadir+'pgbench.csv', 'a') as fout:
            row = OrderedDict([('instanceID', None), ('experimentID', None), ('instanceType', None), ('wallTime', None),
                               ('clients', None), ('threads', None), ('scaleFactor',
                                                                      None), ('transactionsType', None),
                               ('queryMode', None), ('duration',
                                                     None), ('transactions', None), ('mountPoint', None)
                               ])
            writer = csv.DictWriter(fout, fieldnames=row)
            if needHeader:
                writer.writeheader()
            row['instanceType'] = self.kw['instanceType']
            row['instanceID'] = self.kw['instanceID']
            row['experimentID'] = self.kw['experimentID']
            row['wallTime'] = self.kw['duration']

            mountPoint = os.popen(
                'sed -n "s/^data_directory/data_directory/p" /etc/postgresql/9.5/main/postgresql.conf').read()
            row['mountPoint'] = mountPoint
            for line in self.string:
                if line.find('clients:') != -1:
                    obj = re.search(r'(\d+)', line)
                    row['clients'] = obj.group(1)
                if line.find('threads:') != -1:
                    obj = re.search(r'(\d+)', line)
                    row['threads'] = obj.group(1)
                if line.find('factor:') != -1:
                    obj = re.search(r'(\d+)', line)
                    row['scaleFactor'] = obj.group(1)
                if line.find('type:') != -1:
                    obj = re.search(r': (.*)', line)
                    row['transactionsType'] = obj.group(1)
                if line.find('mode:') != -1:
                    obj = re.search(r': (.*)', line)
                    row['queryMode'] = obj.group(1)
                if line.find('duration:') != -1:
                    obj = re.search(r': (.*)', line)
                    row['duration'] = obj.group(1)
                if line.find('processed:') != -1:
                    obj = re.search(r'(\d+)', line)
                    row['transactions'] = obj.group(1)
            writer.writerow(row)
        pass

    def sysbench(self):
        needHeader = False
        if not os.path.isfile(const.datadir + 'sysbench.csv'):
            needHeader = True
        os.system("mkdir " + const.datadir)
        with open(const.datadir+'sysbench.csv', 'a') as fout:
            row = OrderedDict([('experimentID', None), ('instanceID', None), ('instanceType', None),
                               ('wallTime', None), ('testOption',
                                                    None), ('per-request-avg-time', None),
                               ('total-time', None), ('total-time', None)
                               ])

            writer = csv.DictWriter(fout, fieldnames=row)
            if needHeader:
                writer.writeheader()
            row['instanceType'] = self.kw['instanceType']
            row['instanceID'] = self.kw['instanceID']
            row['experimentID'] = self.kw['experimentID']
            row['wallTime'] = self.kw['duration']
            row['testOption'] = self.kw['testOption']

            i = 0
            for line in self.string:
                if line.find('per-request statistics:') != -1:
                    target = self.string[i + 2]
                    avg = re.search(r'avg:\s*(.*)', target).group(1)
                    row['per-request-avg-time'] = avg
                if line.find('total time:') != -1:
                    totalTime = re.search(r'total time:\s*(.*)', line).group(1)
                    row['total-time'] = totalTime
                if line.find('Number of threads:') != -1:
                    threadNum = re.search(
                        r'Number of threads:\s*(.*)', line).group(1)
                    row['thread-num'] = threadNum
                i += 1

            writer.writerow(row)

    def stress_ng(self):
        pass

    def bonnie(self):
        pass

    def iperf3(self):
        pass

    def bandwidth(self):
        pass

    def mbw(self):
        pass

    def getfunc(self):
        return getattr(self, self.benchmark)


class Experiment(object):
    def __init__(self, benchmark, cycle, options, experimentID):
        self.benchmark = benchmark
        self.cycle = int(cycle)
        self.options = options
        self.experimentID = experimentID

    def run(self):
        for i in range(self.cycle):
            # flush cache
            os.popen("echo 3 | sudo tee /proc/sys/vm/drop_caches").read()
            # time stamp that user percieved
            time1 = time.time()
            result = os.popen(
                const.command[self.benchmark]+self.options[self.benchmark]).read()
            time2 = time.time()
            duration = time2-time1  # unit in seconds
            myParser = parser(self.benchmark, result, testOption=self.options[self.benchmark],
                              duration=duration, experimentID=self.experimentID)
            func = myParser.getfunc()
            func()
