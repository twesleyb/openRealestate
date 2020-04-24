#!/usr/bin/env python3

import re
import sys

from lxml import html

import re
import subprocess

## Defaults:
TORPASS="torpass"
BASE_URL="https://www.zillow.com/"
DRIVER = '/home/twesleyb/bin/chromium/chromedriver.exe'

## Functions:
def get_pass(key):
    ''' Get password from password store. '''
    # Requirements:
    import re
    import subprocess
    cmd = ["pass",key]
    process = subprocess.Popen(cmd,stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
    output = process.communicate()
    password = re.split(" |\n",list(output)[0].decode('utf-8'))[1]
    return(password)
# EOF

def get_cookies(url,CHROME_DRIVER):
    ''' Get a websites cookies with Selenium. '''
    ## Default parameters.
    LOG_LEVEL = 3
    CHROME_DRIVER = '/home/twesleyb/bin/chromium/chromedriver.exe'
    # Chrome options and path to chromedriver.
    chrome = CHROME_DRIVER 
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('log-level=' + str(LOG_LEVEL))
    chrome_options.add_experimental_option('excludeSwitches',['enable-logging'])
    # Start headless chromedriver session.
    driver = webdriver.Chrome(chrome,options=chrome_options)
    driver.get(url)
    cookies = driver.get_cookies()
    return(cookies)
# EOF

def bake(cookie_dough):
    ''' Clean-up a cookies.txt file generated from Chrome extension, 
    and return a dictionary of key value pairs that is compatible with requests.
    From: https://stackoverflow.com/questions/14742899/using-cookies-txt-file-with-python-requests
    '''
    cookies = {}
    with open (cookie_dough, 'r') as fp:
        for line in fp:
            if not re.match(r'^\#', line):
                lineFields = line.strip().split('\t')
                if len(lineFields) == 7: 
                    cookies[lineFields[5]] = lineFields[6]
    return cookies
#EOF

def randomize_ip(password,quiet=False):
    ''' Randomize IP addredss with tor.
    Reset tor to randomize your IP address. Takes your tor hashed control
    password as an argument. Requires that you have set HashedControlPassword 
    variable in the tor configuration file.
    '''
    # Requirements
    import sys
    from torrequest import TorRequest
    # Add HashedControlPass.
    tr=TorRequest(password=password)
    # Reset Tor.
    tr.reset_identity()
    # Check new ip.
    response = tr.get('http://ipecho.net/plain')
    ip = response.text
    if not quiet:
        print("IP address is set to: {}".format(ip),file=sys.stderr)
    return(ip)
# EOF

def launch_bug(url,executable_path):
    # Create webdriver.
    # Options allow us to pass undetected by reCaptcha.
    # https://stackoverflow.com/questions/53039551/selenium-webdriver-modifying-navigator-webdriver-flag-to-prevent-selenium-detec/53040904#53040904
    # Imports.
    import sys
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    # Create options to be passed to webdriver.
    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options,executable_path=executable_path)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
      "source": """
          Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                        })
            """
            })
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browser1"}})
    driver.get(url)
    print("Launched chromium at {}".format(url),file=sys.stderr)
    return driver
#EOF

def scrape_zillow(driver,zip_code):
    url = "https://www.zillow.com/homes/{}_rb".format(zip_code)
    driver.get(url)
    html = driver.page_source
    return(html, driver)
#EOF

# Get HashedControlPassword from password store.
password = get_pass(TORPASS)

# Randomize IP address.
ip = randomize_ip(password)

# Launch chromium bug.
driver = launch_bug(url=BASE_URL,executable_path=DRIVER)

# Scrape a page.
zip_code = 10003
html, driver = scrape_zillow(driver,zip_code)

# Order of opperations:
# Randomize IP.
# Init webdriver
# Do captcha.
# Scrape html.
# Store in dictionary.
# Repeat.
data=list()

zip_code = 27519


url = BASE_URL.format(zip_code)
html = scrape(url)
data.append(html)

# Write data to file.
x = data[2]
f = open('27519.txt','w')
f.write(x)
f.close()

# Get a list of zip codes.
# FORMAT: {"zpid":"2080040202",
y = x.split('{"zpid":')


# Parse the html.
get_pass("torpass")

