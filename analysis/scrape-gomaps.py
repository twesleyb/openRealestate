#!/usr/bin/env python3

# It's so easy.

import os
import sys
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
    # Initial numer of results:
    n0 = int(driver.find_element_by_id("numberofResults").text.split(" ")[0])
    print("Found {} result(s).".format(n0),file=sys.stderr)
    # Get neighbors?
    if neighbors:
        # Get adjacent properties and update table.
        el = driver.find_element_by_id("adjoiner0")
        button = el.find_element_by_tag_name('a')
        click(button)
        table = driver.find_element_by_id("tblSRNDetails")
    # Collect results from table.
    results = table.text.split("\n")
    # Numer of results after adding neighbors:
    n1 = int(driver.find_element_by_id("numberofResults").text.split(" ")[0])
    print("Added {} neighbors.".format(n1-n0),file=sys.stderr)


    def get_supplement(driver,number,data_type):
        # Find parcel report or tax history by number.
        button = driver.find_element_by_id("{}{}".format(data_type,number))
        # Open report in a new tab.
        click(button)
        zzz(5)
        # Switch to new tab and get its url.
        driver.switch_to.window(driver.window_handles[-1])
        zzz()
        url=driver.current_url)
        # Close the tab and switch back to main tab.
        driver.close()
        zzz(5)
        driver.switch_to.window(driver.window_handles[-1])
        return(url)
    # EOF.

    # Reset.
    driver.refresh()
    # Return the raw results.

    print(urls)
    return results
# EOF


# function to take care of downloading file
def enable_download_headless(browser,download_dir):
    browser.command_executor._commands["send_command"] = ("POST",
            '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior':
        'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)
# EOF

# Launch chromium bug.
driver = launch_bug(URL,executable_path=DRIVER,headless=True)

num = "1011"
street = "ESTELLE CT"
zip_code = "27704"
address = {'number':num,'street':street,'zip':zip_code}

# Scrape some data.
results = scrape_addr(driver,address)

# Parse the results.
row = results[0]
row = row.replace("Zoom Buffer Find Adjoiners Report Tax Info","1 2 3 4 5")
rdata = row.split(' ')

rdata.remove('1','2','3','4','5')

search_input = driver.find_element_by_css_selector('#main-col > div > div > div:nth-child(8) > p:nth-child(1) > a > img')

search_input.click()
