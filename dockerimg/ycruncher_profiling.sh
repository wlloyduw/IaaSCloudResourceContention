#!bin/bash

./SCRIPT/scripts/remote/plugin/rudata/rudataall.sh > rudata_all_1.json
/home/ubuntu/CPU_test/y-cruncher\ v0.7.5.9480-static/y-cruncher << EOF\n0\n1\n1\nEOF\n
./SCRIPT/scripts/remote/plugin/rudata/rudataall.sh > rudata_all_2.json
./SCRIPT/scripts/remote/plugin/rudata/rudatadelta.sh rudata_all_1.json rudata_all_2.json
jq < rudata_delta.json