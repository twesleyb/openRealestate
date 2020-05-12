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
import sys
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
    msg = ' '.join([address.get('NUMBER'), address.get('STREET'),
        address.get('CITY'), address.get('POSTCODE')])
    print('Searching for: {}...'.format(msg), file=sys.stderr)
    # Search for address.
    response = gomaps.find_address(driver,address)
    # Check response.
    if response is None:
        print('... Address not found.', file = sys.stderr)
        gomaps.append_errors(address,'STDERR')
        driver.refresh()
        utils.zzz(5)
        continue
    ## Add nearby parcels to results.
    print('Address found. Adding nearby parcels to results...',file=sys.stderr)
    response = gomaps.add_buffer(driver,start=1500,increase_by=500)
    ## Download results, and then load into python.
    gomaps.download_results(driver)
    results = gomaps.load_results()
    ## Update results.
    print('Updating results.\n',file=sys.stderr)
    gomaps.append_results(results)
# EOL

