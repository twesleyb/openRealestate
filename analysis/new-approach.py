#!/usr/bin/env python3

import os
import sys
import importlib
from os.path import dirname

## Defaults:
TORPASS="torpass" # password store name
BASE_URL="https://www.zillow.com/"
DRIVER = '/home/twesleyb/bin/chromium/chromedriver.exe'

# Directories.
here = os.getcwd()
root = dirname(here)
sys.path.append(root)

# Load Functions in root/Py
import Py
from Py.get_pass import get_pass
from Py.check_ip import check_ip
from Py.randomize_ip import randomize_ip 
from Py.launch_bug import launch_bug

# Example: how to reload a module.
#importlib.reload(Py.get_pass)
#from Py.get_pass import get_pass

# Get HashedControlPassword from password store.
password = get_pass(TORPASS)

# Check ip address.
ip = check_ip()

# Get tor session.
session = tor_session(password)

#Launch chromium bug.
ipecho = 'http://ipecho.net/plain'
driver = launch_bug(url=ipecho,executable_path=DRIVER,headless=True)

# Launch chromium bug.
url='http://maps2.roktech.net/durhamnc_gomaps4/#'
driver = launch_bug(url,executable_path=DRIVER,headless=False)


