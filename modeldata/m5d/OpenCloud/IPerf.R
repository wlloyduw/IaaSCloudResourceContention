#Set working Directory for this script and clear the working environment
setwd("/home/ravschoo/ResourceContention/IaaSCloudResourceContention/modeldata/m5d/OpenCloud/")
rm(list=ls())

iperf <- read.table("./iperf.csv", sep=",", header=TRUE)
head(iperf)

#Take all the instanceID string and convert them to vmid 1-50
#Since this is the open cloud data all vm ran separately on the cloud
temp_vm_id <- subset(iperf, subset=instanceID!="")
vm_id <- factor(temp_vm_id$instanceID)
vm_ids <- as.integer(vm_id)
print(min(vm_ids))
print(max(vm_ids))
levels(vm_id)

#Standardize MBS and GBS and get rid of this string
#On the raw data this shows a mixture of GBS and MBS.
gb <- "Gbits/sec"
mb <- "Mbits/sec"
print(iperf$bandwidthUpload[50:100])

#Convert gigabytes to megabytes
new_upload = vector()
index <- 1
for (i in iperf$bandwidthUpload) {
  num <- i
  if (grepl(gb, num)) {
    num <- as.numeric(gsub(gb, "", num))
    new_upload[index] <- num
  } else {
    num <- as.numeric(gsub(mb, "", num))
    num <- num / 1000
    new_upload[index] <- num
  }
  index <- index + 1
}

#This prints out the standardized numbers
print(new_upload[50:100])

#Now do same thing with download and combine them.
new_download = vector()
index <- 1
for (i in iperf$bandwitdhDownload) {
  num <- i
  if (grepl(gb, num)) {
    num <- as.numeric(gsub(gb, "", num))
    new_download[index] <- num
  } else {
    num <- as.numeric(gsub(mb, "", num))
    num <- num / 1000
    new_download[index] <- num
  }
  index <- index + 1
}
new_bandwidth <- new_upload + new_download

#and put the new total bandwidth into the dataframe
iperf$Total <- new_bandwidth
head(iperf)
tail(iperf)

levels(iperf$instanceID)

means = vector()
index = 1
for (instanceId in levels(iperf$instanceID)) {
  totals <- iperf[iperf$instanceID == instanceId, "Total"]
  means[index] <- mean(totals)
  index <- index + 1
  #print(instanceId)
}

#get rid of two na values, replace with mean of all means.
print(means)
means[which(is.na(means))] <- mean(means, na.rm=TRUE) 
print(means)

#Create vector that is repeats every value of means 10 times
means_500 <- rep(means, 10)
means_500[c(1, 51, 101, 151)]

means_500 <- vector()
for (num in means) {
  means_500 <- rbind(means_500, rep(num, 10))
}
means_500 <- as.vector(means_500)
means_500[c(1, 51, 101, 151)]

length(means_500)

setId <- rep.int(1, 500)
vmId <- rep(1:50, 10)
length(vmId)

iperf <- data.frame(means_500, setId, vmId)
iperf[1:51,]

#########################################################################################
#Give this data to Delvin and then continue with your data manipulation

#Write out the data we are interested in
colnames(iperf) <-c("iperf","setId","vmId")
write.csv(iperf,"./iperf_standardized.csv",row.names = FALSE)
