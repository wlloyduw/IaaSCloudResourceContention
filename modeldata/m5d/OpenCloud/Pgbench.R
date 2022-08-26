#Set working Directory for this script and clear the working environment
setwd("/home/ravschoo/ResourceContention/IaaSCloudResourceContention/modeldata/m5d/OpenCloud/")
rm(list=ls())


pgbench <- read.table("./50x_m5d_pgbench_open_cloud_11-16-2019-14_29pm_14_45pm_us-east-1b.csv", sep=",", header=TRUE)
head(pgbench)

#Take all the instanceID string and convert them to vmid 1-50
#Since this is the open cloud data all vm ran separately on the cloud
temp_vm_id <- subset(pgbench, subset=instanceID!="")
vm_id <- factor(temp_vm_id$instanceID)
vm_ids <- as.integer(vm_id)
print(min(vm_ids))
print(max(vm_ids))
levels(vm_id)

#Now bind the list of vm ids back into our dataframe
#pgbench <- cbind(pgbench, exp_ids)
pgbench <- pgbench[pgbench$instanceID != "",]
pgbench <- cbind(pgbench, vm_ids)
tail(pgbench)
dim(pgbench)

#Write out the data we are interested in
pgbench <- pgbench[c("vm_ids","instanceID","transactions")]
colnames(pgbench) <-c("vmId", "instanceID","pgbench")

#We only want the average of each record

#for each instanceID save one average.
average <- vector()
index <- 1
for (instance in levels(pgbench$instanceID)) {
  #print(instance)
  average[index] <- mean(pgbench[pgbench$instanceID == instance, "pgbench"])
  index <- index + 1
}

average
pgbench <- data.frame(levels(pgbench$instanceID), average, rep.int(1, 50), 1:50)
colnames(pgbench) <- c("instanceID", "pgbench", "setId", "vmId")
write.csv(pgbench,"./pgbench_standardized.csv",row.names = FALSE)
