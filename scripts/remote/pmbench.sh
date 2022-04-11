#!/bin/bash

export FORCE_TIMES_TO_RUN=1
var=`echo "1 
1
n" | /home/ubuntu/phoronix-test-suite batch-run pts/pmbench`

var1=`echo $var | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[mGK]//g"`

pat='Average: [0-9]*\.[0-9]+'

[[ $var1 =~ $pat ]] # $pat must be unquoted
var2=`echo "${BASH_REMATCH[0]}"` 
echo $var2
#IFS=':'
#read -a strarr <<< "$var"
#echo "${strarr[0]}"
#echo "${strarr[1]}" | tr [:space:] "\n"

