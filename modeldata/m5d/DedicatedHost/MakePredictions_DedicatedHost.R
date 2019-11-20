setwd("/home/ravschoo/ResourceContention/IaaSCloudResourceContention/modeldata/m5d/DedicatedHost/")
#Clear workspace 
rm(list=ls())

#load Open Cloud data
set.seed(100)
wholeSet = read.csv("./Aggregate_Summary_Dedicated_Host_11-16-2019.csv")

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
predictions_rmse <- rmse(wholeSet$setId, rounded_predictions)

#create the confusion matrix
predictions_confusion <- confusionMatrix(wholeSet$setId, rounded_predictions)

#Graph error
par(mfrow=c(1,1))
plot(super_model)

plot(rounded_predictions, wholeSet$setId, xlab="predicted", ylab="actual")
abline(a=0,b=1)


write.csv(predictions, "./predictions.csv")


