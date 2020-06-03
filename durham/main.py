#!/usr/bin/env python3
""" This scrapes address data from durham gomaps. """

# FIXME: remove address that have not been found from addr_list.
# FIXME: How to handle this error:
# invalid literal for int() with base 10: ''
# occured at i = 123509

# Imports.
import sys

# Local imports.
from webscraper import utils
from webscraper import gomaps
from webscraper import addresses

# Create webdriver.
driver = gomaps.launch_gecko(headless=True)

# Load address list class.
durham = addresses.durham

# Get filtered addresses.
# FIXME: handle error which will probably arise if no stdout.json exists!
addr_list = durham.addr_list
addr_filt = durham.filt(addr_list)

# Loop to do the work:
while len(addr_filt) > 0:

    # Get a random address.
    address = durham.random(addr_filt)
    msg = " ".join(
        [
            address.get("NUMBER"),
            address.get("STREET"),
            address.get("CITY"),
            address.get("POSTCODE"),
        ]
    )
    print("Searching for: {}...".format(msg), file=sys.stderr)

    # Search for address.
    response = gomaps.find_address(driver, address)

    # Check response.
    if response is None:
        print("... Address not found.\n", file=sys.stderr)
        gomaps.append_errors(address)
        driver.refresh()
        utils.zzz(5)
        continue

    # Add nearby parcels to results.
    print("Address found. Adding nearby parcels to results...", file=sys.stderr)
    response = gomaps.add_buffer(driver, start=2500, increase_by=500)

    # Download results, and then load into python.
    gomaps.download_results(driver)
    results = gomaps.load_results()

    # Update results.
    print("Updating results.\n", file=sys.stderr)
    gomaps.append_results(results)
# EOL
