#!/usr/bin/env python3

import random
from time import sleep

import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def zzz(t=None,tmin=1,tmax=1.5):
    ''' Take a nap. '''
    if t is None:
        t = random.uniform(tmin,tmax)
    sleep(t)
#EOF

def launch_bug(chromium_path,url = None, headless=False):
    ''' Launch chromium webdriver. '''
    # Create options to be passed to webdriver.
    options=webdriver.ChromeOptions()
    # Download options.
    options.add_experimental_option("prefs", {
        'download.default_directory' : os.getcwd(),
        'profile.default_content_setting_values.automatic_downloads': 2,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True
        })
    # Headless options.
    if headless:
        options.add_argument('--window-size=1920,1080')  
        options.add_argument('--headless')
        options.add_argument('log-level=3')
        options.add_experimental_option('excludeSwitches',['enable-logging'])
    else:
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
    # Create driver.
    driver = webdriver.Chrome(options=options,executable_path=chromium_path)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
      "source": """
          Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                        })
            """
            })
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", 
            {"headers": {"User-Agent": "browser1"}})
    # Get webpage.
    if url is not None:
        driver.get(url)
        print("Launched chromium at: {}".format(url),file=sys.stderr)
    # EIS
    return(driver)
#EOF
