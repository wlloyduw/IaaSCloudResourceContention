#!/bin/bash
date +%T.%3N

stress-ng --malloc 100 --malloc-ops 1000 --malloc-bytes 40000 --fault 500 --fault-ops 500

date +%T.%3N
grep -m 1 -i pgfault /proc/vmstat | cut -d' ' -f 2
grep -m 1 -i pgmajfault /proc/vmstat | cut -d' ' -f 2