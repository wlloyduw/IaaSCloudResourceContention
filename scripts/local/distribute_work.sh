#!/bin/bash
set -f
id=$(date -u +%s)
_task='41 * * * * ubuntu python3  ~/SCRIPT/scripts/remote/run.py -c 10 -i '$id
task=\'$_task\'
psshcommand='set -f && cd ~/SCRIPT && git pull && cp /etc/crontab . && echo '$task' >> crontab && sudo mv crontab /etc/crontab && sudo service cron reload'
pssh -i -h hostfile_pssh -x "-i ~/.ssh/as0.pem" $psshcommand
