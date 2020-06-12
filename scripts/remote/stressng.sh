#!/bin/bash
stress-ng --malloc 1000 --malloc-ops 100000 --malloc-bytes 40000000 --fault 1024 --fault-ops 500000
grep -m 1 -i pgfault /proc/vmstat | cut -d' ' -f 2
grep -m 1 -i pgmajfault /proc/vmstat | cut -d' ' -f 2