#!/bin/bash
set -f
id=$(date -u +%s)
_task='20 * * * * ubuntu python3  ~/SCRIPT/remote/run.py -c 10 -i '$id
task=\'$_task\'
psshcommand='set -f && cp /etc/crontab . && echo '$task' >> crontab && sudo mv crontab /etc/crontab'
pssh -i -h hostfile_pssh -x "-i ~/.ssh/as0.pem" $psshcommand
