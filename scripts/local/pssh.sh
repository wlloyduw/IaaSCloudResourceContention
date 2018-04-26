#!/bin/bash
command='sysbench --test=cpu --cpu-max-prime=40000 --num-threads=1 run'
pssh -i -h hostfile_pssh -x "-i ~/.ssh/as0.pem" $command
