#!/usr/bin/env Rscript

# Load renv.
renv::load(getrd()) # NOTE: getrd() is an alias in my .Rprofile.
# Alternatively, you can use:
#renv::load("your/path/to/open-realestate/")

# Imports:
suppressPackageStartupMessages({
	library(dplyr)
	library(data.table)
	library(TBmiscr)
	#library(tidygeocoder)
})

# Path to durham realestate data.
data_file <- "durham-realestate.csv"
here <- getwd()
myfile <- file.path(here,"data",data_file)

# Load the data.
durham <- data.table::fread(myfile)

# All neighborhood subdivisions.
subdivisions <- unique(durham$SUBD_DESC)
n_subd <- length(subdivisions)
message(paste("Number of subdivisions:",formatC(n_subd,big.mark=",")))

# Fix-up dates.
date_format <- "%Y%d%m"
durham$DATE_SOLD <- as.Date(as.character(durham$DATE_SOLD),format=date_format)

# A function that calculates the duration owned in years.
duration_owned <- function(date_sold,
			   units=c("days","months","years"),today=Sys.Date()) {
	days_owned <- as.numeric(difftime(today,date_sold,units="days"))
	time_owned <- switch(units[1],
				 days = days_owned,
			         months = days_owned/30,
			         years = days_owned/365)
	return(time_owned)
}

# Parcel IDs are truly unique.
#check <- any(duplicated(durham$PARCEL_ID))

# Calculate duration owned for every parcel.
durham$DUR_OWNED <- duration_owned(durham$DATE_SOLD,units="years")

# In 2020, it appears that the formattting of dates changes.
# It appears that the formatting of dates switched from y-d-m to y-m-d. So we
# need to change it back to be consistent.
subdat <- durham %>% filter(DUR_OWNED < 0)
date_format <- "%Y-%d-%m"
subdat$DATE_SOLD <- as.Date(as.character(subdat$DATE_SOLD),format=date_format)
subdat$DUR_OWNED <- duration_owned(subdat$DATE_SOLD,units="years")
idx <- match(subdat$PARCEL_ID,durham$PARCEL_ID)
durham[,"DUR_OWNED"][idx] <- subdat$DUR_OWNED

# Check, minimum duration owned should be positive.
min(durham$DUR_OWNED,na.rm=TRUE)

# Summarize subdivisions.
dt <- durham %>% group_by(SUBD_DESC) %>% 
	summarize(median_price = median(SALE_PRICE),
		  n_parcels = length(unique(PARCEL_ID)),
		  median_size = median(SUM_ACRE),
		  median_dur_owned = median(DUR_OWNED))

# Minimum duration owned:
min(dt$median_dur_owned,na.rm=TRUE)

# Drop columns that are all na.
drop <- which(apply(apply(durham,2,is.na),2,all))
keep <- which(colnames(durham) %notin% names(drop))
durham <- durham %>% select(all_of(keep))

# Tidy the data?
tidy_dt <- durham %>% reshape2::melt(id.var="PARCEL_ID")

# Save to file.
fwrite(dt,"temp.csv")
