## Capstone Project
Multi-dimensional Public Cloud Resource Contention Detection<br>
Edward Han@UWT

## Abstract
This repo are used to purposely create Resource Contention on AWS.
Main idea is to run a sort of benchmarks simultaneously on Dedicated host.

## How to do experiment
1. provision AWS instances
2. [x]TODO

## Directory Description
1. **__local__** # scripts running on my laptop while doing experiment
- **collect_data.py**
- **distribute_work.py** #distribute workload to each VM according to expiment type
- **hostfile_pssh** #public IP pool
2. **__remote__** # scripts assign to each AWS instance involved in experiment
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
