#!/usr/bin/env python3
""" Functions for interacting with durham gomaps."""

import os
import re
import sys

import random
import subprocess
from time import sleep

from pandas import read_csv

from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.firefox.options import Options

import json
from pathlib import Path
from importlib import import_module

# Local imports.
from . import utils
from . import config

# Launch a webdriver.
def launch_gecko(
    gecko_path=config.DRIVER,
    profile_path=config.PROFILE,
    url=config.GOMAPS,
    headless=False,
    log_path="/dev/null",
):
    """ Launch geckodriver configured for webscraping."""

    # Firefox options:
    options = Options()
    if headless:
        options.add_argument("--headless")

    # Firefox profile.
    if profile_path is not None:
        firefox_profile = FirefoxProfile(profile_path)
    else:
        firefox_profile = None

    # Create webdriver.
    driver = webdriver.Firefox(
        executable_path=gecko_path,
        options=options,
        firefox_profile=firefox_profile,
        service_log_path=log_path,
    )

    # If provided, navigate to webpage.
    if url is not None:
        driver.get(url)
        print("Launched gecko at: {}\n".format(url), file=sys.stderr)

    return driver


# EOF

# Wrapper to catch errors.
def safety(fun):
    """ A wrapper function that catches errors and returns None."""

    def wrapper(*args):
        try:
            return fun(*args)
        except Exception as e:
            # print(e,file=sys.stderr)
            return None

    return wrapper


# Search for an address.
@safety
def find_address(driver, address):
    """Find an address on DurhamGOmaps."""
    # Open the query builder.
    button = driver.find_element_by_id("queryBuilderNav")
    button.click()
    utils.zzz()
    # Search for parcels.
    drop_down = driver.find_element_by_name("Parcels")
    drop_down.click()
    utils.zzz()
    # Clear any existing text.
    button = driver.find_element_by_id("btnQueryBuilderClear")
    button.click()
    utils.zzz()
    # Build a query.
    addr_str = " ".join([address.get("NUMBER").strip(), address.get("STREET").strip()])
    keys = {"address": addr_str, "zip": address.get("POSTCODE").strip()}
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


# EOF

# Buffer nearby parcels.
def add_buffer(driver, start, increase_by, n_max=1000):
    """ Add additional parcels to search result by adding nearby properties. """
    # Initial number of results.
    n = int(driver.find_element_by_id("numberofResults").text.split(" ")[0])
    buffer_dist = start
    while n <= n_max:
        buffer_dist += increase_by
        # Open buffer box before trying to select an option from drop down!
        buffer_box = driver.find_element_by_id("buffer0")
        buffer_box.click()
        utils.zzz(2)
        # Selects parcel option.
        xpath = "//select[@name='activeLayersBuffer']/option[text()='Parcels']"
        drop_down = driver.find_element_by_xpath(xpath)
        drop_down.click()
        utils.zzz(3)
        # Add buffer.
        el = driver.find_element_by_id("buferdistance")
        el.clear()
        el.send_keys(buffer_dist)
        utils.zzz(3)
        # Submit.
        driver.find_element_by_id("buffersearchbtn").click()
        utils.zzz(2)
        n = int(driver.find_element_by_id("numberofResults").text.split(" ")[0])
        if n == n_max:
            break
        # EOL
    return "Found {} result(s)".format(n)


# EOF

# Download results, saved in root/downloads.
def download_results(driver, refresh=True):
    """ Download currently active results from gomaps. """
    driver.find_element_by_id("exportToExcelbtn").click()
    utils.zzz(5)
    if refresh:
        driver.refresh()


# EOF

# Load results from file into python.
def load_results():
    """ Load downloaded results (export.csv) into python. """
    ## FIXME: remove excess spaces from strings.

    # Load results.
    results = read_csv(config.EXPORT_CSV)

    # Convert rows to dicts and combine in a list..
    results_dict = results.to_dict("index")
    results_list = [results_dict.get(key) for key in results_dict.keys()]

    # Get parcel ids and create results dictionary.
    ids = [res.get("PARCEL_ID") for res in results_list]
    results = dict(zip(ids, results_list))

    # Clean-up
    os.remove(config.EXPORT_CSV)

    return results


# EOF

# If an address is not found, append this to file.
def append_errors(mydict):
    """ Append a dictionary to json file.
    Requires:
        pathlib.Path, json.dump
    """
    output = config.STDERR
    try:
        check = Path(output).resolve(strict=True)
    except FileNotFoundError:
        # If file doesn't exist, then create it.
        json_file = open(output, "a+")
    else:
        # If file exists, then append to it.
        with open(output, "a+") as json_file:
            json.dump(mydict, json_file)
            json_file.write("\n")
            json_file.close()


# EOF

# Append found addresses to file.
def append_results(mydict):
    """ Append a dictionary to json file.
    Requires:
        pathlib.Path, importlib.import_module, json.dump
    """
    output = config.STDOUT
    try:
        check = Path(output).resolve(strict=True)
    except FileNotFoundError:
        # If file doesn't exist, then create it.
        json_file = open(output, "a+")
        with open(output, "a+") as json_file:
            json.dump(mydict, json_file, indent=4)
            json_file.write("\n")
            json_file.close()
    else:
        # Load current results.
        json_file = open(output).read()
        results = json.loads(json_file)
        # Update.
        results.update(mydict)
        print("Total number of results: {:,}.\n".format(len(results)), file=sys.stderr)
        # Write to file.
        json_file = open(output, "w+")
        json.dump(results, json_file, indent=4)
        json_file.write("\n")
        json_file.close()


# EOF
