#!/usr/bin/env Rscript

## Input Arguments.
input_data = "durham-realestate.csv"

# Load renv.
renv::load(getrd()) # NOTE: getrd() is an alias in my .Rprofile.
# Alternatively, you can use:
#renv::load("your/path/to/open-realestate/")

# Imports:
suppressPackageStartupMessages({
	library(dplyr)
	library(data.table)
	#library(tidygeocoder)
})

# Path to durham realestate data.
here <- getwd()
datadir <- file.path(here,"data",input_data)

# Load the data.
durham <- data.table::fread(datadir)

# All neighborhood subdivisions.
subdivisions <- unique(durham$SUBD_DESC)
n_subd <- length(subdivisions)
message(paste("Number of subdivisions:",formatC(n_subd,big.mark=",")))

# Fix-up dates.
date_format <- "%Y%d%m"
durham$DATE_SOLD <- as.Date(as.character(durham$DATE_SOLD),format=date_format)

# Function to calculate duration owned in years.
dur_owned <- function(col.id,today=Sys.Date()) {
	years_owned <- as.numeric(difftime(today,col.id,units="days"))/365
	return(years_owned)
}

# Summarize subdivisions.
dt <- durham %>% group_by(SUBD_DESC) %>% 
	summarize(median_price = median(SALE_PRICE),
		  n_parcels = length(unique(PARCEL_ID)),
		  median_size = median(SUM_ACRE),
		  median_dur_owned = median(dur_owned(DATE_SOLD),na.rm=TRUE))

fwrite(dt,"temp.csv")
