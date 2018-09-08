FROM ubuntu
RUN apt-get update
RUN apt-get install -y sysbench
RUN apt-get install -y jq
RUN apt-get install -y bc
RUN apt-get install -y  python3
COPY . /home/ubuntu/
COPY ec2metadata /usr/bin/ec2metadata
