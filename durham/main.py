#!/usr/bin/env python3
''' It's so easy. '''

from random import randrange
from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.firefox.options import Options

# Additional imports.
from launch_gecko import *
from load_durham_addresses import *
from find_address import *

## Input parameters:
gecko_driver = '/mnt/c/Program Files/Mozilla Firefox/geckodriver.exe'
#output_json = '/home/twesleyb/open-realestate/data/durham-realestate.json'
#output_err = '/home/twesleyb/open-realestate/data/durham-not-found.json'

## DEFAULTS:
PROFILE = '/home/twesleyb/projects/open-realestate/firefox-profile/'
ADDR_DATA = '/home/twesleyb/projects/open-realestate/data/durham.csv'
GOMAPS = 'http://maps2.roktech.net/durhamnc_gomaps4/'

## Create webdriver.
profile = FirefoxProfile(PROFILE)
driver = launch_gecko(gecko_driver,firefox_profile=profile,
        url=GOMAPS,headless=True)

## Load address list.
addr_list = load_durham_addresses(ADDR_DATA)

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
    continue

# Increase buffer distance.
print("Increasing buffer...",file=sys.stderr)
n = int(response.split(' ')[1])
buffer_dist = 0
while n <= 1000:
    buffer_dist += 100
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
    driver.find_element_by_id('buferdistance').send_keys(buffer_dist)
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

# Parse results -- remove found addresses from address list.
from pandas import read_csv

DATA = '/home/twesleyb/projects/open-realestate/downloads/export.csv'
results = read_csv(DATA)

results_dict = results.to_dict('index')
results_list = [results_dict.get(key) for key in results_dict.keys()]
# GET NUMBER
# STREET
# CITY
# POSTCODE

collected_addr = [res.get('SITE_ADDRE').strip() for res in results_list]

items = [' '.join([addr.get('STREET'),addr.get('NUMBER')]) for addr in addr_list]

[ b.index(x) if x in b else None for x in a ]


