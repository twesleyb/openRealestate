#!/usr/bin/env python3
''' It's so easy. '''

from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.firefox.options import Options

# Additional imports
from utils.zzz import *
#from scrape.launch_gecko import *
from scrape.load_durham_addresses import *
from scrape.find_address import *

# When you launch your Firefox browser, it loads your save preferences.
# On Windows these are often found in %APPDATA%\Mozilla\Firefox\Profiles\.

# By default Firefox will prompt you when downloading a file.
# After changing this setting, your handlers.json file will be modified.

# Initially nothing is in the profile directory.
# When you launch the driver, user.js is created.

# What are the minimum requirements for a profile?
# You can create a directory containing user.js and it works.

# You can pass a file path to an empty directory, and it works.
# A tempory directory will be created with a new user.js with the defaults.

# If we just update handlers, is that enough?

## Input parameters:
# NOTE: Firefox executable needs to be in the same directory as geckodriver, 
# or set as en environmental variable. (Is it set on Windows side?)
gecko = '/mnt/c/Program Files/Mozilla Firefox/geckodriver.exe'
addr_data = '/home/twesleyb/projects/open-realestate/data/durham.csv'
#output_json = '/home/twesleyb/open-realestate/data/durham-realestate.json'
#output_err = '/home/twesleyb/open-realestate/data/durham-not-found.json'

## Create firefox profile.
# NOTE: (1) Calls to FirefoxProfile() create a temporary firefox profile, 
# which is saved in /tmp/. e.g.: /tmpt/tmpizzfipxs
# You can see its path with: profile.path
# NOTE: (2) You can pass a path to FirefoxProfile.
# If you do this, a temporary copy of the profile is made. For example,
# > profile.path
# '/tmp/tmpvo_h1gzw/webdriver-py-profilecopy'

firefox_profile = '/home/twesleyb/projects/open-realestate/firefox-profile/'
profile = FirefoxProfile(firefox_profile)
#profile.set_preference("browser.download.folderList", 2)
#profile.set_preference("browser.download.dir",'/mnt/d/projects/downloads')
#profile.set_preference("browser.download.panel.shown", False)
#profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
#        "text/csv;application/vnd.ms-excel;application/msword")
#profile.update_preferences()
## Create firefox options.
options = Options()
#options.add_argument('--headless')
## Create webdriver.
driver = webdriver.Firefox(executable_path=gecko,
        options=options,firefox_profile=profile)

## Navigate to durham gomaps
gomaps = 'http://maps2.roktech.net/durhamnc_gomaps4/'
driver.get(gomaps)
zzz(5)

## Load address list.
addr_list = load_durham_addresses(addr_data)

## Get an address.
address = addr_list[0]

# Search for address.
response = find_address(driver,address)
zzz(5)

# Check response.
print(response)

# Increase buffer distance.
#add_buffer(driver,buffer_dist=1000)

# Download results.
driver.find_element_by_id('exportToExcelbtn').click()
