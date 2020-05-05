#!/usr/bin/env python3
''' It's so easy. '''

import sys

## User parameters:
addr_data = '/home/twesleyb/projects/open-realestate/data/durham.csv'
chromium_path = '/home/twesleyb/projects/open-realestate/drivers/chromium/chromedriver.exe'
output_json = '/home/twesleyb/open-realestate/data/durham-realestate.json'
output_err = '/home/twesleyb/open-realestate/data/durham-not-found.json'

# Load Functions:
from utils.zzz import *
from utils.append_results import *

from scrape.load_durham_addresses import *
from scrape.find_address import *
from scrape.launch_bug import *
from scrape.get_report import *

# Load addresses.
addr_list = load_durham_addresses(addr_data)

# Launch chromium bug.
driver = launch_bug(chromium_path)

# Loop through address list, scrape report data.
while len(addr_list) > 0:
    # Status report.
    address = addr_list.pop(0)
    msg = ' '.join([address.get('NUMBER'), address.get('STREET'),
        address.get('CITY'), address.get('POSTCODE')])
    print('Searching for: {}...'.format(msg),file=sys.stderr)
    # Search for an address.
    response = find_address(driver,address)
    # If address was not found--skip loop iteration.
    if response is None:
        # Append address to file.
        append_results(address,output_err)
        driver.refresh()
        zzz()
        continue # skips current iteration.
    # Status:
    print("Address found. Collecting parcel report...\n",file=sys.stderr)
    results = get_report(driver)
    # Add to address dictionary.
    address.update(results)
    # Append results to json file.
    append_results(address, output_json)
    # Rinse and repeat.
    driver.refresh()
# EOL
