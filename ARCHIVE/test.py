#!/usr/bin/env python3

#--------------------------------------------------------------------
## Test 1.
#--------------------------------------------------------------------
# Driving tor with selenium + geckodriver.

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# Path to Tor-Firefox and geckodriver executables (Windows).
firefox = '/mnt/c/Users/User/Downloads/Tor Browser/Browser/firefox.exe'
gecko = '/mnt/c/Program Files/Mozilla Firefox/geckodriver.exe'

# Create the webdriver.
binary = FirefoxBinary(firefox)
driver = webdriver.Firefox(firefox_binary=binary,executable_path=gecko)

# ERROR :
# SessionNotCreatedException: Message: Unable to find a matching set of capabilities

# Show that geckodriver works...
driver = webdriver.Firefox(executable_path=gecko)
url="https://www.google.com/"
driver.get(url)

# But, it isn't tor.
driver.get('https://check.torproject.org')

#--------------------------------------------------------------------
## Test 2.
#--------------------------------------------------------------------
# Show that we can randomize ip with torreqeust.

import os
import sys
import requests
from os.path import dirname
from torrequest import TorRequest

# Directories.
here = os.getcwd()
root = dirname(here)
sys.path.append(root)

# Load Functions in root/Py
import Py
from Py.get_pass import get_pass

# Add HashedControlPass.
password = get_pass("torpass")
tr=TorRequest(password=password)

# Reset Tor.
tr.reset_identity()

# Check initial ip.
session = requests.session()
response = session.get('http://ipecho.net/plain')
ip = response.text
print("IP address is set to: {}".format(ip))

# Check new ip with tor.
response = tr.get('http://ipecho.net/plain')
ip = response.text
print("IP address is set to: {}".format(ip))

# Check if tor is active.
response = tr.get('https://check.torproject.org')
response.text # Sorry, you are not using Tor.

#--------------------------------------------------------------------
## Test 3.
#--------------------------------------------------------------------
# We can use torrify on the command line.

torify wget -O - 'https://check.torproject.org' 

# Congratulations. This browser is configured to use Tor.
