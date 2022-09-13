#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#packages importation
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#### setting up working environment ####
while (!is.null(dev.list()))  dev.off()
rm(list=ls()) ## libs
cat("\014")

filepath <- rstudioapi::getSourceEditorContext()$path
dirpath  <- dirname(rstudioapi::getSourceEditorContext()$path)

setwd(dirpath)

# Package names 
packages <- c( "readxl", "plyr", "dplyr", "tibble","data.table", 
               "openxlsx", "writexl", "xlsx", "rJava", "devtools")

# Install packages not yet installed 
installed_packages <- packages %in% rownames(installed.packages()) 

if (any(installed_packages == FALSE)) {   
  install.packages(packages[!installed_packages]) 
} 

# Packages loading
invisible(lapply(packages, library, character.only = TRUE))

#-------------------------------------------------------------------------------

# installing appler package from github
devtools::install_github("ashbaldry/appler")
library(appler)


# pull data for KBC IOS app 
KBC <- lookup_apple(458066754, "be")
dim(KBC)
names(KBC)

# pull data for BNPP IOS app 
BNPP <- lookup_apple(516502006, "be")
dim(BNPP)
names(BNPP)

# select relevant data 


