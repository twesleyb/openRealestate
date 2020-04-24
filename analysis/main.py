#!/usr/bin/env python3

import os
import sys
import importlib
from os.path import dirname

## Defaults:
TORPASS="torpass"
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
importlib.reload(Py.get_pass)
from Py.get_pass import get_pass

# Get HashedControlPassword from password store.
password = get_pass(TORPASS)

# Check ip address.
ip = check_ip()

# Start tor!
print("Start tor in another terminal!",file=sys.stderr)

# Randomize IP address.
ip = randomize_ip(password)

# Test: launch chromium bug.
ipecho = 'http://ipecho.net/plain'
driver = launch_bug(url=ipecho,executable_path=DRIVER,headless=True)

# Note, the IP for our bug is still the same!
# Need to pass torr session along...
session = tr.session
zillow='https://www.zillow.com/'
response = session.get(zillow)
response.status_code
response.text # We have been detected!
# Check session's ip address.
session.get(ipecho).text


zip_code = 27519
