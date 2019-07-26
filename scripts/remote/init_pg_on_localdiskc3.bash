#!bin/bash
echo "c3 instance: moving postgresql to the ephemeral drive before test..."

if [[ ! -d /mnt/postgres-data9.5 ]]
then
  #Stop the Postgres server:
  sudo service postgresql stop
  sleep 30
  #Move the database files to the new data disk:
  sudo mv /var/lib/postgresql/9.5/main /mnt/main
  sudo -u postgres ln -s /mnt/main /var/lib/postgresql/9.5/main 
  sleep 10
  #Edit postgresql.conf:
  #CFG=/etc/postgresql/9.5/main/postgresql.conf
  #K=data_directory
  #V=\'/mnt/postgres-data9.5\'
  #sudo sed -i "/^$K/c$K = $V" $CFG

  #Start Postgres:
  sudo service postgresql start
fi
