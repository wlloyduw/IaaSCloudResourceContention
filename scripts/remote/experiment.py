#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'run.py a experiment.py  with parameter'

import re
import csv
import const
import os
from collections import OrderedDict
class parser(object):
    #kw need experimentID testOption
    def __init__(self,benchmark,string,**kw):
        self.string=string.split('\n')
        self.benchmark=benchmark
        self.kw=kw
        ec2metadata=os.popen('ec2metadata').read()
        self.kw['instanceType']=re.search(r'instance-type: (\w*\.\w*)',ec2metadata)
        self.kw['instanceID']=re.search(r'instance-id: (.*)\n',ec2metadata)

    def y_cruncher(self):
        needHeader=False
        if not os.path.isfile('./data/y_cruncher.csv'):
            needHeader=True
        with open('./data/y_cruncher.csv', 'a') as fout:
            row=OrderedDict([('instanceID',None),('experimentID',None),('instanceType',None)\
                            ('memoryInfo',None),('processorInfo',None),('sysTopology',None),\
                             ('osVersion',None),('testStartTime',None),('testOption',None),('availableMemory',None),\
                            ('isMultiThread',None),('cpuUtilization',None),('multiCoreEfficiency',None),\
                            ('computationTime',None),('wallTime',None)\
                            ])
            writer = csv.DictWriter(fout,fieldnames=row)
            if needHeader:
                writer.writeheader()
<<<<<<< HEAD

            row['instanceType']=self.kw['instanceType']
            row['instanceID']=self.kw['instanceID']
            row['experimentID']=self.kw['experimentID']
            row['testOption']=self.kw['testOption']

=======
            row['instanceID']=os.popen('curl --connect-timeout 1 http://169.254.169.254/latest/meta-data/public-hostname').read()
            row['experimentID']=self.kw['experimentID']
            row['testOption']=self.kw['testOption']
>>>>>>> ed6e564561c98dc778c9b85c8d7feb86eb91166f
                #todo instanceID experimentID testOption
            for line in self.string:

                if line.find('Multi-core Efficiency')!=-1:
                    obj = re.search(r'(\d*\.\d* %)',line)
                    row['multiCoreEfficiency']=obj.group(1)
                if line.find('CPU Utilization')!=-1:
                    obj = re.search(r'(\d*\.\d* %)',line)
                    row['cpuUtilization']=obj.group(1)
                if line.find('Multi-Threading')!=-1:
                    obj = re.search(r'\[01;36m(\w*)',line)
                    row['isMultiThread']=obj.group(1)
                if line.find('Available Memory')!=-1:
                    obj = re.search(r'(\d* MiB)',line)
                    row['availableMemory']=obj.group(1)
                if line.find('Version')!=-1:
                    obj = re.search(r'(\s+)(.*)',line)
                    row['osVersion']=obj.group(2)
                if line.find('Topology')!=-1:
                    obj = re.search(r'(\s+)(.*)',line)
                    row['sysTopology']=obj.group(2)
                if line.find('Processor(s):')!=-1:
                    obj = re.search(r'(\s+)(.*)',line)
                    row['processorInfo']=obj.group(2)
                if line.find('Usable Memory')!=-1:
                    obj = re.search(r'(\d* MiB)',line)
                    row['memoryInfo']=obj.group(1)
                if line.find('Start Time')!=-1:
                    obj = re.search( r'Start Time: .*?(01;33m)(.*)(\[01;37m)', line)
                    row['testStartTime']=obj.group(2)
                if line.find('Wall Time')!=-1:
                    obj = re.search( r'(\d*\.\d*).*seconds', line)
                    row['wallTime']=obj.group(1)
                if line.find('Total Computation')!=-1:
                    obj = re.search( r'(\d*\.\d*).*seconds', line)
                    row['computationTime']=obj.group(1)
                #TODO more attributes 
        
            writer.writerow(row)
            
    def sysbench(self):
        pass
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
        return getattr(self,self.benchmark)


class Experiment(object):
	def __init__(self, benchmark,cycle,parameter,experimentID):
		self.benchmark = benchmark
		self.cycle=int(cycle)
		self.parameter=parameter
		self.experimentID=experimentID
	def run(self):
		for i in range(self.cycle):
			myParser=parser(self.benchmark,os.popen(const.command[self.benchmark]+self.parameter[self.benchmark]).read(),\
				testOption=self.parameter[self.benchmark],experimentID=self.experimentID)
			func=myParser.getfunc()
			func()
		