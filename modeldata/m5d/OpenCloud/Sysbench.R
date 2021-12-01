#Set working Directory for this script and clear the working environment
setwd("/home/ravschoo/ResourceContention/IaaSCloudResourceContention/modeldata/m5d/OpenCloud/")
rm(list=ls())

sysbench <- read.table("./50x_m5d_sysbench_open_cloud_11-16-2019-14_15pm_14_19pm_us-east-1b.csv", sep=",", header=TRUE)
head(sysbench)

#Take all the instanceID string and convert them to vmid 1-50
#Since this is the open cloud data all vm ran separately on the cloud
temp_vm_id <- subset(sysbench, subset=instanceID!="")
vm_id <- factor(temp_vm_id$instanceID)
vm_ids <- as.integer(vm_id)
print(min(vm_ids))
print(max(vm_ids))
levels(vm_id)

#Now bind the list of vm ids back into our dataframe
sysbench <- sysbench[sysbench$instanceID != "",]
sysbench <- cbind(sysbench, vm_ids)
tail(sysbench)
dim(sysbench)

#Write out the data we are interested in
sysbench <- sysbench[, c("vm_ids","instanceID","total.time")]
sysbench$setId <- rep.int(1, 50)
sysbench$total.time <- as.numeric(gsub("s", "", unlist(sysbench$total.time)))
colnames(sysbench) <- c("vmId", "instanceID", "sysbench", "setId")

#for each vmId save one average.
average <- vector()
index <- 1
for (instance in levels(sysbench$instanceID)) {
  average[index] <- mean(sysbench[sysbench$instanceID == instance, "sysbench"])
  index <- index + 1
}

average
sysbench <- data.frame(levels(sysbench$instanceID), average, rep.int(1, 50), 1:50)


#Write out the data we are interested in

colnames(sysbench) <-c("instanceID","sysbench", "setId", "vmId")
write.csv(sysbench,"./sysbench_standardized.csv",row.names = FALSE)
