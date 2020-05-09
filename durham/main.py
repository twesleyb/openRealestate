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

## Get an address.
i = randrange(len(addr_list))
address = addr_list[i]

# Search for address.
response = find_address(driver,address)

# Check response.
if response is None:
print(response)

# Increase buffer distance.
#add_buffer(driver,buffer_dist=1000)

# Download results.
driver.find_element_by_id('exportToExcelbtn').click()

# Parse results.

