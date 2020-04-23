# Rprofile.

#--------------------------------------------------------------------
## Functions:
#--------------------------------------------------------------------

# Define a function that installs with INSTALL_opts = "--no-lock"
install.nolock <- function(package){
	install.packages(package,INSTALL_opts="--no-lock")
	}

# Define a function to get root directory.
getrd <- function(dpattern = ".git", fpattern = NULL, max_trys = 5) {
  here <- getwd()
  if (!is.null(dpattern) & is.null(fpattern)) {
    # Loop to search for directory pattern.
    root <- FALSE
    i <- 0
    while (!root & i < max_trys) {
      root <- dpattern %in% basename(list.dirs(here, recursive = FALSE))
      if (!root) {
        here <- dirname(here)
        i <- i + 1
      }
    }
  } else if (!is.null(fpattern) & is.null(dpattern)) {
    # Loop to search for file pattern.
    root <- FALSE
    i <- 0
    while (!root & i < max_trys) {
      root <- fpattern %in% list.files(here)
      if (!root) {
        here <- dirname(here)
        i <- i + 1
      }
    }
  } else {
    stop("Please provide a file pattern or directory pattern.")
  }
  # Check if root was found.
  if (root) {
    root_directory <- here
    return(root_directory)
  } else {
    stop(paste("Unable to find root directory after", max_trys, "tries."))
  }
}

#--------------------------------------------------------------------
## Startup.
#--------------------------------------------------------------------
# What to do upon startup.

# Note: startup messages are disable by bash alias: R --silent.
# This just prints the current version of R when launching an 
# interactive session.
.First <- function() {
	# Print R version.
	if(interactive()) {
		cat(R.version$version.string,"\n") 
	}
	# Check if an renv exists in root, and source it.
	#root <- getrd()
	#renvdir <- list.files(root,pattern="renv$",full.names=TRUE)
	#if ("activate.R" %in% list.files(renvdir)) {
	#	cat(file.path(root,"renv","activate"))
	#	source(file.path(root,"renv","activate.R"))
	#}
}

#--------------------------------------------------------------------
## Shutdown.
#--------------------------------------------------------------------
# Control behavior of R when quitting.

#.Last <- function() {
#	renv_available <- "renv" %in% rownames(installed.packages())
#	if (interactive() & renv_available) { renv::snapshot() }
#}

# Don't prompt me to save when quiting.
utils::assignInNamespace("q", function(save = "no", status = 0, runLast = TRUE){
				 .Internal(quit(save, status, runLast)) }, "base")    
utils::assignInNamespace("quit", function(save = "no", status = 0, runLast = TRUE) {
				 .Internal(quit(save, status, runLast)) }, "base")

#--------------------------------------------------------------------
## Use tar.
#--------------------------------------------------------------------
Sys.setenv(TAR = "/bin/tar")

#--------------------------------------------------------------------
## Set default CRAN mirror.
#--------------------------------------------------------------------

#local({
#	r <- getOption("repos")
#	r["CRAN"] <- "http://cran.cnr.berkeley.edu/"
#	options(repos = r)
#})

#--------------------------------------------------------------------
## Some hidden functions.
#--------------------------------------------------------------------

# Need to declare an environment to attach the functions.
.env <- new.env()

# Create functions that can be called without parentheses.
print.command <- function (cmd) {
	default.args <- attr(cmd, "default.args")
  if (length(default.args) == 0L) {
	  default.args <- list()
  }
  res <- do.call(cmd, default.args, envir = parent.frame(2))
  if (attr(cmd, "print_result")) { 
	  print(res)
  }
  invisible(NULL)
}

make_command <- function(x, ..., print = TRUE) {
	class(x) <- c("command", class(x))
	attr(x, "default.args") <- list(...)
	attr(x, "print_result") <- print
	x
}

# Aliases for quit()
# exit
exit <- function() { quit() }
exit <- make_command(exit,print = FALSE)
.env$exit <- exit

# q
q <- function() { quit() }
q <- make_command(q,print = FALSE)
.env$q <- q

# Add any functions.
attach(.env,warn.conflicts=FALSE)
