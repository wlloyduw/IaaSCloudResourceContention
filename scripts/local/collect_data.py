import os
import csv
def download():
	with open('hostfile_pssh','r') as f:
		hostlist=f.read()
		hostlist=hostlist.strip().split('\n')
	datadir=':~/SCRIPT/scripts/remote/data ../../cleandata/'
	command ='scp -i as0.pem -r '

	for host in hostlist:
		wholecommand=command+host+datadir+host
		os.system(wholecommand)


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
collecter('y_cruncher.csv')