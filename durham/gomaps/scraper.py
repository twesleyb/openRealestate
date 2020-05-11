#!/usr/bin/env python3

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


def zzz(t=None,tmin=1,tmax=1.5):
    ''' A function that just sleeps for a random duration. '''
    if t is None:
        t = random.uniform(tmin,tmax)
    sleep(t)


def load_durham_addresses(addr_data):
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
    zzz()
    # Search for parcels.
    drop_down = driver.find_element_by_name('Parcels')
    drop_down.click()
    zzz()
    # Clear any existing text.
    button = driver.find_element_by_id("btnQueryBuilderClear")
    button.click()
    zzz()
    # Build a query.  
    addr_str = address.get('NUMBER') + ' ' + address.get('STREET')
    keys={"address":addr_str,"zip":address.get('POSTCODE')}
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
#EOF


def firefox_profile(profile_path):
    profile = FirefoxProfile(profile_path)
    return (profile)

def launch_gecko(gecko_path, firefox_profile = None, url=None, 
        headless=False, log_path = '/dev/null'):
    ''' Launch geckodriver at a specified url. '''
    options = Options()
    if headless:
        options.add_argument('--headless')
    driver = webdriver.Firefox(executable_path=gecko_path, 
            options = options, firefox_profile = firefox_profile,
            service_log_path = log_path)
    if url is not None:
        driver.get(url)
        print("Launched gecko at: {}".format(url),file=sys.stderr)
    return(driver)
#EOF


def get_report_url(driver,result=0):
    ''' Get url for the supplemental report associated with an address.'''
    # Find parcel report by number.
    button = driver.find_element_by_id("report{}".format(result))
    # Open report in a new tab.
    button.click()
    zzz(5)
    # Switch to new tab and get its url.
    driver.switch_to.window(driver.window_handles[-1])
    zzz()
    url=driver.current_url
    # Close the tab and switch back to main window.
    driver.close()
    zzz()
    driver.switch_to.window(driver.window_handles[-1])
    return(url)
# EOF


def download_report(url,output_pdf='.temp.pdf'):
    ''' Get supplemental data associated with an address.'''
    # Download report with wget.
    cmd = ["wget", "--quiet", "-O", ".temp.pdf", url]
    process = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    response = process.communicate()
    stdout, stderr = [r.decode('utf-8').strip() for r in response]
    return(stderr)

def convert_report(input_pdf='.temp.pdf',output_txt='.temp.txt'):
    ''' Convert report.pdf to report.text.'''
    cmd = ['pdftotext','-raw','-nopgbrk',input_pdf, output_txt]
    process = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    response = process.communicate()
    stdout, stderr = [r.decode('utf-8').strip() for r in response]
    return(stderr)
#EOF


def get_kv_pair(string,key):
    ''' Extract key-value pairs from a string. '''
    value = string.split(key)[1].strip().split(' ')[0].strip()
    pair = {key:value}
    return(pair)
#EOF


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


def get_report(driver):
    ''' Wrap-up all the work done above in a single function. '''
    # Get report url.
    url = get_report_url(driver)
    # Download report as pdf.
    response = download_report(url)
    # Convert pdf report to text.
    response = convert_report()
    # Extract key-value pairs from text.
    results = parse_report()
    return(results)
# EOF
