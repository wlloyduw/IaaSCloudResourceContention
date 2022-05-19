#!/bin/bash

# Run times, it depends on test duration
export FORCE_TIMES_TO_RUN=1

# Select the options and run the test 
test_result=`echo "1
n" | phoronix-test-suite run compilebench`

# Remove the color code
text=`echo $test_result | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[mGK]//g"`

pat='Average: [0-9]*\.[0-9]+'

# Match the result 'Average: '
[[ $text =~ $pat ]]
matched=`echo "${BASH_REMATCH[0]}"`
echo $matched
