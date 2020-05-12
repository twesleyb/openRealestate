#!/usr/bin/env python3

from . import config

from pandas import read_csv
from random import randrange


def load_addresses(addr_data):
    ''' Load Durham addresses from https://openaddresses.io/ '''
    addr = read_csv(addr_data)
    # Clean-up the address data.
    addr = addr.dropna(axis='index',subset=['POSTCODE']) # Drop Na.
    addr['POSTCODE'] = [str(int(z)) for z in addr['POSTCODE'].values] # To str.
    addr.loc[(addr.CITY == 'DURH'),'CITY']='DURHAM' # Fix names.
    addr.loc[(addr.CITY == 'CHAP'),'CITY']='CHAPEL HILL' # Fix names.
    # Subset data from Durham, NC.
    addr = addr.loc[(addr.CITY == 'DURHAM'),]
    # Collect rows as dicts.
    addr_dict = addr.to_dict('index')
    # Coerce to list of dicts.
    addr_list = [addr_dict.get(key) for key in addr_dict.keys()]
    return(addr_list)
#EOF


class durham:
    ''' Simple class that contains list of addresses. '''
    addr_list = load_addresses(config.ADDR_DATA)
    def random():
        i = randrange(len(durham.addr_list))
        address = durham.addr_list.pop(i)
        return(address)
# EOC
