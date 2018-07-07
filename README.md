# Capstone Project
Multi-dimensional Public Cloud Resource Contention Detection


## Abstract
This repo are used to purposely create Resource Contention on AWS.
Main idea is simultaneously running a sort of benchmarks on Dedicated host.
Functions include scheduling experiment based on CRONTAB,
generating formated data which may reflect performance degradation,
downloading data to local and proceeding data analyse.

## Directory Description
├── local # scripts running on my laptop while doing experiment
│   ├── collect_data.py
│   ├── distribute_work.py #distribute workload to each VM according to expiment type
│   ├── hostfile_pssh #public IP pool
└── remote # scripts assign to each AWS instance involved in experiment
    ├── const.py #defined a sort of constant, such as benchmark name, etc.
    ├── experiment.py #mainly defined Parser for grabing output of benchmark
    └── run.py #main()

## Manual 
run.py 
  -c <num of cycles> 
  -i <exp_id> 
  -t <exp_type>

distribute_work.py
	-h : help
	-t/c <minute:hour:day in UTC>/<minutes count down> 
	-n <num of works> 
	-d <dedicated host mode interval>
