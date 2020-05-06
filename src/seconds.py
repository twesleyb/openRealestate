#!/usr/bin/env python3
''' It's so easy. '''

## Parameters:
gecko = '/mnt/c/Program Files/Mozilla Firefox/geckodriver.exe'
parcel_id = 150621

# Imports
from bs4 import BeautifulSoup  

# Additional functions.
from scrape.launch_gecko import *

# Defaults:
BASE_URL='https://property.spatialest.com/nc/durham/#/property/{}'

# Launch gecko
driver = launch_gecko(gecko_path=gecko)

# Get webpage.
url = BASE_URL.format(parcel_id)
driver.get(url)

# Get html source.
html = driver.page_source

# Parse with bs4.
soup = BeautifulSoup(html,'html')

table = soup.find_all('div', attrs={'id':'keyinformation'})
table = soup.find_all('div', attrs={'id':'keyinformation'})

foo = soup.find_all('li', attrs = {'class':'clearfix data-list-row'})
x = foo[1]
x.find_all('span',attrs = {'class':'title'})
x.find_all('span',attrs = {'class':'value'})



