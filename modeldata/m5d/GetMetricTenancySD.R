setwd("/home/ravschoo/ResourceContention/IaaSCloudResourceContention/modeldata/m5d")
#Clear workspace 
rm(list=ls())

set.seed(100)
wholeSet = read.csv("./merged.csv")

#Separate out each benmark into vector of vectors
pgbench <- wholeSet$pgbench
sysbench <- wholeSet$sysbench
ycruncher <- wholeSet$ycruncher
iperf <- wholeSet$iperf * 1000

sds <- data.frame(vector(), vector(), vector(), vector())
benchmarks <- c("pgbench", "sysbench", "ycruncher", "iperf")
colnames(sds) <- benchmarks
head(sds)

for (i in 1:48) {
  set <- wholeSet[wholeSet$setId == i, ]
  a <- sd(set$pgbench)
  b <- sd(set$sysbench)
  c <- sd(set$ycruncher)
  d <- sd(set$iperf)
  sds <- rbind(sds, cbind(a, b, c, d))
}

sd(wholeSet$pgbench[wholeSet$setId == 1])
sd(wholeSet$pgbench[wholeSet$setId == 2])

sd(wholeSet$sysbench[wholeSet$setId == 1])
sd(wholeSet$sysbench[wholeSet$setId == 2])

sd(wholeSet$ycruncher[wholeSet$setId == 1])
sd(wholeSet$ycruncher[wholeSet$setId == 2])

sd(wholeSet$iperf[wholeSet$setId == 1])
sd(wholeSet$iperf[wholeSet$setId == 2])
