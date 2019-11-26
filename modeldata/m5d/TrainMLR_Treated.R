setwd("/home/ravschoo/ResourceContention/IaaSCloudResourceContention/modeldata/m5d/")
#Clear workspace 
rm(list=ls())

library(tidyverse)
library(splitstackshape)

#load DedicatedHost Data
set.seed(100)
wholeSet = read.csv("./merged.csv")
wholeSet$iperf <- wholeSet$iperf * 1000 

#Statify a new dataset so that we have same number of samples for each vm tenancy.
strat_data <- stratified(indt=wholeSet, group=c("setId"), size=3)

#Scale data
#Scale data to make it normally distributed

iperf_scaled <- scale(strat_data $iperf)
summary(iperf_scaled)

pgbench_scaled <- scale(strat_data$pgbench)
summary(pgbench_scaled)

sysbench_scaled <- scale(strat_data$sysbench)
summary(sysbench_scaled)

ycruncher_scaled <- scale(strat_data$ycruncher)
summary(ycruncher_scaled)

#Lets use the scaled data to train the model
strat_data$iperf <- iperf_scaled
strat_data$pgbench <- pgbench_scaled
strat_data$sysbench <- sysbench_scaled
strat_data$ycruncher <- ycruncher_scaled

#Lets leave out iperf for now
model <- lm(setId ~ pgbench + sysbench + ycruncher, data = strat_data)
summary(model)

#Save this model
saveRDS(model, "./model_mlr_treated_no_iperf.rds")
