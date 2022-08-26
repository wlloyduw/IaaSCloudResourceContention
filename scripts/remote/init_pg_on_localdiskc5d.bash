  #!/bin/bash


  echo "checking if /dev/nvme1n1 exist"
  if [ -a /dev/nvme1n1 ]
    then
      echo "/dev/nvme1n1 exist"
  fi
  echo "...done."
  echo "Creating file system and mount at /mnt"
  sudo  mkfs -t ext3 /dev/nvme1n1
  sudo mount /dev/nvme1n1 /mnt
  echo "Stoping the Postgres server:"
  sudo service postgresql stop
  sleep 30
  echo "Moveing the database files to the new data disk:"
  sudo mv /var/lib/postgresql/9.5/main /mnt/postgres-data9.5
  sleep 10
  echo "Editing postgresql.conf:"
  CFG=/etc/postgresql/9.5/main/postgresql.conf
  K=data_directory
  V=\'/mnt/postgres-data9.5\'
  sudo sed -i "/^$K/c$K = $V" $CFG

  echo "Start Postgres:"
  sudo service postgresql start
#problem is here, how to init
  echo "initiating for sysbench IO test"
  cd /mnt/ && sudo sysbench --test=fileio --file-total-size=8G prepare