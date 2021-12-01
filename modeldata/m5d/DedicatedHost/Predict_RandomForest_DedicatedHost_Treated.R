setwd("/home/ravschoo/ResourceContention/IaaSCloudResourceContention/modeldata/m5d/DedicatedHost/")
#Clear workspace 
rm(list=ls())
library("randomForest")

#load Open Cloud data
set.seed(100)
wholeSet = read.csv("./Aggregate_Summary_Dedicated_Host_11-16-2019.csv")

# load the model
super_model <- readRDS("modelRandomForest_Treated.rds")
print(super_model)

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


predictions <- predict(super_model, strat_data)
predictions

max(predictions)
min(predictions)
mean(predictions)
sd(predictions)

#We need to round each predictions to nearest integer value
#rounded_predictions <- round(predictions)

#calculate the rmse
library("ModelMetrics")
predictions_rmse <- rmse(predictions, strat_data$setId)
predictions_rmse

metrics_mae <- mae(predictions, strat_data$setId)
metrics_mae

#create the confusion matrix
#predictions_confusion <- confusionMatrix(wholeSet$setId, rounded_predictions)

#Graph error
par(mfrow=c(1,1))
plot(super_model)

plot(predictions, strat_data$setId, xlab="Predicted # of VMs", ylab="Actual # of VMs", col="blue", main="Treated Random Forest")
abline(a=0,b=1)

par(mfrow = c(1,1))
plot(super_model$err.rate[,1], type = "l")
plot(super_model)


write.csv(predictions, "./predictions.csv")


