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

# Using sample_frac to create 70 - 30 slipt into test and train
#train <- sample_frac(wholeSet, 0.9)
#sample_id <- as.numeric(rownames(train)) # rownames() returns character so as.numeric
#test <- wholeSet[-sample_id,]

formula = setId ~ iperf+sysbench+ycruncher+pgbench

modelRandomForest <- randomForest(formula, data=wholeSet, ntree=2000, na.action=na.exclude, importance=TRUE)

print(modelRandomForest)
saveRDS(modelRandomForest, "./modelRandomForest.rds")


