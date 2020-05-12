#!/usr/bin/env python3
''' It's so easy. '''

# How to handle this error:
# invalid literal for int() with base 10: ''
# occured at i = 123509 

# Imports.
from webscraper import utils
from webscraper import gomaps
from webscraper import addresses

## Parameters:
output_json = '/home/twesleyb/open-realestate/data/durham-realestate.json'
output_err = '/home/twesleyb/open-realestate/data/durham-not-found.json'

## Create webdriver.
driver = gomaps.launch_gecko(headless=True)

## Load address list = Class.
durham = addresses.durham

## ORDER OF OPERATIONS:
# * Search for a randomized address.
#   - If not found, then remove from search list.
#   - Write to file.

# * Add nearby parcels until n results == 1,000.
# * Download into root/downloads.
# * Remove found addresses from search list.
# * Write data to file!!!


while len(durham.addr_list) > 0:

    ## Get a random address.
    address = durham.random()

    # Search for address.
    response = gomaps.find_address(driver,address)

    # Check response.
    if response is None:
        append_results(address,output_err)
        driver.refresh()
        sleep(5)
        continue

    ## Add additional results.
    response = gomaps.add_buffer(driver,start=500,increase_by=500)

    ## Download.
    download_results(driver)

    ## Load results and append to output.
    append_results(address, output_json)

    # Parse results -- remove found addresses from address list.
    RESULTS_PATH = '/home/twesleyb/projects/open-realestate/downloads/export.csv'
    results = read_csv(RESULTS_PATH)

    results_dict = results.to_dict('index')
    results_list = [results_dict.get(key) for key in results_dict.keys()]
    # We collected these addresses:
    found_addresses = [combine_terms(addr,t1='SITE_ADDRE') for addr in results_list]
    # These are the addresses we have not yet searched for:
    current_addresses = [combine_terms(addr,t1='NUMBER',t2='STREET') for addr in addr_list]
    # These are the matches:
    check = [current_addresses.index(addr) if addr in current_addresses else None for addr in found_addresses]
    idx = [x for x in check if x is not None]
    # Remove any address in list that we have collected data for.
    found = [addr_list.pop(i) for i in idx]
    os.remove(DATA) 
# LOOP





    # Add to address dictionary.
    address.update(results)
    # Append results to json file.
    append_results(address, output_json)
    # Rinse and repeat.
    driver.refresh()
# EOL
