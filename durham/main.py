#!/usr/bin/env python3
''' It's so easy. '''

# How to handle this error:
# invalid literal for int() with base 10: ''
# occured at i = 123509 

## ORDER OF OPERATIONS:
# * Search for a randomized address.
#   - If not found, then remove from search list.
#   - Write to file.

# * Add nearby parcels until n results == 1,000.
# * Download into root/downloads.
# * Remove found addresses from search list.
# * Write data to file!!!

# Imports.
from webscraper import utils
from webscraper import gomaps
from webscraper import addresses

## Create webdriver.
driver = gomaps.launch_gecko(headless=True)

## Load address list class.
durham = addresses.durham

while len(durham.addr_list) > 0:
    ## Get a random address.
    address = durham.random()
    # Search for address.
    response = gomaps.find_address(driver,address)
    # Check response.
    if response is None:
        gomaps.append_errors(address,'STDERR')
        driver.refresh()
        sleep(5)
        continue
    ## Add nearby parcels to results.
    response = gomaps.add_buffer(driver,start=1500,increase_by=500)
    ## Download results, and then load into python.
    gomaps.download_results(driver)
    results = gomaps.load_results()
    ## Update results.
    append_results(results)
# EOL

