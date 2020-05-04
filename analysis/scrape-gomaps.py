#!/usr/bin/env python3

# It's so easy.

import os
import sys
import json
from pandas import read_csv

## User parameters:
# Output directory for data.
data_dir = '/home/twesleyb/projects/open-realestate/data/'

## Defaults:
CHROMIUM = '/home/twesleyb/bin/chromium/chromedriver.exe'
ADDRESSES = '/home/twesleyb/projects/open-realestate/data/durham.csv'
ROOT = '/home/twesleyb/projects/open-realestate/'

# Add root/Py to path.
sys.path.append(ROOT)

# Load Functions in root/Py
from Py.zzz import *
from Py.launch_bug import *
from Py.get_report import *
from Py.find_address import *

# Load open address data.
addr = read_csv(ADDRESSES)

# Clean-up the address data.
addr = addr.dropna(axis='index',subset=['POSTCODE']) # Drop Na.
addr['POSTCODE'] = [str(int(z)) for z in addr['POSTCODE'].values] # Coerce to str
addr.loc[(addr.CITY == 'DURH'),'CITY']='DURHAM' # Fix names.
addr.loc[(addr.CITY == 'CHAP'),'CITY']='CHAPEL HILL' # Fix names.

# Subset data from Durham, NC.
addr = addr.loc[(addr.CITY == 'DURHAM'),]

# Collect rows as dicts.
addr_dict = addr.to_dict('index')

# Coerce to list of dicts.
addr_list = [addr_dict.get(key) for key in addr_dict.keys()]

# Launch chromium bug.
driver = launch_bug(chromium_path=CHROMIUM)
zzz(3)

# Loop to scrape data for all address in list.
for i in range(len(addr_list)):

    # Get an address.
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

    # Get supplemental data.
    report = get_report(driver)

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
