#Set working Directory for this script and clear the working environment
setwd("/home/ravschoo/ResourceContention/IaaSCloudResourceContention/modeldata/m5d/OpenCloud/")
rm(list=ls())

ycruncher <- read.table("./50x_m5d_y-cruncher_open_cloud_11-16-2019-14_21pm_14_26pm_us-east-1b.csv", sep=",", header=TRUE)
head(ycruncher)

#Take all the instanceID string and convert them to vmid 1-50
#Since this is the open cloud data all vm ran separately on the cloud
temp_vm_id <- subset(ycruncher, subset=instanceID!="")
vm_id <- factor(temp_vm_id$instanceID)
vm_ids <- as.integer(vm_id)
print(min(vm_ids))
print(max(vm_ids))
levels(vm_id)

#Now bind the list of vm ids back into our dataframe
ycruncher <- ycruncher[ycruncher$instanceID != "",]
ycruncher <- cbind(ycruncher, vm_ids)
head(ycruncher)
tail(ycruncher)

#There are exactly as many observations as there should be: 50 * 10 = 500
dim(ycruncher)

#Write out the data we are interested in

ycruncher <- ycruncher[c("vm_ids","instanceID","computationTime")]
colnames(ycruncher) <-c("vmId", "instanceID","ycruncher")

#for each instanceID save one average.
average <- vector()
index <- 1
for (instance in levels(ycruncher$instanceID)) {
  #print(instance)
  average[index] <- mean(ycruncher[ycruncher$instanceID == instance, "ycruncher"])
  index <- index + 1
}

average
ycruncher <- data.frame(levels(ycruncher$instanceID), average, rep.int(1, 50), 1:50)

colnames(ycruncher) <-c("instanceID","ycruncher", "setId", "vmId")
write.csv(ycruncher,"./ycruncher_standardized.csv",row.names = FALSE)
