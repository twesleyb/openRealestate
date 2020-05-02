#!/usr/bin/env python3

# It's so easy.

import os
import sys
import json
import importlib
from pandas import read_csv

## Defaults:
CHROMIUM = '/home/twesleyb/bin/chromium/chromedriver.exe'

# Directories.
here = os.getcwd()
root = os.path.dirname(here)
sys.path.append(root)

# Load Functions in root/Py
from Py.zzz import zzz 
from Py.launch_bug import *
from Py.find_address import *
from Py.get_supplement import *

# Load open address data.
addr = read_csv('durham.csv')

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

# The actual work.
for i in range(len(addr_list)):
    # Get an address.
    address = addr_list[i]
    address.keys()
    msg = ' '.join([address.get('NUMBER'), address.get('STREET'),
        address.get('CITY'), address.get('POSTCODE')])
    print('Searching for: {}'.format(msg),file=sys.stderr)
    # Launch chromium bug.
    driver = launch_bug(chromium_path=CHROMIUM)
    # Search for an address.
    find_address(driver,address)
    # Get supplement.
    url = get_supplement(driver)
    driver.close()
    # Add to address dictionary.
    address['report'] = url
    with open('realestate.txt','a') as json_file:
        json.dump(address, json_file)
# EOL


import requests

def safety(fun):
    def wrapper(*args):
        try:
            return fun(*args)
        except Exception:
            print("problem")
    return wrapper

@safety
def scrape(url):
    requests.get(url)

scrape('https://realpythor-on-python-decorators/#simple-decorators')

