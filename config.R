#!/usr/bin/env Rscript

## OPTIONS ------------------------------------------------------------

# everything is relative to projects root directory
root = "~/projects/openRealestate"

## utility functions --------------------------------------------------
# functions that do all the work

load_imports <- function(imports=NULL) {
	# wrapper around R::library
	import <- function(lib) {
		suppressPackageStartupMessages(library(lib))
	}
	do.call(import,as.list(imports))
}


is_installed <- function(package) {
	# check if a package is installed
	installed <- rownames(installed.packages())
	return(package %in% installed)
}


load_renv <- function(root=getwd(),quiet=TRUE) {
	# load renv given path to project root dir containing renv/
	if (!dir.exists(file.path(root,"renv"))) {
		# renv does not exist
		if (!is_installed("renv")) {
			stop(paste("renv is not installed.\n",
				   "Please install renv",
				   "to manage R dependencies.")) }
	} else {
		renv::load(project=root,...)
	}
}


str_within_paren <- function(string) {
	# extract strings from within parentheses, e.g.
	# > str_within_paren("foo (bar) man (biz)")
	# [1] "bar" "biz"
	re = "(?<=\\().*?(?=\\))"
	matches <- regmatches(string, gregexpr(re, string, perl=T))[[1]]
	return(matches)
}


load_namespace <- function(root, myfile="NAMESPACE") {
	# load imports delclared in NAMESPACE file
	namespace <- readLines(myfile)
	imports <- str_within_paren(paste(namespace,collapse=" "))
	if (length(imports) == 0) {
	#	warning("There are no imports declared in NAMESPACE." )
	} else {
		do.call(library,as.list(imports))
	}
}

load_project <- function(root=getwd(),
			 datadir = file.path(root,"data"),
			 funcdir = file.path(root,"R"),
			 quiet = TRUE) {
	# load project's functions and data from the R/ and data/ dirs
	# NOTE: only loads .rda and .R files
	data_files <- list.files(datadir, pattern=".rda")
	R_files <- list.files(funcdir, pattern=".R")
	#
	for (dfile in data_files) {
		if (!quiet) {
			message(paste("Loaded dataset:",
				      tools::file_path_sans_ext(dfile)))
		}
		load(file = file.path(root,"data",dfile))
	}
	#
	if (length(R_files) > 0) {
		message(paste("Importing functions from:",
			      file.path(root,"R")))
		for (Rfile in R_files) {
			source(file = file.path(root,"data",Rfile))
		}
	}
}


# main --------------------------------------------------------------

.env <- new.env()

load_renv(root)      # load reproducible R environment

load_project(root)   # load functions (R/) and data (data/)

load_namespace(root) # load any dependencies declared in NAMESPACE

# attach these imports to an environment which is loaded by
# source("config.R")
attach(.env,warn.conflicts=FALSE)
