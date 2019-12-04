setwd("/home/ravschoo/ResourceContention/IaaSCloudResourceContention/modeldata/m5d/")
#Clear workspace 
rm(list=ls())

library(tidyverse)
library(splitstackshape)

#load DedicatedHost Data
set.seed(100)
wholeSet = read.csv("./merged.csv")
wholeSet$iperf <- wholeSet$iperf * 1000 

#Scale data
#Scale data to make it normally distributed

iperf_scaled <- scale(wholeSet$iperf)
summary(iperf_scaled)

pgbench_scaled <- scale(wholeSet$pgbench)
summary(pgbench_scaled)

sysbench_scaled <- scale(wholeSet$sysbench)
summary(sysbench_scaled)

ycruncher_scaled <- scale(wholeSet$ycruncher)
summary(ycruncher_scaled)

#Lets use the scaled data to train the model
wholeSet$iperf <- iperf_scaled
wholeSet$pgbench <- pgbench_scaled
wholeSet$sysbench <- sysbench_scaled
wholeSet$ycruncher <- ycruncher_scaled

model <- lm(setId ~ iperf + pgbench + sysbench + ycruncher, data = wholeSet)
summary(model)

#Save this model
saveRDS(model, "./model_mlr_unstrat.rds")

## Get mean and sd for each benchmark.  Use this to scale the prediction data
means <- vector()
sds <- vector()

means[1] <- mean(sysbench_scaled)
sds[1] <- sd(sysbench_scaled)
means[2] <- mean(ycruncher_scaled)
sds[2] <- sd(ycruncher_scaled)
means[3] <- mean(pgbench_scaled)
sds[3] <- sd(pgbench_scaled)
means[4] <- mean(iperf_scaled, na.rm=TRUE)
sds[4] <- sd(iperf_scaled, na.rm=TRUE)

save(means, file="./means.rds")
save(sds, file="./sds.rds")
