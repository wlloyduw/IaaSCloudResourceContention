setwd("/home/ravschoo/ResourceContention/IaaSCloudResourceContention/modeldata/m5d/OpenCloud/")
#Clear workspace 
rm(list=ls())

#I need to take it each benchmarks data set
ycruncher <- read.table("./ycruncher_standardized.csv", sep=",", header=TRUE)
sysbench <- read.table("./sysbench_standardized.csv", sep=",", header=TRUE)
pgbench <- read.table("./pgbench_standardized.csv", sep=",", header=TRUE)
iperf <- read.table("./iperf_standardized.csv", sep=",", header=TRUE)



#All data sets should have same dimensions
print(dim(iperf))
print(dim(pgbench))
print(dim(sysbench))
print(dim(ycruncher))

#Put all data into a dataframe 
globalMerged = data.frame()

for (vm in 1:50) {
  a = iperf[iperf$vmId == vm,] 
  b = sysbench[sysbench$vmId == vm,]
  c = ycruncher[ycruncher$vmId == vm,]
  d = pgbench[pgbench$vmId == vm,]
  #Get a hold of th instance id
  #Map predictions to instances
  merged = cbind(a["iperf"],b["sysbench"],c["ycruncher"],d["pgbench"],1, vm)
  globalMerged = rbind(globalMerged, merged)
}

#woops somehow forgot to get rid of the s(seconds) in sysbench
#globalMerged$sysbench <- as.numeric(gsub("s", "", unlist(globalMerged$sysbench)))

#write it out as merged.csv.
write.csv(globalMerged,"./merged.csv",row.names=FALSE, col.names=FALSE)
