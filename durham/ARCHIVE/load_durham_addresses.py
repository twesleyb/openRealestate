#!/usr/bin/env python3

from pandas import read_csv


def load_durham_addresses(addr_data):
    """ Load Durham addresses from https://openaddresses.io/ """
    addr = read_csv(addr_data)
    # Clean-up the address data.
    addr = addr.dropna(axis="index", subset=["POSTCODE"])  # Drop Na.
    addr["POSTCODE"] = [str(int(z)) for z in addr["POSTCODE"].values]  # Coerce to str
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
    return addr_list


# EOF
