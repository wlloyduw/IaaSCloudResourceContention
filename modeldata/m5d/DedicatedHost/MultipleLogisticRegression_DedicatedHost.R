setwd("/home/ravschoo/ResourceContention/IaaSCloudResourceContention/modeldata/m5d/")
#Clear workspace 
rm(list=ls())

set.seed(100)
wholeSet = read.csv("./merged.csv")
#If iperf is in gbs turn to mbs
wholeSet$iperf <- wholeSet$iperf * 1000

library(nnet)
formula = setId~iperf+sysbench+ycruncher+pgbench
multinomModel <- multinom(formula, data=wholeSet) # multinom Model
summary (multinomModel) # model summary
saveRDS(multinomModel, "./multinomModel.rds")
