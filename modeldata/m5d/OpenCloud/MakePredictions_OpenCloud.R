setwd("/home/ravschoo/ResourceContention/IaaSCloudResourceContention/modeldata/m5d/OpenCloud/")
#Clear workspace 
rm(list=ls())

library("randomForest")

#load Open Cloud data
set.seed(100)
wholeSet = read.csv("./merged.csv")
wholeSet$iperf <- wholeSet$iperf * 1000

# load the model
super_model <- readRDS("modelRandomForest.rds")
print(super_model)

predictions_open <- predict(super_model, wholeSet)
predictions_open

max(predictions_open)
min(predictions_open)
mean(predictions_open)
sd(predictions_open)

write.csv(predictions_open, "./predictions_openCloud.csv")
