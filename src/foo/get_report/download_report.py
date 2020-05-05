#!/usr/bin/env python3
''' Download a report associated with an address. '''

import os
import subprocess

def download_report(url,output_pdf='.temp.pdf'):
    ''' Get supplemental data associated with an address.'''
    # Download report with wget.
    cmd = ["wget", "--quiet", "-O", ".temp.pdf", url]
    process = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    response = process.communicate()
    stdout, stderr = [r.decode('utf-8').strip() for r in response]
    return(stderr)
# EOF
#!/usr/bin/env python3

import re
import sys
import subprocess

# Define a function that converts report.pdf to report.text.
def convert_report(input_pdf='.temp.pdf',output_txt='.temp.txt'):
    ''' Get supplemental data associated with an address.'''
    # Convert pdf to text.
    cmd = ['pdftotext','-raw','-nopgbrk',input_pdf, output_txt]
    process = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    response = process.communicate()
    stdout, stderr = [r.decode('utf-8').strip() for r in response]
    return(stderr)
#EOF
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
