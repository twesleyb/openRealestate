#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def launch_gecko(executable_path,headless=True):
    # Options:
    options = Options()
    if headless:
        options.add_argument('--headless')
    # Create driver.
    driver = webdriver.Firefox(executable_path, options = options)
    return(driver)
#EOF

