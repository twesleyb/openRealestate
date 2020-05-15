#!/usr/bin/env Rscript

# Load renv.
renv::load(getrd()) # NOTE: getrd() is an alias in my .Rprofile.
# Alternatively, you can use:
#renv::load("your/path/to/open-realestate/")

library(dplyr)
library(data.table)
library(tidygeocoder)

## Input Arguments.
input_data = "durham-realestate.csv"

# Path to durham realestate data.
here <- getwd()
datadir <- file.path(here,"data",input_data)

# Load the data.
dt <- data.table::fread(datadir)

## Let's look at Milan Woods.

# Subset the data.
subdivisions <- unique(dt$SUBD_DESC) # All subdivisions.
milan_woods <- subdivisions[grep("MILAN",subdivisions)] # Combine Milan Woods.
subdt <- dt %>% filter(SUBD_DESC %in% milan_woods)

# Median home price:
median_price <- formatC(median(subdt$SALE_PRICE),format='d',big.mark=',')
median_price

# Number of addresses and owners:
n_addr <- length(unique(subdt$PARCEL_ID))
n_owners <- length(unique(subdt$OWNER_NAME))

# Median size:
median_size <- median(subdt$SUM_ACRE)

# Median duration owned.
# Tidy-up dates.
date_format <- "%Y%d%m"
subdt$DATE_SOLD <- as.Date(as.character(subdt$DATE_SOLD),format=date_format)

# Median ownership.
subdt$DUR_OWN <- as.numeric(difftime(today,subdt$DATE_SOLD,units="days"))/365
median(subdt$DUR_OWN,na.rm=TRUE)



# Convert addresses to lat/lon.
# To install needed: libudunits2-dev.
# $ sudo apt-get install libudunits2-dev

# Complete addresses:
colnames(subdt)
address <- paste(subdt$street,subdt$city,subdt$zip)

subdt %>% geocode(.tbl, address, method = "census", lat = lat, long = long, ...)
geocode(.tbl, address, method = "census", lat = lat, long = long, ...)

