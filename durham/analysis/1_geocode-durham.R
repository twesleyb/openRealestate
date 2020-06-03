#!/usr/bin/env Rscript

# 1. loads the data saved as csv from python.
# 2. save the data as an rda object in openRealestate/data.
# 3. geocode addresses with twesleyb/tidygeocoder.
# 4. save the data as rda.

#--------------------------------------------------------------------
## Input Arguments.
input = "durham/data/durham-realestate.csv" 
	
#--------------------------------------------------------------------
## Prepare the workspace for the analysis.
#--------------------------------------------------------------------

# Load renv.
root <- getrd() # NOTE: getrd() is an alias in my .Rprofile.
renv::load(root,quiet=TRUE) # Equivalent to load("/path/to/open-realestate/")

# Load project specific data and functions.
devtools::load_all()

# Additional imports:
suppressPackageStartupMessages({
	library(dplyr)
	library(data.table)
	library(tidygeocoder) # My fork: twesleyb/tidygeocoder
})

# Load the data -- this is the durham data scraped from
# durham gomaps using python.
datadir <- file.path(root,input)
durham <- data.table::fread(datadir)

#--------------------------------------------------------------------
## Save durham data as rda.
#--------------------------------------------------------------------

# Save the data as rda.
datadir <- file.path(root,"data","durham.rda")
if (file.exists(datadir)) { 
	stop("Warning: overwrite data?")
	save(durham,file=datadir,version=2)
}

#--------------------------------------------------------------------
## Geocode the addresses.
#--------------------------------------------------------------------

# Create column with complete parcel address:
# PARCEL_ADDR = NUMBER STREET CITY STATE ZIP
durham$PARCEL_ADDR <- paste(trimws(durham$SITE_ADDR),
			    "Durham NC","OWZIPA")

# Encode addresses as lat/lon with tidy geocoder.
start <- Sys.time()
message(paste("\nStarting geocoding at:",start))
durham <- durham %>% tidygeocoder::geocode(ADDR)

# Time to complete:
now <- Sys.time()
dt <- difftime(now,start)
message(paste0("\nCompleted geocoding at: ", now))
message(paste0("\nTime to encode ", 
	       formatC(nrow(durham), big.mark=","), " rows: ",
	       round(dt,3), " ", attr(dt,"units"),"."))

#--------------------------------------------------------------------
## Save geocoded data to file.
#--------------------------------------------------------------------

datadir <- file.path(root,city,"data","durham-geocoded.rda")
save(durham,file=datadir,version=2)

message("done!")
