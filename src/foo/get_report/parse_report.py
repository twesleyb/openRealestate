#!/usr/bin/env python3

import re

# Define a helper function that extracts key-value pairs from text.
def get_kv_pair(string,key):
    ''' Get the value of a key from the string. '''
    value = string.split(key)[1].strip().split(' ')[0].strip()
    pair = {key:value}
    return(pair)
#EOF

# Define main function that reads report.txt and extracts key-value pairs.
def parse_report(input_text = '.temp.txt'):
    ''' Parse the text output of pdftotext. '''
    # Read result from pdftotext.
    with open(input_text,'r') as myfile:
        text_list = myfile.readlines()
        myfile.close()
    # Coerce list to a single string.
    string = ' '.join(text_list)
    # We will values for the following keys.
    keys = ['PIN','Parcel ID','Acreage','Land Use','Land Value','Land Use',
            'Deed Book', 'Deed Page', 'Plat Book', 'Plat Page', 'Subdivision',
            'Land Value', 'Building Value', 'Total Value', 'Sale Price']
    results_list = [get_kv_pair(string,key) for key in keys]
    results = {k: v for d in results_list for k, v in d.items()}
    return(results)
#EOF
