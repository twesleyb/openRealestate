#!/usr/bin/env python3

# It's so easy.

import os
import sys
import importlib
from os.path import dirname

## Defaults:
BASE_URL="https://www.zillow.com/"
DRIVER = '/home/twesleyb/bin/chromium/chromedriver.exe'
URL='http://maps2.roktech.net/durhamnc_gomaps4/'

# Directories.
here = os.getcwd()
root = dirname(here)
sys.path.append(root)

# Load Functions in root/Py
import Py
from Py.launch_bug import launch_bug

# Launch chromium bug.
driver = launch_bug(URL,executable_path=DRIVER)

# Take a nap
def zzz(tmin=1,tmax=1.5):
    import random
    from time import sleep
    t=random.uniform(tmin,tmax)
    sleep(t)
#EOF

# Click a button and sleep for a random duration.
def click(button):
    button.click()
    zzz()
#EOF


# Scrape an addresses data.
# FIXME: if any error, return None and reset.
def scrape_addr(driver,address,neighbors=True):
    # Open the query builder.
    button = driver.find_element_by_id("queryBuilderNav")
    click(button)
    # Search for parcels.
    drop_down = driver.find_element_by_name('Parcels')
    click(drop_down)
    # Clear any existing text
    button = driver.find_element_by_id("btnQueryBuilderClear")
    click(button)
    # Build a query.  
    addr_str = address.get('number') + ' ' + address.get('street')
    keys={"address":addr_str,"zip":address.get('zip')}
    query = "SITE_ADDRE = '{address}' And OWZIPA = {zip}".format(**keys)
    # Add query.
    text_box = driver.find_element_by_id("queryBuilderQueryTextArea")
    text_box.send_keys(query)
    zzz()
    # Submit query.
    button = driver.find_element_by_id("btnQueryBuildersearch")
    click(button)
    # Need to wait until page is done loading...
    # Response is pretty quick if you get a hit.
    # Collect the initial results.
    table = driver.find_element_by_id("tblSRNDetails")
    n = num_results(driver)
    # Get neighbors?
    if neighbors:
        # Get adjacent properties and update table.
        el = driver.find_element_by_id("adjoiner0")
        button = el.find_element_by_tag_name('a')
        click(button)
        table = driver.find_element_by_id("tblSRNDetails")
    # Collect results from table.
    results = table.text.split("\n")
    # This downloads the report.
    #button = driver.find_element_by_id("report0")
    #button.click()
    # Reset.
    driver.refresh()
    zzz()
    # Return the raw results.
    return results
# EOF

#Get an address.
num = "1011"
street = "ESTELLE CT"
zip_code = "27704"

# Scrape some data.
results = scrape_addr(driver,address = {'number':num,'street':street,'zip':zip_code})

# Parse the results.
row = results[0]
row = row.replace("Zoom Buffer Find Adjoiners Report Tax Info","1 2 3 4 5")
rdata = row.split(' ')

rdata.remove('1','2','3','4','5')

