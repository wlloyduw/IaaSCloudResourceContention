#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import os
import csv
import threading
def download():
	with open('hostfile_pssh','r') as f:
		hostlist=f.read()
		hostlist=hostlist.strip().split('\n')
	datadir=':~/SCRIPT/scripts/remote/data ../../cleandata/'
	command ='scp -i as0.pem -r '
	threadlist=[]
	for host in hostlist:
		wholecommand=command+host+datadir+host
		def func(i):
			def run():
				os.system(i)
			return threading.Thread(target=run,name=i)
		threadlist.append(func(wholecommand))
	for threads in threadlist:
		threads.start()
	for threads in threadlist:
		threads.join()

def collecter(filename):
	a=os.popen('ls ../../cleandata/./').read()
	a=a.strip().split('\n')
	needHeader=False
	if not os.path.isfile('../../cleandata/data/'+filename):
		needHeader=True
		os.system('mkdir ../../cleandata/data')
	f=open('../../cleandata/data/'+filename,'a')
	writer=csv.writer(f)
	for eachdir in a:
		if 'ubuntu' in eachdir:
			#print(eachdir)
			path='../../cleandata/'+eachdir+'/'+filename
			with open(path,'r') as f:
				reader=csv.reader(f)
				if needHeader is True:
					needHeader=False
					writer.writerow(next(reader))
				else:
					next(reader)
				for row in reader:
					writer.writerow(row)
	f.close() 
	os.system('rm -r ../../cleandata/ubuntu*')

download()
collecter('pgbench.csv')