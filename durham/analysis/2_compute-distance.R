#!/usr/bin/env Rscript

#--------------------------------------------------------------------
## Input Arguments.
input_data = "durham-geocoded" # openRealestate/data

#--------------------------------------------------------------------
## Prepare the workspace for the analysis.
#--------------------------------------------------------------------

# Load renv.
root <- getrd() # NOTE: getrd() is an alias in my .Rprofile.
renv::load(root,quiet=TRUE) # Equivalent to load("/path/to/open-realestate/")

# Load project specific data and functions.
devtools::load_all()

# Imports:
suppressPackageStartupMessages({
	library(dplyr)
	library(HDF5Array)
	library(data.table)
})

# Load the geocoded data.
data(list=input_data) # durham

# Check, how big is the data?
message(paste("Size of durham dataset:",
	      10^-6*pryr::object_size(durham),"MB."))

# Collect long, long in a matrix.
.dm <- durham %>% dplyr::select(PARCEL_ID,long,lat) %>% 
	as.data.table() %>% as.matrix(rownames="PARCEL_ID")

# Coordinates as a list.
coordinates <- apply(.dm,1,list)

# Create an empty matrix for distances beween lat/lon points.
# THESE OPERATIONS ARE SLOW!
nrow <- ncol <- length(coordinates)
distm <- matrix(data=0,nrow=nrow,ncol=ncol)

# Coerce to HDF5Matrix
#hd_distm <- as(distm,"HDF5Matrix")

da <- DelayedArray(distm)
rownames(da) <- colnames(da) <- names(coordinates)
#h5a <- HDF5Array::HDF5Dataset(da) 

# Undirected, no self-interactions.
# THESE OPERATIONS ARE SLOW!
distm[lower.tri(distm)] <- NA

# Matrix names are PARCEL_IDs.
# THESE OPERATIONS ARE SLOW!
rownames(distm) <- colnames(distm) <- names(coordinates)

# Melt into an edge list.
# THESE OPERATIONS ARE SLOW!
x <- matrix(nrow=10,ncol=10)
rownames(x) <- colnames(x) <- c(1:10)

# Compute shortest distancee between points.
# distHaversine units defaults to meters.
# This is too slow to do on the entire set of points.
.distm <- geosphere::distm(x=.dm,fun=geosphere::distHaversine)

