#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Defaults:
GECKO = '/mnt/d/projects/open-realestate/drivers/geckodriver.exe'
URL = 'http://maps2.roktech.net/durhamnc_gomaps4/'

# Options:
options = Options()
options.add_argument('--headless')

# Create driver.
driver = webdriver.Firefox(executable_path = GECKO, options = options)

# Get webpage.
driver.get(URL)

