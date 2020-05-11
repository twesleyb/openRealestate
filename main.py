#!/usr/bin/env python3
''' It's so easy. '''

# How to handle this error:
# invalid literal for int() with base 10: ''
# occured at i = 123509 

# Imports.
import os
from pandas import read_csv
from random import randrange
from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.firefox.options import Options

# Additional imports.
from durham.launch_gecko import *
from durham.load_durham_addresses import *
from durham.find_address import *

def combine_terms(mydict,**kwargs):
    ''' Combine site address and zip code to identify a parcel. '''
    vals = [mydict.get(arg) for arg in kwargs.values()]
    clean_vals = [val.strip() for val in vals]
    return(' '.join(clean_vals))
# EOF

## Input parameters:
gecko_driver = '/mnt/c/Program Files/Mozilla Firefox/geckodriver.exe'
#output_json = '/home/twesleyb/open-realestate/data/durham-realestate.json'
#output_err = '/home/twesleyb/open-realestate/data/durham-not-found.json'

## DEFAULTS:
PROFILE = '/home/twesleyb/projects/open-realestate/profile/'
ADDR_DATA = '/home/twesleyb/projects/open-realestate/data/durham-addresses.csv'
GOMAPS = 'http://maps2.roktech.net/durhamnc_gomaps4/'

## Create webdriver.
profile = FirefoxProfile(PROFILE) 
driver = launch_gecko(gecko_driver,firefox_profile=profile,
        url=GOMAPS,headless=True)

## Load address list.
addr_list = load_durham_addresses(ADDR_DATA)

## Collect addresses that we cannot find in a list:
not_found = list()

## ORDER OF OPERATIONS:
# * Search for a randomized address.
#   - If not found, then remove from search list.
#   - Write to file.

# * Add nearby parcels until n results == 1,000.
# * Download into root/downloads.
# * Remove found addresses from search list.
# * Write data to file!!!


while len(addr_list) > 0:
    ## Get a random address.
    i = randrange(len(addr_list))
    address = addr_list[i]
    # Search for address.
    # NOTE: The following error will be caught, and results in response = None.
    # Alert Text: None
    # Message: Dismissed user prompt dialog: No Features Found.
    response = find_address(driver,address)
    # Check response.
    if response is None:
        driver.refresh()
        sleep(5)
        not_found.append(addr_list.pop(i))
        continue
    # EIF
    # Increase buffer distance.
    print("Adding additional parcels to search results...",file=sys.stderr)
    n = int(response.split(' ')[1])
    buffer_dist = 2500
    while n <= 1000:
        buffer_dist += 500
        # Open buffer box before trying to select an option from drop down!
        buffer_box = driver.find_element_by_id('buffer0')
        buffer_box.click()
        sleep(2)
        # Selects parcel option.
        xpath = "//select[@name='activeLayersBuffer']/option[text()='Parcels']"
        drop_down = driver.find_element_by_xpath(xpath)
        drop_down.click()
        sleep(2)
        # Add buffer.
        el = driver.find_element_by_id('buferdistance')
        el.clear()
        el.send_keys(buffer_dist)
        sleep(2)
        # Submit.
        driver.find_element_by_id('buffersearchbtn').click()
        sleep(2)
        n = int(driver.find_element_by_id('numberofResults').text.split(' ')[0])
        print("Number of results: {}.".format(n))
        if n == 1000: 
            break
    # EWL
    # Download results.
    driver.find_element_by_id('exportToExcelbtn').click()
    sleep(5)
    driver.refresh()
    # Parse results -- remove found addresses from address list.
    DATA = '/home/twesleyb/projects/open-realestate/downloads/export.csv'
    results = read_csv(DATA)
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





