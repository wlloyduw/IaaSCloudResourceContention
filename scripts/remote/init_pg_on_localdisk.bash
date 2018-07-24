#!bin/bash

#Stop the Postgres server:
sudo service postgresql stop
sleep 30
#Move the database files to the new data disk:
sudo mv /var/lib/postgresql/9.5/main /mnt/postgres-data9.5
sleep 10
#Edit postgresql.conf:
CFG=/etc/postgresql/9.5/main/postgresql.conf
K=data_directory
V=\'/mnt/postgres-data9.5\'
sudo sed -i "/^$K/c$K = $V" $CFG

#Start Postgres:
sudo service postgresql start