#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import requests
from torrequest import TorRequest

# Must install with pip. 
# Install pip with conda into env.
# Then insure you have unset pip
# $ unset pip
# $ unset pip3
#https://conda.io/projects/conda/en/latest/user-guide/getting-started.html#installing-a-package-with-pip
# /home/twesleyb/anaconda3/envs/pipenv/bin/pip install <package>

## Defaults:
url="https://www.zillow.com/"
TORPASS='16:84205A404D64FF5F60EB72627A012BB308919ACA14AB093C6F9379EAD7'

def get_cookies(url):
    ''' Get a websites cookies given its url. '''
    ## Default parameters.
    LOG_LEVEL = 3 # What does log level do?
    CHROME_DRIVER = '/home/twesleyb/bin/chromium/chromedriver.exe'
    # Chrome options and path to chromedriver.
    chrome = CHROME_DRIVER 
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('log-level=' + str(LOG_LEVEL))
    chrome_options.add_experimental_option('excludeSwitches',['enable-logging'])
    # Start headless chromedriver session.
    driver = webdriver.Chrome(chrome,options=chrome_options)
    driver.get(url)
    # Get cookies.
    cookies = driver.get_cookies()
    return(cookies)
# EOF

cookies = get_cookies(url)

# Randomize IP address with tor.
# pip install torrequest
def random_ip(password):
    ''' Reset tor to randomize your password given your tor hashed control
    password. Requires that you set HashedControlPassword in .torrc'''
    # Add hashed passwordexit()
    r=TorRequest(password)
    # Reset Tor.
    tr.reset_identity()
    # Check new ip.
    response= tr.get('http://ipecho.net/plain')
    print ("New IP Address",response.text)
# EOF

random_ip(password=TORPASS)
