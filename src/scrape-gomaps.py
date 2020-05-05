#!/usr/bin/env python3

# It's so easy.

#import os
import sys
#import json
#from pandas import read_csv

## User parameters:
# Output directory for data.
addr_data = '/home/twesleyb/projects/open-realestate/data/durham.csv'

## Defaults:
CHROMIUM = '/home/twesleyb/bin/chromium/chromedriver.exe'
ROOT = '/home/twesleyb/projects/open-realestate/'

# Add root/Py to path.
sys.path.append(ROOT)

# Load Functions in root/Py
from . import .scrape

from . import foo.

import .scrape

from src.addresses import *
from src.scrape import *

from src.get_report import *

from Py.find_address import *
from Py.load_durham_addresses import *

from Py.get_report_url import *
from Py.get_report import *



# Launch chromium bug.
driver = launch_bug(chromium_path=CHROMIUM)

# Load addresses.
addr_list = load_durham_addresses(addr_data)

# Loop to scrape data for all address in list.
for i in range(len(addr_list)):

    # Get an address.
    i = 1
    address = addr_list[i]

    # Status report.
    msg = ' '.join([address.get('NUMBER'), address.get('STREET'),
        address.get('CITY'), address.get('POSTCODE')])
    print('Searching for: {}...'.format(msg),file=sys.stderr)

    # Search for an address.
    response = find_address(driver,address)

    # If address not found--skip iteration.
    if response is None:
        driver.refresh()
        zzz()
        continue

    # Status:
    print("Address found. Collecting parcel report.",file=sys.stderr)

    results = get_report(url)

    # Add to address dictionary.
    address = addr_list.pop(i)
    address.update(report)

    # Write as json.
    with open('durham-realestate.txt','a') as json_file:
        json.dump(address, json_file)
        json_file.write('\n')
        json_file.close()

    # Rinse and repeat.
    driver.refresh()
# EOL
