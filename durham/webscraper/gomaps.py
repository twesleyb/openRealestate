#!/usr/bin/env python3

import os
import re
import sys
import json
import random
import subprocess
from time import sleep
from pandas import read_csv
from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.firefox.options import Options

from . import utils
from . import config


def launch_gecko(gecko_path=config.DRIVER, profile_path=config.PROFILE, 
        url=config.GOMAPS, headless=False, log_path = '/dev/null'):
    ''' Launch geckodriver configured for webscraping.'''

    # Firefox options:
    options = Options()
    if headless:
        options.add_argument('--headless')

    # Firefox profile.
    if profile_path is not None:
        firefox_profile = FirefoxProfile(profile_path)
    else:
        firefox_profile = None

    # Create webdriver.
    driver = webdriver.Firefox(executable_path=gecko_path, 
            options = options, firefox_profile = firefox_profile,
            service_log_path = log_path)

    # If provided, navigate to webpage.
    if url is not None:
        driver.get(url)
        print("Launched gecko at: {}".format(url),file=sys.stderr)

    return(driver)
#EOF


def safety(fun):
    ''' A wrapper function that catches errors and returns None.'''
    def wrapper(*args):
        try:
           return fun(*args)
        except Exception as e:
            print(e,file=sys.stderr)
            return None
    return wrapper


@safety
def find_address(driver,address):
    '''Find an address on DurhamGOmaps.'''
    # Open the query builder.
    button = driver.find_element_by_id("queryBuilderNav")
    button.click()
    utils.zzz()
    # Search for parcels.
    drop_down = driver.find_element_by_name('Parcels')
    drop_down.click()
    utils.zzz()
    # Clear any existing text.
    button = driver.find_element_by_id("btnQueryBuilderClear")
    button.click()
    utils.zzz()
    # Build a query.  
    addr_str = address.get('NUMBER') + ' ' + address.get('STREET')
    keys={"address":addr_str,"zip":address.get('POSTCODE')}
    query = "SITE_ADDRE = '{address}' And OWZIPA = {zip}".format(**keys)
    # Add query.
    text_box = driver.find_element_by_id("queryBuilderQueryTextArea")
    text_box.send_keys(query)
    utils.zzz()
    # Submit query.
    button = driver.find_element_by_id("btnQueryBuildersearch")
    button.click()
    utils.zzz()
    # Numer of results:
    n = int(driver.find_element_by_id("numberofResults").text.split(" ")[0])
    response = "Found {} result(s).".format(n)
    return response
#EOF


def add_buffer(driver, start, increase_by, n_max=1000):
    ''' Add additional parcels to search result by adding nearby properties. '''
    # Initial number of results.
    n = int(driver.find_element_by_id('numberofResults').text.split(' ')[0])
    buffer_dist = start
    while n <= n_max:
        buffer_dist += increase_by
        # Open buffer box before trying to select an option from drop down!
        buffer_box = driver.find_element_by_id('buffer0')
        buffer_box.click()
        utils.zzz(2)
        # Selects parcel option.
        xpath = "//select[@name='activeLayersBuffer']/option[text()='Parcels']"
        drop_down = driver.find_element_by_xpath(xpath)
        drop_down.click()
        utils.zzz(2)
        # Add buffer.
        el = driver.find_element_by_id('buferdistance')
        el.clear()
        el.send_keys(buffer_dist)
        utils.zzz(2)
        # Submit.
        driver.find_element_by_id('buffersearchbtn').click()
        utils.zzz(2)
        n = int(driver.find_element_by_id('numberofResults').text.split(' ')[0])
        if n == n_max:
            break
        # EOL
    return "Found {} result(s)".format(n)
# EOF

def download_results(driver,refresh=True):
    driver.find_element_by_id('exportToExcelbtn').click()
    utils.zzz(5)
    if refresh:
        driver.refresh()
# EOF



def append_results(mydict,output_json):
    ''' Append a dictionary to json file. '''
    with open(output_json,'a') as json_file:
        json.dump(mydict, json_file)
        json_file.write('\n')
    json_file.close()
# EOF
