setwd("/home/ravschoo/ResourceContention/IaaSCloudResourceContention/modeldata/m5d")
#Clear workspace 
rm(list=ls())
library(randomForest)
library(rpart)
set.seed(100)
wholeSet = read.csv("./merged.csv")

#Convert to mbs, only if they are in gbs
wholeSet$iperf <- wholeSet$iperf * 1000

str(wholeSet)

# Loading the dplyr package
library(dplyr)

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

formula = setId ~ iperf+sysbench+ycruncher+pgbench

modelRandomForest <- randomForest(formula, data=strat_data, ntree=2000, na.action=na.exclude, importance=TRUE)
modelRandomForest$importance

print(modelRandomForest)
saveRDS(modelRandomForest, "./modelRandomForest_Treated.rds")

# Importance of each predictor.
print(importance(modelRandomForest,type = 1)) 

#We are no longer using a train split
#predictions <- predict(modelRandomForest, test)

#write.table(table(predictions, test$set), "./predictions1.txt")



summary(modelRandomForest)

#plot(x = test$set , y = predictions,col="blue",pch=19,xlab="# of co-located",ylab="# of co-located", xaxt='n',yaxt='n')
#par(new=TRUE)
#plot(x = test$set  , y = comparason$set, col="red",pch=17, xlab='', ylab='', xaxt='n',yaxt='n')
#axis(1,1:48)
#axis(2,1:48)
#legend("topleft",legend=c("observed value","predicted value"),pch=c(17,19), col=c("red","blue"))
