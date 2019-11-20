setwd("/home/ravschoo/ResourceContention/IaaSCloudResourceContention/modeldata/m5d/DedicatedHost/")
#Clear workspace 
rm(list=ls())

#load Open Cloud data
set.seed(100)
wholeSet = read.csv("./merged_11-16-2019 .csv")

# load the model
super_model <- readRDS("modelRandomForest.rds")
print(super_model)

predictions <- predict(super_model, wholeSet)
predictions

max(predictions)
min(predictions)
mean(predictions)
sd(predictions)

#We need to round each predictions to nearest integer value
rounded_predictions <- round(predictions)

#calculate the rmse
library("ModelMetrics")
predictions_rmse <- rmse(wholeSet$setId, predictions)
predictions_rmse

#create the confusion matrix
predictions_confusion <- confusionMatrix(wholeSet$setId, rounded_predictions)

#Graph error
par(mfrow=c(1,1))
plot(super_model)

plot(predictions, wholeSet$setId, xlab="predicted", ylab="actual", col="blue")
abline(a=0,b=1)


write.csv(predictions, "./predictions_merged.csv")


