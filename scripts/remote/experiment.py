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
import sys
import stat
import time
from datetime import datetime
from collections import OrderedDict
import subprocess
import logging
logging.basicConfig(level=logging.DEBUG,
                    filename=const.logdir + 'experiment.log')


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

            # 'sed -n "s/^data_directory/data_directory/p" /etc/postgresql/9.5/main/postgresql.conf | cut -d\'#\' -f 1').readline().rstrip().partition('\n')[0]
            mountPoint = os.popen(
                'sed -n "s/^data_directory/data_directory/p" /etc/postgresql/9.5/main/postgresql.conf | cut -d\'#\' -f 1').readline().rstrip()
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
        with open(const.datadir+'sysbench1.csv', 'a') as fout:
            row = OrderedDict([('experimentID', None), ('instanceID', None), ('instanceType', None),
                               ('wallTime', None), ('testOption',
                                                    None), ('per-request-avg-time', None),
                               ('total-time', None), ('thread-num', None)
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

    def sysbench_ram(self):
        needHeader = False
        if not os.path.isfile(const.datadir + 'sysbench_ram.csv'):
            needHeader = True
        os.system("mkdir " + const.datadir)
        with open(const.datadir+'sysbench_ram.csv', 'a') as fout:
            row = OrderedDict([('experimentID', None), ('instanceID', None), ('instanceType', None),
                               ('wallTime', None), ('testOption',
                                                    None), ('ram_write_speed', None),
                               ('total-time', None), ('thread-num', None)
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
                if line.find('transferred') != -1:
                    speed = re.search(r'\((\d*\.\d*) MB/sec\)', line).group(1)
                    row['ram_write_speed'] = speed
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
        os.chmod(const.remotedir+'stressng.sh', stat.S_IRWXU)
        proc = subprocess.check_output([const.remotedir+'stressng.sh'])
        pgfaultList = proc.decode('utf-8').split("\n")
        pgfault = pgfaultList[5]
        pgmajfault = pgfaultList[6]
        startTime = pgfaultList[0]
        endTime = pgfaultList[4]
        runtime = (datetime.strptime(endTime, "%H:%M:%S.%f") -
                   datetime.strptime(startTime, "%H:%M:%S.%f")).total_seconds()

        needHeader = False
        if not os.path.isfile(const.datadir + 'stress_ng.csv'):
            needHeader = True
        os.system("mkdir " + const.datadir)
        with open(const.datadir+'stress_ng.csv', 'a') as fout:
            row = OrderedDict([('experimentID', None), ('instanceID', None), ('instanceType', None),
                               ('wallTime', None), ('testOption',
                                                    None), ('vpgFaults', None), ('vmajorpgFaults', None),
                               ('startTime', None), ('endTime', None)])

            writer = csv.DictWriter(fout, fieldnames=row)
            if needHeader:
                writer.writeheader()
            row['instanceType'] = self.kw['instanceType']
            row['instanceID'] = self.kw['instanceID']
            row['experimentID'] = self.kw['experimentID']
            row['wallTime'] = runtime
            row['testOption'] = self.kw['testOption']
            row['vpgFaults'] = pgfault
            row['vmajorpgFaults'] = pgmajfault
            row['startTime'] = startTime
            row['endTime'] = endTime

            writer.writerow(row)

    def cachebench(self):
        needHeader = False
        if not os.path.isfile(const.datadir + 'cachebench.csv'):
            needHeader = True
        os.system("mkdir " + const.datadir)
        with open(const.datadir+'cachebench.csv', 'a') as fout:
            row = OrderedDict([('experimentID', None), ('instanceID', None), ('instanceType', None),
                               ('wallTime', None), ('testOption',
                                                    None), ('1 KiB Throughput', None),
                               ('1 MiB Throughput', None),
                               ('1 GiB Throughput', None),
                               ('4 GiB Throughput', None),
                               ('total-time', None), ('thread-num', None)
                               ])

            writer = csv.DictWriter(fout, fieldnames=row)
            if needHeader:
                writer.writeheader()
            row['instanceType'] = self.kw['instanceType']
            row['instanceID'] = self.kw['instanceID']
            row['experimentID'] = self.kw['experimentID']
            row['wallTime'] = self.kw['duration']
            row['testOption'] = self.kw['testOption']
            row['total-time'] = self.string

            i = 0
            for line in self.string:
                if line.find('1024') != -1:
                    target_1KiB = self.string[i]
                    val_1KiB = target_1KiB.split(" ")[1]
                    row['1 KiB Throughput'] = val_1KiB
                if line.find('1048576') != -1:
                    target_1MiB = self.string[i]
                    val_1MiB = target_1MiB.split(" ")[1]
                    row['1 MiB Throughput'] = val_1MiB
                if line.find('1073741824') != -1:
                    target_1GiB = self.string[i]
                    val_1GiB = target_1GiB.split(" ")[1]
                    row['1 GiB Throughput'] = val_1GiB
                if line.find('4294967296') != -1:
                    target_4GiB = self.string[i]
                    val_4GiB = target_4GiB.split(" ")[1]
                    row['4 GiB Throughput'] = val_4GiB
                i += 1

            writer.writerow(row)

    def cachebenchw(self):
        needHeader = False
        if not os.path.isfile(const.datadir + 'cachebenchw.csv'):
            needHeader = True
        os.system("mkdir " + const.datadir)
        with open(const.datadir+'cachebenchw.csv', 'a') as fout:
            row = OrderedDict([('experimentID', None), ('instanceID', None), ('instanceType', None),
                               ('wallTime', None), ('testOption',
                                                    None), ('1 KiB Throughput', None),
                               ('1 MiB Throughput', None),
                               ('1 GiB Throughput', None),
                               ('4 GiB Throughput', None),
                               ('total-time', None), ('thread-num', None)
                               ])

            writer = csv.DictWriter(fout, fieldnames=row)
            if needHeader:
                writer.writeheader()

            row['instanceType'] = self.kw['instanceType']
            row['instanceID'] = self.kw['instanceID']
            row['experimentID'] = self.kw['experimentID']
            row['wallTime'] = self.kw['duration']
            row['testOption'] = self.kw['testOption']
            row['total-time'] = self.string

            i = 0
            for line in self.string:
                if line.find('1024') != -1:
                    target_1KiB = self.string[i]
                    val_1KiB = target_1KiB.split(" ")[1]
                    row['1 KiB Throughput'] = val_1KiB
                if line.find('1048576') != -1:
                    target_1MiB = self.string[i]
                    val_1MiB = target_1MiB.split(" ")[1]
                    row['1 MiB Throughput'] = val_1MiB
                if line.find('1073741824') != -1:
                    target_1GiB = self.string[i]
                    val_1GiB = target_1GiB.split(" ")[1]
                    row['1 GiB Throughput'] = val_1GiB
                if line.find('4294967296') != -1:
                    target_4GiB = self.string[i]
                    val_4GiB = target_4GiB.split(" ")[1]
                    row['4 GiB Throughput'] = val_4GiB
                i += 1

            writer.writerow(row)

    def cachebenchb(self):
        needHeader = False
        if not os.path.isfile(const.datadir + 'cachebenchb.csv'):
            needHeader = True
        os.system("mkdir " + const.datadir)
        with open(const.datadir+'cachebenchb.csv', 'a') as fout:
            row = OrderedDict([('experimentID', None), ('instanceID', None), ('instanceType', None),
                               ('wallTime', None), ('testOption',
                                                    None), ('1 KiB Throughput', None),
                               ('1 MiB Throughput', None),
                               ('1 GiB Throughput', None),
                               ('4 GiB Throughput', None),
                               ('total-time', None), ('thread-num', None)
                               ])

            writer = csv.DictWriter(fout, fieldnames=row)
            if needHeader:
                writer.writeheader()
            row['instanceType'] = self.kw['instanceType']
            row['instanceID'] = self.kw['instanceID']
            row['experimentID'] = self.kw['experimentID']
            row['wallTime'] = self.kw['duration']
            row['testOption'] = self.kw['testOption']
            row['total-time'] = self.string

            i = 0
            for line in self.string:
                if line.find('1024') != -1:
                    target_1KiB = self.string[i]
                    val_1KiB = target_1KiB.split(" ")[1]
                    row['1 KiB Throughput'] = val_1KiB
                if line.find('1048576') != -1:
                    target_1MiB = self.string[i]
                    val_1MiB = target_1MiB.split(" ")[1]
                    row['1 MiB Throughput'] = val_1MiB
                if line.find('1073741824') != -1:
                    target_1GiB = self.string[i]
                    val_1GiB = target_1GiB.split(" ")[1]
                    row['1 GiB Throughput'] = val_1GiB
                if line.find('4294967296') != -1:
                    target_4GiB = self.string[i]
                    val_4GiB = target_4GiB.split(" ")[1]
                    row['4 GiB Throughput'] = val_4GiB
                i += 1

            writer.writerow(row)

    def stream(self):
        needHeader = False
        if not os.path.isfile(const.datadir + 'stream.csv'):
            needHeader = True
        os.system("mkdir " + const.datadir)
        with open(const.datadir+'stream.csv', 'a') as fout:
            row = OrderedDict([('experimentID', None), ('instanceID', None), ('instanceType', None),
                               ('wallTime', None), ('testOption',
                                                    None), ('Copy best rate', None),
                               ('Copy avg time', None),
                               ('Copy min time', None),
                               ('Copy max time', None),
                               ('total-time', None),
                               ('thread-num', None),
                               ('Output-Stream', None)
                               ])

            writer = csv.DictWriter(fout, fieldnames=row)
            if needHeader:
                writer.writeheader()

            row['instanceType'] = self.kw['instanceType']
            row['instanceID'] = self.kw['instanceID']
            row['experimentID'] = self.kw['experimentID']
            row['wallTime'] = self.kw['duration']
            row['testOption'] = self.kw['testOption']
            row['Output-Stream'] = self.string

            #j = 0
            # for a in self.string:
            # obj = re.search(
            # r'Copy:\s+([0-9]*\.[0-9]+( +[0-9]*\.[0-9]+)+)', a).group(1)
            #row['Copy best rate'] = obj
            #row['Copy avg time'] = j
            #j += 1

            i = 0
            obj_data = 0
            count = 0
            for line in self.string:
                if line.find('Copy:') != -1:
                    obj = re.search(
                        r'Copy:\s+([0-9]*\.[0-9]+( +[0-9]*\.[0-9]+)+)', line).group(1)
                    obj_data += int(obj)
                    row['Copy best rate'] = obj_data
                    count += i
                    row['Copy avg time'] += count
                if line.find('1048576') != -1:
                    target_1MiB = self.string[i]
                    val_1MiB = target_1MiB.split(" ")[1]
                    row['Scale'] = val_1MiB
                if line.find('1073741824') != -1:
                    target_1GiB = self.string[i]
                    val_1GiB = target_1GiB.split(" ")[1]
                    row['Add'] = val_1GiB
                if line.find('4294967296') != -1:
                    target_4GiB = self.string[i]
                    val_4GiB = target_4GiB.split(" ")[1]
                    row['Triad'] = val_4GiB
                i += 1

            writer.writerow(row)

    def bonnie(self):
        pass

    def iperf3(self):
        pass

    def bandwidth(self):
        pass

    def mbw(self):
        pass

    y_cruncherc3 = y_cruncher
    y_cruncherc4 = y_cruncher
    y_cruncherz1d = y_cruncher
    y_cruncherm5d = y_cruncher

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
            print(const.command[self.benchmark]+self.options[self.benchmark])
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
            print(result)
