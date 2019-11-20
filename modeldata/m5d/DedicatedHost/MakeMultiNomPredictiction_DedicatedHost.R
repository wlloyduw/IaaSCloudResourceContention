setwd("/home/ravschoo/ResourceContention/IaaSCloudResourceContention/modeldata/m5d/DedicatedHost/")
#Clear workspace 
rm(list=ls())

#load Open Cloud data
set.seed(100)
wholeSet = read.csv("./Aggregate_Summary_Dedicated_Host_11-16-2019.csv")

# load the model
super_model <- readRDS("multinomModel.rds")
print(super_model)

predictions <- predict(super_model, wholeSet)
predictions

predicted_scores <- predict (super_model, wholeSet, "probs")
predicted_scores

predicted_class <- predict (super_model, wholeSet)
table(predicted_class, wholeSet$setId)

plot(x = wholeSet$setId , y = predicted_class,col="blue",pch=19,xlab="set observed",ylab="set predicted")
axis(1,1:48,1:48,cex.axis=0.8)
axis(2,1:148,1:48,cex.axis=0.8)
par(new=TRUE)
lines(x = range(1:48) , y = range(1:48),col="red")
legend("topright",legend=c("observed value","predicted value"),pch=19, col=c("red","blue"))

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


write.csv(predictions, "./predictions.csv")


