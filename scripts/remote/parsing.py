#!/bin/python3
# -*- coding: utf-8 -*-

'parse and write experiment.py result into data.csv'
import re
import csv
import const
def func(benchmark,string):
	row=[]
	string=string.split('\n')
	def y_cruncher():
		for line in string:
			if line.find('Start-to-End')!=-1:
				obj = re.search( r'(\d*\.\d*).*seconds', line)
				row.append(obj.group(1))
			if line.find('Total Computation')!=-1:
				obj = re.search( r'(\d*\.\d*).*seconds', line)
				row.append(obj.group(1))
			#TODO more attributes 
		with open('./data.csv', 'w') as ff:
			writer=csv.writer(ff)
			writer.writerow(row)
	def sysbench():
		pass
	def stress_ng():
		pass
	def bonnie():
		pass
	def iperf3():
		pass
	def bandwidth():
		pass
	def mbw():
		pass


	return self.__dict__[benchmark];

# string=''
# with open('out','r') as f:
# 	string=f.read();
# parsing(string)

