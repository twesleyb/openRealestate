#!/usr/bin/env python3
""" Functions for working with Durham addresses. """

import re
import sys
import json

from pandas import read_csv
from random import randrange

from . import utils
from . import config

# Simple function to test if value is a string.
def isstr(val):
    """ Example: 
        >>> isstr('string') # Returns True
    """
    return isinstance(val, str)

# Simple function to remove excess whitespace from a string.
def clean_str(string):
    """ Example:
        >>> In [1]: clean_str('   the  fat     cat  sat   in the hat      ')
        >>> Out[1]: 'the fat cat sat in the hat'
    """
    string = re.sub(' +', ' ',string)
    return string.strip()

# Simple function to strip excess whitespace from dict values.
def clean_dict(mydict):
    """ Strip whitespace from dictionary strings. """
    keys = list(mydict.keys())
    #vals = [val.strip() if isstr(val) else val for val in mydict.values()]
    vals = [clean_str(val)  if isstr(val) else val for val in mydict.values()]
    return dict(zip(keys, vals))


# Load address data from file.
def load_addresses(addr_data):
    """ Load Durham addresses from https://openaddresses.io/ """
    addr = read_csv(addr_data)
    # Clean-up the address data.
    addr = addr.dropna(axis="index", subset=["POSTCODE"])  # Drop Na.
    addr["POSTCODE"] = [str(int(z)) for z in addr["POSTCODE"].values]  # To str.
    addr.loc[(addr.CITY == "DURH"), "CITY"] = "DURHAM"  # Fix names.
    addr.loc[(addr.CITY == "CHAP"), "CITY"] = "CHAPEL HILL"  # Fix names.
    # Subset data from Durham, NC.
    addr = addr.loc[
        (addr.CITY == "DURHAM"),
    ]
    # Collect rows as dicts.
    addr_dict = addr.to_dict("index")
    # Coerce to list of dicts.
    addr_list = [addr_dict.get(key) for key in addr_dict.keys()]
    # Insure that extra whitspace is stripped.
    addr_list = [clean_dict(addr) for addr in addr_list]
    return addr_list


# EOF

# Simple function to remove an element from a list by index.
def del_index(mylist, index):
    del mylist[index]
    return mylist


# Filter addresses.
def filter_addresses(addr_list):

    # FIXME: Not working with stderr:
    # json_file = open(config.STDERR).read()
    # output_stderr = json.loads(json_file)

    # Generate identifiers for addresses in addr_list.
    terms = {"t1": "NUMBER", "t2": "STREET", "t3": "POSTCODE"}
    addr_keys = [utils.combine_terms(addr, **terms) for addr in addr_list]

    # Load found addresses.
    json_file = open(config.STDOUT).read()
    found_addr = json.loads(json_file)

    # Generate identifiers for addresses in found addresses.
    terms = {"t1": "SITE_ADDRE", "t2": "OWZIPA"}
    found_keys = [
        utils.combine_terms(found_addr.get(k), **terms) for k in found_addr.keys()
    ]

    # Remove address from addr_list if it was already found.
    # This is pretty slow.
    print(
        "Removing addresses that have already been found from addr_list.",
        "This may take several minutes...\n",
        file=sys.stderr,
    )
    found = [addr in found_keys for addr in addr_keys]
    remove = [i for i, j in enumerate(found) if j]
    addr_filt = [i for j, i in enumerate(addr_list) if j not in remove]

    return addr_filt


# EOF

# A class that contains open addresses for Durham, NC.
class durham:
    """ Simple class that contains list of addresses. """

    addr_list = load_addresses(config.ADDR_DATA)

    def random(addr_list):
        i = randrange(len(addr_list))
        return addr_list.pop(i)

    def filt(addr_list):
        return filter_addresses(addr_list)


# EOC
