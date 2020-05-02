#!/usr/bin/env python3

# It's so easy.

import os
import sys
import json
import importlib
from os.path import dirname

## Defaults:
URL='http://maps2.roktech.net/durhamnc_gomaps4/'
DRIVER = '/home/twesleyb/bin/chromium/chromedriver.exe'

# Directories.
here = os.getcwd()
root = dirname(here)
sys.path.append(root)

# Load Functions in root/Py
import Py
from Py.launch_bug import launch_bug
from Py.zzz import zzz

# Load addresses.
from pandas import read_csv
addr = read_csv('durham.csv')

# Clean up the address data.
addr = addr.dropna(axis='index',subset=['POSTCODE']) # Drop Na.
addr['POSTCODE'] = [str(int(z)) for z in addr['POSTCODE'].values] # Coerce to str
addr.loc[(addr.CITY == 'DURH'),'CITY']='DURHAM'
addr.loc[(addr.CITY == 'CHAP'),'CITY']='CHAPEL HILL'

# Subset data from Durham.
addr = addr.loc[(addr.CITY == 'DURHAM'),]

# Collect rows as dicts.
mydict = addr.to_dict('index')

# Coerce to list.
addr_list = [mydict.get(key) for key in mydict.keys()]

# Define a function that clicks a button and sleeps for a random duration.
def click(button):
    button.click()
    zzz()
#EOF

# Define a wrapper to catch errors.
# FIXME: if any error, return None and reset.
def scrape_addr(driver,address,neighbors=True):
    ''' Scrape an addresses data from DurhamGOMaps.'''
    # Open the query builder.
    button = driver.find_element_by_id("queryBuilderNav")
    click(button)
    # Search for parcels.
    drop_down = driver.find_element_by_name('Parcels')
    click(drop_down)
    # Clear any existing text.
    button = driver.find_element_by_id("btnQueryBuilderClear")
    click(button)
    # Build a query.  
    addr_str = address.get('NUMBER') + ' ' + address.get('STREET')
    keys={"address":addr_str,"zip":address.get('POSTCODE')}
    query = "SITE_ADDRE = '{address}' And OWZIPA = {zip}".format(**keys)
    # Add query.
    text_box = driver.find_element_by_id("queryBuilderQueryTextArea")
    text_box.send_keys(query)
    zzz()
    # Submit query.
    button = driver.find_element_by_id("btnQueryBuildersearch")
    click(button)
    # Initial numer of results:
    n = int(driver.find_element_by_id("numberofResults").text.split(" ")[0])
    print("Found {} result(s).".format(n),file=sys.stderr)
#EOF

def get_supplement(driver,result=0,data_type="report"):
    # Find parcel report or tax history by number.
    button = driver.find_element_by_id("{}{}".format(data_type,result))
    # Open report in a new tab.
    click(button)
    zzz(5)
    # Switch to new tab and get its url.
    driver.switch_to.window(driver.window_handles[-1])
    zzz()
    url=driver.current_url
    # Close the tab and switch back to main tab.
    driver.close()
    zzz()
    driver.switch_to.window(driver.window_handles[-1])
    return(url)
# EOF.

for i in range(len(addr_list)):
    ## ACTUAL WORK:
    print("Scraping data for address: {}".format(i))
    # Launch chromium bughhk.
    driver = launch_bug(URL,executable_path=DRIVER)
    # Get an address.
    address = addr_list[i]
    # Search for an address.
    scrape_addr(driver,address)
    # Get supplement.
    url = get_supplement(driver)
    driver.close()
    address['report'] = url
    with open('results.txt','a') as json_file:
        json.dump(address, json_file)
# EOL
