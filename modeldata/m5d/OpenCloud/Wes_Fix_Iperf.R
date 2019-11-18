#Set working Directory for this script and clear the working environment
setwd("/home/ravschoo/ResourceContention/IaaSCloudResourceContention/modeldata/m5d/OpenCloud/")
rm(list=ls())

iperf <- read.table("./Wes_Data_Fix_Iperf.csv", sep=",", header=TRUE)
head(iperf)


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
iperf$Total[which(is.na(iperf$Total))] <- mean(means, na.rm=TRUE) 

iperf$Total

head(iperf)


#########################################################################################
#Give this data to Delvin and then continue with your data manipulation

#Write out the data we are interested in
iperf <- iperf[, c("instanceID","Total","setId","vmId")]
iperf$setId <- rep.int(1, 50)
#for each vmId save one average.
average <- vector()
index <- 1
for (instance in levels(iperf$instanceID)) {
  average[index] <- mean(iperf[iperf$instanceID == instance, "Total"])
  index <- index + 1
}

average
iperf <- data.frame(levels(iperf$instanceID), average, rep.int(1, 50), 1:50)

colnames(iperf) <-c("instanceID","iperf","setId","vmId")
write.csv(iperf,"./iperf_standardized.csv",row.names = FALSE)
