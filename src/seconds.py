#!/usr/bin/env python3

## Parameters:
gecko = '/mnt/c/Program Files/Mozilla Firefox/geckodriver.exe'
parcel_id = 150621

# Imports
from bs4 import BeautifulSoup  

from scrape.launch_gecko import *

# Defaults:
BASE_URL='https://property.spatialest.com/nc/durham/#/property/{}'

# Launch gecko
driver = launch_gecko(executable_path=gecko)

# Get webpage.
url = BASE_URL.format(parcel_id)
driver.get(url)

# Get html source.
html = driver.page_source

# Parse with bs4.
soup = BeautifulSoup(html,'html')


