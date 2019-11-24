library(tidyverse)

data("marketing", package = "datarium")
head(marketing, 4)

model <- lm(sales ~ youtube + facebook + newspaper, data = marketing)
summary(model)
