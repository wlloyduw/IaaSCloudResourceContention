#Clear workspace 
rm(list=ls())

setwd("/home/ravschoo/ResourceContention/IaaSCloudResourceContention/modeldata/m5d/DedicatedHost/")


wholeSet = read.csv("./Aggregate_Summary_Dedicated_Host_11-16-2019.csv")

library(nnet)
# load the model
mlr_model <- readRDS("./model_mlr_unstrat.rds")
print(mlr_model)
summary (mlr_model) # model summary

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


predictions <- predict(mlr_model, wholeSet)
predictions

max(predictions)
min(predictions)
mean(predictions)
sd(predictions)


#calculate the rmse
library("ModelMetrics")
predictions_rmse <- rmse(predictions, wholeSet$setId)
predictions_rmse

metrics_mae <- mae(predictions, wholeSet$setId)
metrics_mae

#Calculate the absolute error for each data point/prediction
abs_error <- vector()
for (i in 1:length(predictions)) {
  abs_error[i] <- abs(predictions[i] - wholeSet$setId[i])
}

#This should give us the mean of the abs error for predictions that should be 48 vms.
#mean(abs_error[1:48])

#write.csv(abs_error, "./unstratified_abs_error.csv")


plot(predictions, wholeSet$setId, xlab="Predicted # of VMs", ylab="Actual # of VMs", col="blue", main="MLR")
abline(a=0,b=1)

