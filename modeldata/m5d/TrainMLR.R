setwd("/home/ravschoo/ResourceContention/IaaSCloudResourceContention/modeldata/m5d/")
#Clear workspace 
rm(list=ls())

library(tidyverse)
library(splitstackshape)

#load DedicatedHost Data
set.seed(100)
wholeSet = read.csv("./merged_qt_144.csv")

#Statify a new dataset so that we have same number of samples for each vm tenancy.

model <- lm(setId ~ iperf + pgbench + sysbench + ycruncher, data = wholeSet)
summary(model)

#Save this model
saveRDS(model, "./model_mlr.rds")
