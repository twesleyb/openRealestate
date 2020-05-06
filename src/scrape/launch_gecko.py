#!/usr/bin/env python3

import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def launch_gecko(gecko_path,headless=True):
    # Options:
    options = Options()
    if headless:
        options.add_argument('--headless')
    # Create driver.
    driver = webdriver.Firefox(executable_path=gecko_path, 
            options = options)
    if url is not None:
        driver.get(url)
        print("Launched gecko at: {}".format(url),file=sys.stderr)
    return(driver)
#EOF

