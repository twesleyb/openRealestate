#!/usr/bin/env python3

import os
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def launch_gecko(gecko_path, firefox_path, download_dir = os.getcwd(), 
        url=None, headless=False):

    # Options:
    options = Options()
    # 
    if headless:
        options.add_argument('--headless')
    # Profile settings:
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", download_dir)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
            "application/x-gzip")
    # Create driver.
    driver = webdriver.Firefox(executable_path=gecko_path, 
            options = options, firefox_profile=profile)
    # Navigate to specified url.
    if url is not None:
        driver.get(url)
        print("Launched gecko at: {}".format(url),file=sys.stderr)
    # Return the driver.
    return(driver)
#EOF

