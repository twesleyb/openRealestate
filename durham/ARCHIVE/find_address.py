#!/usr/bin/env python3
"""Find an address on DurhamGOmaps."""

import sys
import random
from time import sleep


def zzz(t=None, tmin=1, tmax=1.5):
    """ Take a nap. """
    if t is None:
        t = random.uniform(tmin, tmax)
    sleep(t)


# EOF


def safety(fun):
    """ A wrapper function that catches errors and returns None."""

    def wrapper(*args):
        try:
            return fun(*args)
        except Exception as e:
            print(e, file=sys.stderr)
            return None

    return wrapper


@safety
def find_address(driver, address):
    """ Find an address on DurhamGOMaps."""
    # Open the query builder.
    button = driver.find_element_by_id("queryBuilderNav")
    button.click()
    zzz()
    # Search for parcels.
    drop_down = driver.find_element_by_name("Parcels")
    drop_down.click()
    zzz()
    # Clear any existing text.
    button = driver.find_element_by_id("btnQueryBuilderClear")
    button.click()
    zzz()
    # Build a query.
    addr_str = address.get("NUMBER") + " " + address.get("STREET")
    keys = {"address": addr_str, "zip": address.get("POSTCODE")}
    query = "SITE_ADDRE = '{address}' And OWZIPA = {zip}".format(**keys)
    # Add query.
    text_box = driver.find_element_by_id("queryBuilderQueryTextArea")
    text_box.send_keys(query)
    zzz()
    # Submit query.
    button = driver.find_element_by_id("btnQueryBuildersearch")
    button.click()
    zzz()
    # Numer of results:
    n = int(driver.find_element_by_id("numberofResults").text.split(" ")[0])
    response = "Found {} result(s).".format(n)
    return response


# EOF
