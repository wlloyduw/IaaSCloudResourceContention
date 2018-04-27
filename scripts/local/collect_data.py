import os
with open('hostfile_pssh','r') as f:
    hostlist=f.read()
    hostlist=hostlist.strip().split('\n')
datadir=':~/SCRIPT/scripts/remote/data ../../cleandata/'
command ='scp -i as0.pem -r '

for host in hostlist:
    wholecommand=command+host+datadir+host
    os.system(wholecommand)