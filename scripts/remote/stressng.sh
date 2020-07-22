#!/bin/bash
date +”%T.%3N”

sleep=1

for i in {1..6}
do
   stress-ng --malloc 1000 --malloc-ops 100000 --malloc-bytes 40000000 --fault 1024 --fault-ops 5000
   sleep $sleep
done

date +”%T.%3N”
grep -m 1 -i pgfault /proc/vmstat | cut -d' ' -f 2
grep -m 1 -i pgmajfault /proc/vmstat | cut -d' ' -f 2