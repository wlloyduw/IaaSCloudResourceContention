import os
import getopt
import sys
import datetime
from dateutil.relativedelta import relativedelta

def pssh(minute='*',hour='*',day='*',cycles='10'):
	shellscript=r'''
	set -f
	id=$(date -u +%s)
	_task='''+"'"+minute+" "+hour+" "+day+''' * * ubuntu python3  ~/SCRIPT/scripts/remote/run.py -c '''+cycles+''' -i '$id
	task=\\'$_task\\'
	psshcommand='set -f && eval "$(ssh-agent -s)" && ssh-add -k ~/.ssh/git_capstone && rm -rf Capstone SCRIPT && git clone git@github.com:khaosminded/Capstone.git  && mv Capstone SCRIPT && cd ~/SCRIPT && cp /etc/crontab . && echo '$task' >> crontab && sudo mv crontab /etc/crontab && sudo chown root.root /etc/crontab && sudo service cron reload'
	pssh -i -h hostfile_pssh -x "-i ~/.ssh/as0.pem" $psshcommand
	'''
	respond=os.popen(shellscript).read()
	print(respond)

def getPublicIpPool():
	getPublicIp=r'aws ec2 describe-instances | grep PublicIpAddress | cut -d":" -f 2 | cut -d"," -f 1 | cut -d"\"" -f 2 '
	ipList=os.popen(getPublicIp).read()
	ipList=ipList.strip().split('\n')
	with open('hostfile_pssh','w') as f:
		for n in range(len(ipList)):
			ipList[n]='ubuntu@'+ipList[n]+'\n'
			f.write(ipList[n])


def main(argv):
	notice='#distribute_work.py# -t <minute:hour:day in UTC> -c <minutes count down>'
	if len(argv)==0:
		print(notice)
		sys.exit()
	try:
		opts, args = getopt.getopt(argv,"ht:c:n:")
	except getopt.GetoptError:
		print(notice)
		sys.exit(2)
	minute,hour,day,cycles='0，15，30，45','*','*','10'
	for opt, arg in opts:
		if opt == '-h':
			print('help: '+notice)
			sys.exit()
		elif opt in ("-t"):
			minute=arg.strip().split(':')[0]
			hour=arg.strip().split(':')[1]
			day=arg.strip().split(':')[2]
			if int(hour) not in range(24) or int(minute) not in range(60) or int(day) not in range(31): 
				print('illegal time input')
				sys.exit()
			
		elif opt in ("-c"):
			if int(arg) not in range(360):
				print('count down need to be less than 360 min')
				sys.exit()
			utc_datetime = datetime.datetime.utcnow()
			target_time=utc_datetime+relativedelta(minutes=int(arg))
			minute,hour,day=str(target_time.minute),str(target_time.hour),str(target_time.day)
		elif opt in ('-n'):
			cycles=arg

	getPublicIpPool()
	pssh(minute,hour,day,cycles)



if __name__ == "__main__":
	main(sys.argv[1:])
