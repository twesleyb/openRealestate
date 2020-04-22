#!/usr/bin/env python3

# Using selenium.

import os
import re
import sys
import json
from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

## Default parameters.
LOG_LEVEL = 3
META_EXTENSION = ".json"
DATA_EXTENSION = ".tsv.gz"
BASEURL = "https://cells.ucsc.edu/"
CHROME_DRIVER = "/home/twesleyb/src/chromedriver.exe"

# Chrome options and path to chromedriver.
chrome = CHROME_DRIVER 
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('log-level=' + str(LOG_LEVEL))
chrome_options.add_experimental_option('excludeSwitches',['enable-logging'])

# Start headless chromedriver session.
driver = webdriver.Chrome(chrome,options=chrome_options)
driver.get(BASEURL)

# All dataset buttons.
# While loop to insure that we successfully collect buttons.
buttons = []
while len(buttons) <= 0:
    buttons = driver.find_elements_by_class_name('list-group-item')
# Iterate through buttons, get page source data.
soup = list()
for button in buttons:
    button.click()
    soup.append(BeautifulSoup(driver.page_source,"xml"))

