#!/bin/python3
#parsing y-cruncher

import re
import csv
def parsing(s):
	wallTime=None
	computationTime=None
	startTime=None
	row=[]
	s=s.split('\n')
	for line in s:
		if line.find('Start-to-End')!=-1:
			obj = re.search( r'(\d*\.\d*).*seconds', line)
			row.append(obj.group(1))
		if line.find('Total Computation')!=-1:
			obj = re.search( r'(\d*\.\d*).*seconds', line)
			row.append(obj.group(1))
	with open('./some.csv', 'w') as ff:
		writer=csv.writer(ff)
		writer.writerow(row)
	return wallTime

s=''
with open('out','r') as f:
	s=f.read();
parsing(s)

