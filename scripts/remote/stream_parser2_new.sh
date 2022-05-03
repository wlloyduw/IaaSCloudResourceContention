#!/bin/bash

data_parsing(){
sum_Best_Rate=0
sum_Avg_time=0
sum_Min_time=0
sum_Max_time=0
run_count=0
while read Feature Best_Rate Avg_time Min_time Max_time; do
    #echo "$Feature $Best_Rate $Avg_time $Min_time $Max_time"
    run_count=$((run_count+1))
    sum_Best_Rate=$(bc <<< "$sum_Best_Rate + $Best_Rate") 
    sum_Avg_time=$(bc <<< "$sum_Avg_time + $Avg_time")
    sum_Min_time=$(bc <<< "$sum_Min_time + $Min_time")
    sum_Max_time=$(bc <<< "$sum_Max_time + $Max_time")
    #echo Total_Best_Rate: $sum_Best_Rate
    #echo Total_Avg_time: $sum_Avg_time
    #echo Total_Min_time: $sum_Min_time
    #echo Total_Max_time: $sum_Max_time
    #echo run_count: $run_count
done <<< "$1"
}

data_extract(){
var2=`echo $var | grep -Eo ""$1":+  +*[0-9]*.[0-9]+ +*[0-9]*.[0-9]+ +*[0-9]*.[0-9]+ +*[0-9]*.[0-9]+"` 
echo $var2

data_parsing "${var2}"
#echo run_count_1:$run_count
#echo Total_Best_Rate::: $sum_Best_Rate
echo "$1"_Average_Best_Rate:$(bc <<< "scale=7; $sum_Best_Rate/$run_count")
#echo Total_Avg_time::: $sum_Avg_time
echo "$1"_Average_Avg_time:$(bc <<< "scale=7; $sum_Avg_time/$run_count")
#echo Total_Min_time::: $sum_Min_time
echo "$1"_Average_Min_time:$(bc <<< "scale=7; $sum_Min_time/$run_count")
#echo Total_Max_time::: $sum_Max_time
echo "$1"_Average_Max_time:$(bc <<< "scale=7; $sum_Max_time/$run_count")
echo run_count:$run_count
}

var=`export OMP_NUM_THREADS=2 | for i in {1..15}; do time ./stream; done`

#echo $var

#echo -n "" > data3.txt
data_extract "Copy"
data_extract "Scale"
data_extract "Add"
data_extract "Triad"

