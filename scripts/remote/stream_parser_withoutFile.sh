#!/bin/bash

sum_Best_Rate=0
sum_Avg_time=0
sum_Min_time=0
sum_Max_time=0

data_parsing(){
while read Feature Best_Rate Avg_time Min_time Max_time; do
    echo "$Feature $Best_Rate $Avg_time $Min_time $Max_time"
    sum_Best_Rate=$(bc <<< "$sum_Best_Rate + $Best_Rate") 
    sum_Avg_time=$(bc <<< "$sum_Avg_time + $Avg_time")
    sum_Min_time=$(bc <<< "$sum_Min_time + $Min_time")
    sum_Max_time=$(bc <<< "$sum_Max_time + $Max_time")
    echo Total_Best_Rate: $sum_Best_Rate
    echo Total_Avg_time: $sum_Avg_time
    echo Total_Min_time: $sum_Min_time
    echo Total_Max_time: $sum_Max_time
done < "$var2"
}

var=`gcc -o -DSTREAM_ARRAY_SIZE=100000000 -fopenmp -mcmodel=medium stream.c -o stream | export OMP_NUM_THREADS=2 | for i in {1..10}; do time ./stream; done`

echo $var

#echo -n "" > data3.txt
var2=`echo $var | grep -Eo "Copy:+  +*[0-9]*.[0-9]+ +*[0-9]*.[0-9]+ +*[0-9]*.[0-9]+ +*[0-9]*.[0-9]+"` 
echo $var2

data_parsing
echo Total_Best_Rate::: $sum_Best_Rate
echo Average_Best_Rate:$(bc <<< "scale=7; $sum_Best_Rate/10")
echo Total_Avg_time::: $sum_Avg_time
echo Average_Avg_time:$(bc <<< "scale=7; $sum_Avg_time/10")
echo Total_Min_time::: $sum_Min_time
echo Average_Min_time:$(bc <<< "scale=7; $sum_Min_time/10")
echo Total_Max_time::: $sum_Max_time
echo Average_Max_time:$(bc <<< "scale=7; $sum_Max_time/10")
