# Capstone Project

Multi-dimensional Public Cloud Resource Contention Detection<br>
Advisor, Wes Lloyd@UWT
Edward Han@UWT

## Abstract

This repo is used to purposely create Resource Contention on AWS.<br/>
Main idea is to run a sort of benchmarks simultaneously on Dedicated host.

## How to do experiment

1. provision AWS instances using **ami-0c85437aa3f534a1a**
   - for iperf
     - tag half instance as <key:iperfRole, val:client> and half <key:iperfRole, val:server>
   - for pgbench
     - provision c3 with instance store
2. python3 distribute_work.py / iperf_master.py accordingly
3. python3 collect_data.py
   - for iperf
     - use iperClient as input when collecting data
   - for other benchmarks
     - use hostfile input when collecting data
4. proceeding .csv file with jupyter-notebokk accordingly, if needed

## Directory Description

    #scripts/
    .
    ├── local
    │   ├── collect_data.py
    │   ├── crontab # use linux crontab as a RPC interface
    │   ├── crontab.bak
    │   ├── distribute_work.py # entrance module on local
    │   ├── hostfile_pssh #public IP pool
    │   ├── iperfClients  #public IP pool
    │   ├── iperfServers  #public IP pool
    │   ├── iperf_master.py #for iperf only
    └── remote
        ├── __init__.py
        ├── const.py #defined a sort of constant, such as benchmark name, etc.
        ├── experiment.py #mainly defined Parser for grabing output of benchmark
        ├── init_pg_on_localdisk.bash #will be invoked when working with pgbench
        ├── iperf_slave.py # for iperf only
        └── run.py # entrance module on remote

## Manual

run.py<br>

    -c [num of cycles]
    -i [exp_id]
    -t [exp_type]

distribute_work.py

    -h #help
    -r #dedicated host reverse_mode 1to16 (16to1 by default)
    -t/c [minute:hour:day in UTC]/[minutes count down]
    -n [num of works]
    -d [dedicated host mode interval]

## Updates

**Oct 10. 2018** Version 1.0 - Add support to sysbench

**Oct 7. 2018** Add two sepretated .py for iperf experiment

     iperf_master.py
     iperf_slave.py

- Dependencies

  - slavenode

    - git, all benchmarks [iperf, pgbench, y-cruncher, sysbench, ...]

  - masternode

    - pssh, scp, ssh

  - shared
    - python3 [re,csv...a sort of packages]
    - environment variables
    - file paths [.pem .csv .py]

Previous module have some design flaw since most of the work was served for making a proof that our method is feasible<br>
For convenience and agile, I simplely mixed python3 and some bash scripts without encapsulation, which lead to a painful experience of maintaining after that...<br>
At this time, rewrite is much faster than reuse... well, quality of those two new added module is quite better than what I wrote before.
Overall, it's fairly scalable now, and definitely can achieve our goal :)<br>
I'm on the way to coding elegantly!

**July 22. 2018** Add a init script for pgbench experiment

     init_pg_on_localdisk.bash
