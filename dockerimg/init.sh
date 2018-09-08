#!bin/bash
#setup postgres server
service postgresql restart
sudo -u postgres createdb ubuntu
sudo -u postgres -s createuser root
pgbench -i ubuntu
