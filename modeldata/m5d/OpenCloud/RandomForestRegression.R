setwd("/home/ravschoo/ResourceContention/IaaSCloudResourceContention/modeldata/m5d")
#Clear workspace 
rm(list=ls())
library(randomForest)
library(rpart)
wholeSet = read.csv("./merged.csv")

str(wholeSet)

# Loading the dplyr package
library(dplyr)

# Using sample_frac to create 70 - 30 slipt into test and train
train <- sample_frac(wholeSet, 0.9)
sample_id <- as.numeric(rownames(train)) # rownames() returns character so as.numeric
test <- wholeSet[-sample_id,]

formula = set~iperf+sysbench+ycruncher+pgbench

modelRandomForest <- randomForest(
  formula,
  data=train)

print(modelRandomForest)

# Importance of each predictor.
print(importance(modelRandomForest,type = 2)) 

predictions <- predict(modelRandomForest, test)

write.table(table(predictions, test$set), "./predictions1.txt")

summary(modelRandomForest)

plot(x = test$set , y = predictions,col="blue",pch=19,xlab="# of co-located",ylab="# of co-located", xaxt='n',yaxt='n')
par(new=TRUE)
plot(x = test$set  , y = comparason$set, col="red",pch=17, xlab='', ylab='', xaxt='n',yaxt='n')
axis(1,1:48)
axis(2,1:48)
legend("topleft",legend=c("observed value","predicted value"),pch=c(17,19), col=c("red","blue"))
