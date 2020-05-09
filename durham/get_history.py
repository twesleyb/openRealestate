#!/usr/bin/env python3
''' Download report as pdf, convert it to text, and extract its key results. '''


import requests
from bs4 import BeautifulSoup

def get_history(parcel_id): 
    #EOF

parcel_id = 150621

# url to property page.
BASE_URL = 'https://property.spatialest.com/nc/durham/#/property/{}'
url = BASE_URL.format(parcel_id)

# Start requests session and get the page.
session = requests.Session()
page = session.get(url)
status = page.status_code

# Parse with bs4.
soup = BeautifulSoup(page.content,"html")

import re
re
headers = soup.find_all(re.compile(r'h\d+'))

soup.find_all("class", {'class' : 'data-list-section'})
