setwd("/home/ravschoo/ResourceContention/IaaSCloudResourceContention/modeldata/m5d/OpenCloud/")
#Clear workspace 
rm(list=ls())

#load Open Cloud data
set.seed(100)
wholeSet = read.csv("./merged.csv")

# load the model
super_model <- readRDS("modelRandomForest.rds")
print(super_model)

predictions <- predict(super_model, wholeSet)
predictions

max(predictions)
min(predictions)
mean(predictions)



write.csv(predictions, "./predictions.csv")
