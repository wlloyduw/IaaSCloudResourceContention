# Capstone Project

Multi-dimensional Public Cloud Resource Contention Detection<br>
Advisor, Wes Lloyd@UWT
Edward Han@UWT

## Abstract

This repo is used to purposely create Resource Contention on AWS.
Main idea is to run a sort of benchmarks simultaneously on Dedicated host.

## How to do experiment

1. provision AWS instances
   - for iperf tag half instance as <key:iperfRole, val:client> and half <key:iperfRole, val:server>
2. python3 distribute_work.py / iperf_master.py accordingly
3. python3 collect_data.py

## Directory Description

1. \***\*local\*\*** # scripts running on my laptop while doing experiment

- **collect_data.py**
- **distribute_work.py** #distribute workload to each VM according to expiment type
- **hostfile_pssh** #public IP pool

2. \***\*remote\*\*** # scripts assign to each AWS instance involved in experiment

- **const.py** #defined a sort of constant, such as benchmark name, etc.
- **experiment.py** #mainly defined Parser for grabing output of benchmark
- **run.py** #main()

## Manual

run.py<br>
-c [num of cycles]<br>
-i [exp_id]<br>
-t [exp_type]<br>

distribute_work.py<br>
-h : help<br>
-r :dedicated host reverse_mode 1to16 (16to1 by default)<br>
-t/c [minute:hour:day in UTC]/[minutes count down]<br>
-n [num of works]<br>
-d [dedicated host mode interval]<br>

## Updates

**July 22. 2018** Add a init script for pgbench experiment

**Oct 7. 2018** Add two sepretated .py for iperf experiment

     iperf_master.py
     iperf_slave.py

Dependencies(may uncomprehensive)

1. slavenode

   - git
   - all benchmarks [iperf, pgbench, y-cruncher, sysbench, ...]

2. masternode

   - pssh
   - scp
   - ssh

3. shared

   - python3 [re,csv...a sort of packages]
   - environment variables & paths [.pem .csv .py]

Refactor most of exsited scripts to support iperf<br>
Part of the reason is functional problem and design flaw in previous work<br>
Main reason is that I wanna do some improvment on it and get rid of that whole that of mess...<br>
Since I mix python3 and some shell, it's hard to debug<br>
Overall, it's not element...uhhh, but much better than that before.<br>
It's partially maintainable, fairly scalable, definitely conquered what we wanted :)...<br>
