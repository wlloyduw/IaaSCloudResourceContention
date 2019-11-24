setwd("/home/ravschoo/ResourceContention/IaaSCloudResourceContention/modeldata/m5d/DedicatedHost/")
#Clear workspace 
rm(list=ls())

library(tidyverse)

#load Dedicated Host data
set.seed(100)
wholeSet = read.csv("./Aggregate_Summary_Dedicated_Host_11-16-2019.csv")

# load the model
mlr_model <- readRDS("model_mlr.rds")
print(mlr_model)

predictions <- predict(mlr_model, wholeSet$setId)
predictions

max(predictions)
min(predictions)
mean(predictions)
sd(predictions)
