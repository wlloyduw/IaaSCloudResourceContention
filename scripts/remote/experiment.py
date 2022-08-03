#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
run.py a experiment.py  with options;
data should be collect every run, otherwise it will be overwrite;
'''

from cmath import log
import re
import csv
import const
import os
import sys
import stat
import time
import textwrap
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
            row['startTime'] = self.kw['time1']
            row['endTime'] = self.kw['time2']
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
                                                    None), ('NumberOfRuns', None),
                               ('Average-Copy best rate', None),
                               ('Average-Copy avg time', None),
                               ('Average-Copy min time', None),
                               ('Average-Copy max time', None),
                               ('Average-Scale best rate', None),
                               ('Average-Scale avg time', None),
                               ('Average-Scale min time', None),
                               ('Average-Scale max time', None),
                               ('Average-Add best rate', None),
                               ('Average-Add avg time', None),
                               ('Average-Add min time', None),
                               ('Average-Add max time', None),
                               ('Average-Triad best rate', None),
                               ('Average-Triad avg time', None),
                               ('Average-Triad min time', None),
                               ('Average-Triad max time', None),
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

            i = 0
            for line in self.string:
                if line.find('run_count') != -1:
                    runcount = self.string[i]
                    val_0 = runcount.split(":")[1]
                    row['NumberOfRuns'] = val_0
                if line.find('Copy_Average_Best_Rate') != -1:
                    copy_best_rate = self.string[i]
                    val_1 = copy_best_rate.split(":")[1]
                    row['Average-Copy best rate'] = val_1
                if line.find('Copy_Average_Avg_time') != -1:
                    copy_avg_time = self.string[i]
                    val_2 = copy_avg_time.split(":")[1]
                    row['Average-Copy avg time'] = val_2
                if line.find('Copy_Average_Min_time') != -1:
                    copy_min_time = self.string[i]
                    val_3 = copy_min_time.split(":")[1]
                    row['Average-Copy min time'] = val_3
                if line.find('Copy_Average_Max_time') != -1:
                    copy_max_time = self.string[i]
                    val_4 = copy_max_time.split(":")[1]
                    row['Average-Copy max time'] = val_4
                if line.find('Scale_Average_Best_Rate') != -1:
                    scale_best_rate = self.string[i]
                    val_5 = scale_best_rate.split(":")[1]
                    row['Average-Scale best rate'] = val_5
                if line.find('Scale_Average_Avg_time') != -1:
                    scale_avg_time = self.string[i]
                    val_6 = scale_avg_time.split(":")[1]
                    row['Average-Scale avg time'] = val_6
                if line.find('Scale_Average_Min_time') != -1:
                    scale_min_time = self.string[i]
                    val_7 = scale_min_time.split(":")[1]
                    row['Average-Scale min time'] = val_7
                if line.find('Scale_Average_Max_time') != -1:
                    scale_max_time = self.string[i]
                    val_8 = scale_max_time.split(":")[1]
                    row['Average-Scale max time'] = val_8
                if line.find('Add_Average_Best_Rate') != -1:
                    add_best_rate = self.string[i]
                    val_9 = add_best_rate.split(":")[1]
                    row['Average-Add best rate'] = val_9
                if line.find('Add_Average_Avg_time') != -1:
                    add_avg_time = self.string[i]
                    val_10 = add_avg_time.split(":")[1]
                    row['Average-Add avg time'] = val_10
                if line.find('Add_Average_Min_time') != -1:
                    add_min_time = self.string[i]
                    val_11 = add_min_time.split(":")[1]
                    row['Average-Add min time'] = val_11
                if line.find('Add_Average_Max_time') != -1:
                    add_max_time = self.string[i]
                    val_12 = add_max_time.split(":")[1]
                    row['Average-Add max time'] = val_12
                if line.find('Triad_Average_Best_Rate') != -1:
                    triad_best_rate = self.string[i]
                    val_13 = triad_best_rate.split(":")[1]
                    row['Average-Triad best rate'] = val_13
                if line.find('Triad_Average_Avg_time') != -1:
                    triad_avg_time = self.string[i]
                    val_14 = triad_avg_time.split(":")[1]
                    row['Average-Triad avg time'] = val_14
                if line.find('Triad_Average_Min_time') != -1:
                    triad_min_time = self.string[i]
                    val_15 = triad_min_time.split(":")[1]
                    row['Average-Triad min time'] = val_15
                if line.find('Triad_Average_Max_time') != -1:
                    triad_max_time = self.string[i]
                    val_16 = triad_max_time.split(":")[1]
                    row['Average-Triad max time'] = val_16
                i += 1

            writer.writerow(row)

    def pmbench(self):
        needHeader = False
        if not os.path.isfile(const.datadir + 'pmbench.csv'):
            needHeader = True
        os.system("mkdir " + const.datadir)
        with open(const.datadir+'pmbench.csv', 'a') as fout:
            row = OrderedDict([('experimentID', None), ('instanceID', None), ('instanceType', None),
                               ('wallTime', None), ('testOption',
                                                    None),
                               ('Average Page Latency', None),
                               ('Output', None)
                               ])

            writer = csv.DictWriter(fout, fieldnames=row)
            if needHeader:
                writer.writeheader()
            row['instanceType'] = self.kw['instanceType']
            row['instanceID'] = self.kw['instanceID']
            row['experimentID'] = self.kw['experimentID']
            row['wallTime'] = self.kw['duration']
            row['testOption'] = self.kw['testOption']
            row['Output'] = self.string

            i = 0
            for line in self.string:
                if line.find('Average') != -1:
                    avg_latency = self.string[i]
                    val_1 = avg_latency.split(":")[1]
                    row['Average Page Latency'] = val_1
                i += 1

            writer.writerow(row)

    def pmbenchw(self):
        needHeader = False
        if not os.path.isfile(const.datadir + 'pmbenchw.csv'):
            needHeader = True
        os.system("mkdir " + const.datadir)
        with open(const.datadir+'pmbenchw.csv', 'a') as fout:
            row = OrderedDict([('experimentID', None), ('instanceID', None), ('instanceType', None),
                               ('wallTime', None), ('testOption',
                                                    None),
                               ('Average Page Latency', None),
                               ('Output', None)
                               ])

            writer = csv.DictWriter(fout, fieldnames=row)
            if needHeader:
                writer.writeheader()
            row['instanceType'] = self.kw['instanceType']
            row['instanceID'] = self.kw['instanceID']
            row['experimentID'] = self.kw['experimentID']
            row['wallTime'] = self.kw['duration']
            row['testOption'] = self.kw['testOption']
            row['Output'] = self.string

            i = 0
            for line in self.string:
                if line.find('Average') != -1:
                    avg_latency = self.string[i]
                    val_1 = avg_latency.split(":")[1]
                    row['Average Page Latency'] = val_1
                i += 1

            writer.writerow(row)

    def pmbenchw50(self):
        needHeader = False
        if not os.path.isfile(const.datadir + 'pmbenchw50.csv'):
            needHeader = True
        os.system("mkdir " + const.datadir)
        with open(const.datadir+'pmbenchw50.csv', 'a') as fout:
            row = OrderedDict([('experimentID', None), ('instanceID', None), ('instanceType', None),
                               ('wallTime', None), ('testOption',
                                                    None),
                               ('Average Page Latency', None),
                               ('Output', None)
                               ])

            writer = csv.DictWriter(fout, fieldnames=row)
            if needHeader:
                writer.writeheader()
            row['instanceType'] = self.kw['instanceType']
            row['instanceID'] = self.kw['instanceID']
            row['experimentID'] = self.kw['experimentID']
            row['wallTime'] = self.kw['duration']
            row['testOption'] = self.kw['testOption']
            row['Output'] = self.string

            i = 0
            for line in self.string:
                if line.find('Average') != -1:
                    avg_latency = self.string[i]
                    val_1 = avg_latency.split(":")[1]
                    row['Average Page Latency'] = val_1
                i += 1

            writer.writerow(row)

    def pmbenchw20r80(self):
        needHeader = False
        if not os.path.isfile(const.datadir + 'pmbenchw20r80.csv'):
            needHeader = True
        os.system("mkdir " + const.datadir)
        with open(const.datadir+'pmbenchw20r80.csv', 'a') as fout:
            row = OrderedDict([('experimentID', None), ('instanceID', None), ('instanceType', None),
                               ('wallTime', None), ('testOption',
                                                    None),
                               ('Average Page Latency', None),
                               ('Output', None)
                               ])

            writer = csv.DictWriter(fout, fieldnames=row)
            if needHeader:
                writer.writeheader()
            row['instanceType'] = self.kw['instanceType']
            row['instanceID'] = self.kw['instanceID']
            row['experimentID'] = self.kw['experimentID']
            row['wallTime'] = self.kw['duration']
            row['testOption'] = self.kw['testOption']
            row['Output'] = self.string

            i = 0
            for line in self.string:
                if line.find('Average') != -1:
                    avg_latency = self.string[i]
                    val_1 = avg_latency.split(":")[1]
                    row['Average Page Latency'] = val_1
                i += 1

            writer.writerow(row)

    # Zening's change ZZZ
    def sklearn(self):
        needHeader = False
        if not os.path.isfile(const.datadir + 'sklearn.csv'):
            needHeader = True
        os.system("mkdir " + const.datadir)
        with open(const.datadir+'sklearn.csv', 'a') as fout:
            row = OrderedDict([('experimentID', None), ('instanceID', None), ('instanceType', None),
                               ('wallTime', None),
                               ('avg_time', None)
                               ])

            writer = csv.DictWriter(fout, fieldnames=row)
            if needHeader:
                writer.writeheader()
            row['instanceType'] = self.kw['instanceType']
            row['instanceID'] = self.kw['instanceID']
            row['experimentID'] = self.kw['experimentID']
            row['wallTime'] = self.kw['duration']

            i = 0
            for line in self.string:
                if line.find('Average') != -1:
                    avg_time = self.string[i]
                    val_1 = avg_time.split(":")[1]
                    row['avg_time'] = val_1
                i += 1

            writer.writerow(row)

    def apache_siege(self):
        needHeader = False
        if not os.path.isfile(const.datadir + 'apache_siege.csv'):
            needHeader = True
        os.system("mkdir " + const.datadir)
        with open(const.datadir+'apache_siege.csv', 'a') as fout:
            row = OrderedDict([('experimentID', None), ('instanceID', None), ('instanceType', None),
                               ('wallTime', None),
                               ('transactionsPerSecond', None)
                               ])

            writer = csv.DictWriter(fout, fieldnames=row)
            if needHeader:
                writer.writeheader()
            row['instanceType'] = self.kw['instanceType']
            row['instanceID'] = self.kw['instanceID']
            row['experimentID'] = self.kw['experimentID']
            row['wallTime'] = self.kw['duration']

            i = 0
            for line in self.string:
                if line.find('Average') != -1:
                    avg_res = self.string[i]
                    val_1 = avg_res.split(":")[1]
                    row['transactionsPerSecond'] = val_1
                i += 1

            writer.writerow(row)

    def compilebench(self):
        needHeader = False
        if not os.path.isfile(const.datadir + 'compilebench.csv'):
            needHeader = True
        os.system("mkdir " + const.datadir)
        with open(const.datadir+'compilebench.csv', 'a') as fout:
            row = OrderedDict([('experimentID', None), ('instanceID', None), ('instanceType', None),
                               ('wallTime', None),
                               ('create', None)
                               ])

            writer = csv.DictWriter(fout, fieldnames=row)
            if needHeader:
                writer.writeheader()
            row['instanceType'] = self.kw['instanceType']
            row['instanceID'] = self.kw['instanceID']
            row['experimentID'] = self.kw['experimentID']
            row['wallTime'] = self.kw['duration']

            i = 0
            for line in self.string:
                if line.find('Average') != -1:
                    avg_res = self.string[i]
                    val_1 = avg_res.split(":")[1]
                    row['create'] = val_1
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
            logging.info(const.command[self.benchmark] +
                         self.options[self.benchmark])
            # time stamp that user percieved
            time1 = time.time()
            result = os.popen(
                const.command[self.benchmark]+self.options[self.benchmark]).read()
            logging.info(result)
            time2 = time.time()
            duration = time2-time1  # unit in seconds
            myParser = parser(self.benchmark, result, testOption=self.options[self.benchmark],
                              duration=duration, time1=time1, time2=time2, experimentID=self.experimentID)
            func = myParser.getfunc()
            func()
            print(result)
