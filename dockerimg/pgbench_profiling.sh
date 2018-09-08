#!bin/bash

./SCRIPT/scripts/remote/plugin/rudata/rudataall.sh > rudata_all_1.json
pgbench --client=10 --jobs=10 --time=60  ubuntu
./SCRIPT/scripts/remote/plugin/rudata/rudataall.sh > rudata_all_2.json
./SCRIPT/scripts/remote/plugin/rudata/rudatadelta.sh rudata_all_1.json rudata_all_2.json
jq < rudata_delta.json