#!/bin/bash
date +%T.%3N

stress-ng --malloc 1000 --malloc-ops 10000 --malloc-bytes 40000

date +%T.%3N
grep -m 1 -i pgfault /proc/vmstat | cut -d' ' -f 2
grep -m 1 -i pgmajfault /proc/vmstat | cut -d' ' -f 2