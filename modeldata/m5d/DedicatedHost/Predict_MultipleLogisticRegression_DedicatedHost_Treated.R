setwd("/home/ravschoo/ResourceContention/IaaSCloudResourceContention/modeldata/m5d/DedicatedHost/")
#Clear workspace 
rm(list=ls())

set.seed(100)
wholeSet = read.csv("./Aggregate_Summary_Dedicated_Host_11-16-2019.csv")

library("ModelMetrics")
library(nnet)
library(splitstackshape)
# load the model
mlr_model <- readRDS("./model_mlr_treated.rds")
print(mlr_model)
summary (mlr_model) # model summary

#Statify a new dataset so that we have same number of samples for each vm tenancy.
strat_data <- stratified(indt=wholeSet, group=c("setId"), size=3)

#Scale data
#Scale data to make it normally distributed
#iperf_log <- log(strat_data$iperf)
#summary(iperf_log)
iperf_scaled <- scale(strat_data$iperf)
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


predictions <- predict(mlr_model, strat_data)
predictions

max(predictions)
min(predictions)
mean(predictions)
sd(predictions)


#calculate the rmse

predictions_rmse <- rmse(predictions, strat_data$setId)
predictions_rmse

metrics_mae <- mae(predictions, strat_data$setId)
metrics_mae

#Calculate the absolute error for each data point/prediction
abs_error <- vector()
for (i in 1:length(predictions)) {
  abs_error[i] <- abs(predictions[i] - strat_data$setId[i])
}

#This should give us the mean of the abs error for predictions that should be 48 vms.
#mean(abs_error[1:3])
#sum(abs_error[1:3]) / 3

#write.csv(abs_error, "./treated_mlr_abs_error_no_iperf.csv")

#plot(predictions, strat_data$setId, xlab="Predicted # of VMs", ylab="Actual # of VMs", col="blue", main="Treated MLR")
#abline(a=0,b=1)

#Match bad predictions with instance ids and get predictors
bad_indices <- abs_error > 4

strat_data[bad_indices,]

## Lets look at the raw values.
strat_data1 <- stratified(indt=wholeSet, group=c("setId"), size=3)
strat_data1[bad_indices,]

good_data <- strat_data[!bad_indices]

good_predictions <- predict(mlr_model, good_data)

max(good_predictions)
min(good_predictions)
mean(good_predictions)
sd(good_predictions)

good_predictions_rmse <- rmse(good_predictions, good_data$setId)
good_predictions_rmse

good_metrics_mae <- mae(good_predictions, good_data$setId)
good_metrics_mae
