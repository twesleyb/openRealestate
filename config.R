#!/usr/bin/env Rscript

# OPTIONS ---------------------------------------------------------------------

# the project's root directory:
root = getwd() # its assumed that this script is in the projects root dir

# project dependencies:
imports = c("data.table","dplyr")

# load renv -------------------------------------------------------------------

if (!dir.exists(file.path(root,"renv"))) {
} else {
	renv::load(root,quiet=TRUE)
}

# utility functions ------------------------------------------------------------

str_within_paren <- function(string) { 
	# extract strings from within parentheses, e.g.
	# > str_within_paren("foo (bar) man (biz)")
	# [1] "bar" "biz"
	regex = "(?<=\\().*?(?=\\))"
	matches <- regmatches(string, gregexpr(regex, string, perl=T))[[1]]
	return(matches)
}

load_imports <- function(imports=NULL) {
	# load imports
	do.call(library,as.list(imports))
}

load_namespace <- function(myfile="NAMESPACE") {
	namespace <- readLines(myfile)
	imports <- str_within_paren(paste(namespace,collapse=" "))
	if (length(imports) == 0) { 
		warning("There are no imports declared in NAMESPACE." ) 
	} else {
		do.call(library,as.list(imports))
	}
}

load_namespace()

load_project <- function(root = getwd, "data" = TRUE, "R" = TRUE) {
	# load project's functions and data from the R/ and data/ directories
	# NOTE: only loads .rda and .R files
	#
	data_files <- list.files(file.path(root,"data"),pattern=".rda") 
	R_files <- list.files(file.path(root,"R"),pattern=".R")
	#
	for (dfile in data_files) {
		message(paste("loaded dataset:",tools::file_path_sans_ext(dfile)))
		load(file = file.path(root,"data",dfile))
	}
	#
	if (length(R_files) > 0) {
		message(paste("Importing functions from:",file.path(root,"R")))
		for (Rfile in R_files) {
			source(file = file.path(root,"data",Rfile))
		}
	}
}

# main ------------------------------------------------------------------------

main <- function() {

	.env <- new.env()

	load_renv()    # load reproducible R environment

	load_project() # load functions (R/) and data (data/)

	load_imports() # load any dependencies declared in NAMESPACE

	return attach(.env,warn.conflicts=FALSE)
}
