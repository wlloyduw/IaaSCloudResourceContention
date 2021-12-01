setwd("/home/ravschoo/ResourceContention/IaaSCloudResourceContention/modeldata/m5d")
#Clear workspace 
rm(list=ls())

#I need to take it each benchmarks data set
ycruncher <- read.table("./ycruncher_standardized.csv", sep=",", header=TRUE)
sysbench <- read.table("./sysbench_standardized.csv", sep=",", header=TRUE)
pgbench <- read.table("./pgbench_standardized.csv", sep=",", header=TRUE)
iperf <- read.table("./iperf_standardized.csv", sep=",", header=TRUE)

#Take just 3 observations for each set and vid
new_sysbench <- data.frame(sysbench=vector(), setId=vector(), vmId=vector())
for (setid in 0:47) {
  for (vmid in 1:48) {
    #for each set and vm combination we need 3 observations
    result <- sysbench[(sysbench$setId == setid & sysbench$vmId == vmid), ][1:3, ]
    result <- na.omit(result)
    result$sysbench <- as.numeric(gsub("s", "", unlist(result$sysbench)))
    new_sysbench <- rbind(new_sysbench, result)
  }
}

new_ycruncher <- data.frame(ycruncher=vector(), setId=vector(), vmId=vector())
for (setid in 0:47) {
  for (vmid in 1:48) {
    #for each set and vm combination we need 3 observations
    result <- ycruncher[(ycruncher$setId == setid & ycruncher$vmId == vmid), ][1:3, ]
    result <- na.omit(result)
    new_ycruncher <- rbind(new_ycruncher, result)
  }
}

new_iperf <- data.frame(iperf=vector(), setId=vector(), vmId=vector())
for (setid in 1:48) {
  for (vmid in 1:48) {
    #for each set and vm combination we need 3 observations
    result <- iperf[(iperf$setId == setid & iperf$vmId == vmid), ][1:3, ]
    result <- na.omit(result)
    new_iperf <- rbind(new_iperf, result)
  }
}

#For data sets that have setid of 0 to 47, convert this to 1 - 48.
#The set id also tells us how many vms ran during this set.


new_sysbench$setId <- new_sysbench$setId * -1 + 48
new_sysbench <- new_sysbench[order(new_sysbench$setId), ]

#Notice that as of now the vmids are not in the right order.  
#Should start with 1 and go consecutively, will fix later.
print(head(new_sysbench))

#This data set looks good already
print(head(new_iperf))

new_ycruncher$setId <- new_ycruncher$setId * -1 + 48
new_ycruncher <- new_ycruncher[order(new_ycruncher$setId), ]

print(head(new_ycruncher))

pgbench$setId <- pgbench$setId * -1 + 48
pgbench <- pgbench[order(pgbench$setId), ]

print(head(pgbench))

#Now fix the vmids
pgbench$vmId <- new_iperf$vmId
new_sysbench$vmId <- new_iperf$vmId
new_ycruncher$vmId <- new_iperf$vmId

#All data sets should have same dimensions
print(dim(new_iperf))
print(dim(pgbench))
print(dim(new_sysbench))
print(dim(new_ycruncher))

#Put all data into a dataframe 
globalMerged = data.frame()
for (set in 1:48) {
  for (vm in 1:set) {
    a = new_iperf[new_iperf$setId == set & new_iperf$vmId == vm,] 
    b = new_sysbench[new_sysbench$setId == set & new_sysbench$vmId == vm,]
    c = new_ycruncher[new_ycruncher$setId == set & new_ycruncher$vmId == vm,]
    d = pgbench[pgbench$setId == set & pgbench$vmId == vm,]
    merged = cbind(a["i_perf"],b["sysbench"],c["yCruncher"],d["pgbench"],rep.int(set, 3), rep.int(vm, 3))
    globalMerged = rbind(globalMerged, merged)
    
  }
}

colnames(globalMerged)[colnames(globalMerged)=="rep.int(set, 3)"] <- "set"
colnames(globalMerged)[colnames(globalMerged)=="rep.int(vm, 3)"] <- "vm"

#write it out as merged.csv.
write.csv(globalMerged,"./merged.csv",row.names=FALSE, col.names=FALSE)
