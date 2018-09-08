#! /bin/bash
#pmIp="192.168.10.102"
# Capture the resource profile of a docker container at 2 time points
# Also, the processes statistics inside the container 

# The first time this is run current cpu, disk, and network storage is snapshot
# The second time this is run the differences are calculated in order to determine 
# the CPU time, Sectors read/written, and Network bytes rcv'd/transmitted 
# CPU time is in hundreths of a second (col ?)
# Sectors read is number of sectors read, where a sector is typically 512 bytes (col 2) assumes /dev/sda1
# Sectors written (col 3) assumes /dev/sda1
# network Bytes recv'd assumes eth0 (col ?)
# network Bytes written assumes eth0 (col ?)
# col 6 cpu time for processes executing in user mode
# col 7 cpu time for processes executing in kernel mode
# col 8 cpu idle time
# col 9 cpu time waiting for I/O to complete
# col 10 cpu time servicing interrupts
# col 11 cpu time servicing soft interrupts
# col 12 number of context switches
# col 13 number of disk reads completed succesfully
# col 14 number of disk reads merged together (adjacent and merged for efficiency) 
# col 15 time in ms spent reading
# col 16 number of disk writes completed succesfully
# col 17 number of disk writes merged together (adjacent and merged for efficiency)
# col 18 time in ms spent writing

## Parentheses in bash:
## Array=(element1 element2 element3) Array initialization  
## ( command1; command2 )      Command group executed within a subshell  
## result=$(COMMAND)                  Command substitution, new style  

outfile=rudata_all.json

# Get CPU stats

CPUUSRC=$(cat /sys/fs/cgroup/cpuacct/cpuacct.stat | grep 'user' | cut -d" " -f 2) # in cs

CPUKRNC=$(cat /sys/fs/cgroup/cpuacct/cpuacct.stat | grep 'system' | cut -d" " -f 2) # in cs

CPUTOTC=$(cat /sys/fs/cgroup/cpuacct/cpuacct.usage) # in ns


IFS=$'\n'

PROS=(`cat /proc/cpuinfo | grep 'processor' | cut -d":" -f 2`)
NUMPROS=${#PROS[@]}


CPU_TYPE=(`cat /proc/cpuinfo | grep 'model name' | cut -d":" -f 2 | sed 's/^ *//'`)
CPU_MHZ=(`cat /proc/cpuinfo | grep 'cpu MHz' | cut -d":" -f 2 | sed 's/^ *//'`)
CPUTYPE=${CPU_TYPE[0]}
CPUMHZ=${CPU_MHZ[0]}


# Get disk stats
arr=($(cat /sys/fs/cgroup/blkio/blkio.sectors | grep 'Total' | cut -d" " -f 2))
#[[ -z "$SRWC" ]] && SRWC=0

if [ -z "$arr" ]; then
  SRWC=0
else
  SRWC=$(( IFS=+; echo "${arr[*]}" ) | bc)
fi


arr=($(cat /sys/fs/cgroup/blkio/blkio.throttle.io_service_bytes  | grep 'Read' | \
    cut -d":" -f 2 | cut -d" " -f 3)) # in Bytes
#[[ -z "$BRC" ]] && BRC=0

if [ -z "$arr" ]; then
  BRC=0
else
  BRC=$(( IFS=+; echo "${arr[*]}" ) | bc)
fi


arr=($(cat /sys/fs/cgroup/blkio/blkio.throttle.io_service_bytes  | grep 'Write' | \
    cut -d":" -f 2 | cut -d" " -f 3)) # in Bytes
#[[ -z "$BWC" ]] && BWC=0

if [ -z "$arr" ]; then
  BWC=0
else
  BWC=$(( IFS=+; echo "${arr[*]}" ) | bc)
fi

# Get network stats

NET=(`cat /proc/net/dev | grep 'eth0'`)
NRC=${NET[1]}  # bytes received
[[ -z "$NRC" ]] && NRC=0

NTC=${NET[9]}  # bytes transmitted
[[ -z "$NTC" ]] && NTC=0


epochtime=$(date +%s)
# Get container ID
CIDS=$(cat /etc/hostname)

# Get memory stats
MEMUSEDC=$(cat /sys/fs/cgroup/memory/memory.usage_in_bytes)
MEMMAXC=$(cat /sys/fs/cgroup/memory/memory.max_usage_in_bytes)

unset IFS
CPUPERC=(`cat /sys/fs/cgroup/cpuacct/cpuacct.usage_percpu`) # in ns, 0, 1, 2, 3 elements

echo "{" > $outfile
echo "  \"cpuTime(ns)\": $CPUTOTC," >> $outfile
#echo "  \"timePerCPU (ns)\": ${CPUPERC[0]}, ${CPUPERC[1]}, ${CPUPERC[2]}, ${CPUPERC[3]} " >> $outfile

###
# echo "  \"numProcessors\": $NUMPROS," >> $outfile
# for ((i=0; i<NUMPROS; i++))
# do 
#   echo "  \"CPU${i}TIME\": ${CPUPERC[$i]}," >> $outfile
# done
###

echo "  \"processorStats\": [" >> $outfile
for (( i=0; i<NUMPROS; i++ ))
do 
  echo "  {\"CPU${i}TIME\": ${CPUPERC[$i]}}, " >> $outfile
done
echo "  {\"numProcessors\": $NUMPROS}" >> $outfile
echo "  ]," >> $outfile

echo "  \"cpuTimeUserMode(cs)\": $CPUUSRC," >> $outfile
echo "  \"cpuTimeKernelMode(cs)\": $CPUKRNC," >> $outfile

echo "  \"diskSectorIO\": $SRWC," >> $outfile
echo "  \"diskReadBytes\": $BRC," >> $outfile
echo "  \"diskWriteBytes\": $BWC," >> $outfile

echo "  \"networkBytesRecvd\": $NRC," >> $outfile
echo "  \"networkBytesSent\": $NTC," >> $outfile

echo "  \"memoryUsed\": $MEMUSEDC," >> $outfile
echo "  \"memoryMaxUsed\": $MEMMAXC," >> $outfile


echo "  \"cpuType\": \"$CPUTYPE\"," >> $outfile
echo "  \"cpuMhz\": $CPUMHZ," >> $outfile
echo "  \"containerId\": \"$CIDS\"," >> $outfile


# Stats for processes inside the container
# Number of processes
# For each process, parse the data
IFS=$'\n'
PPS=(`cat /sys/fs/cgroup/pids/tasks`)
unset IFS

length=${#PPS[@]}
PIDS=$((length-2)) # cat and rudataall.sh are 2 extra processes

#echo "  \"numProcesses\": $PIDS," >> $outfile
echo "  \"processes\": [" >> $outfile

for (( i=0; i<PIDS; i++ ))
do 
  pid=${PPS[i]}
  STAT=(`cat /proc/$pid/stat`)

  PID=${STAT[0]}
  NUMTHRDS=${STAT[19]}

  # Get process CPU stats
  UTIME=${STAT[13]}
  STIME=${STAT[14]}
  CUTIME=${STAT[15]}
  CSTIME=${STAT[16]}
  TOTTIME=$((${UTIME}+${STIME}))

  # context switch  !! double check result format
  VCSWITCH=$(cat /proc/$pid/status | grep "^voluntary_ctxt_switches" | \
      cut -d":" -f 2 | sed 's/^[ \t]*//') 
  NVCSSWITCH=$(cat /proc/$pid/status | grep "^nonvoluntary_ctxt_switches" | \
      cut -d":" -f 2 | sed 's/^[ \t]*//') 

  # sed 's/^[ \t]*//'  
  # remove all leading blank spaces including tab (\t)
  # ^[ \t]* : Search pattern ( ^ – start of the line; 
  # [ \t]* match one or more blank spaces including tab)
  # sed 's/^[ \t]*//;s/[ \t]*$//' 
  # remove all leading (^) and trailing ($) spaces including tab (\t)

  # Get process disk stats
  DELAYIO=${STAT[41]}

  # Get process memory stats
  VSIZE=${STAT[22]} # in Bytes
  RSS=${STAT[23]} # in pages



  echo "  {" >> $outfile
  echo "  \"pid\": $PID, " >> $outfile
  echo "  \"numThreads\": $NUMTHRDS, " >> $outfile
  echo "  \"cpuTimeUserMode(cs)\": $UTIME, " >> $outfile
  echo "  \"cpuTimeKernelMode(cs)\": $STIME, " >> $outfile
  echo "  \"childrenUserMode(cs)\": $CUTIME, " >> $outfile
  echo "  \"childrenKernelMode(cs)\": $CSTIME, " >> $outfile
  echo "  \"voluntaryContextSwitches\": $VCSWITCH, " >> $outfile
  echo "  \"nonvoluntaryContextSwitches\": $NVCSSWITCH, " >> $outfile
  echo "  \"blockIODelays(cs)\": $DELAYIO, " >> $outfile
  echo "  \"virtualMemoryBytes\": $VSIZE, " >> $outfile
  echo "  \"residentSetSize(page)\": $RSS " >> $outfile
  echo "  }, " >> $outfile

done

echo "  {\"numProcesses\": $PIDS}" >> $outfile
echo "  ]," >> $outfile

echo "  \"currentTime\": $epochtime" >> $outfile

echo "}" >> $outfile

cat $outfile





