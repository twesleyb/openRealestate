#!/usr/bin/env python3

import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import requests
from torrequest import TorRequest

from lxml import html

## Defaults:
BASE_URL = "https://www.zillow.com/homes/{0}_rb/"
TORPASS='16:84205A404D64FF5F60EB72627A012BB308919ACA14AB093C6F9379EAD7'
HEADERS = {
        'authority' : 'https://www.zillow.com/',
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'accept-encoding':'gzip, deflate, sdch, br',
        'accept-language':'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
        'referer': 'https://www.zillow.com/',
        'cache-control':'max-age=10',
        'upgrade-insecure-requests':'1',
        'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }

def get_cookies(url):
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

def randomize_ip(HashedControlPassword):
    ''' Randomize IP addredss with tor.
    Reset tor to randomize your IP address. Takes your tor hashed control
    password as an argument. Requires that you have set HashedControlPassword 
    variable in the tor configuration file.'''
    # Add hashed passwordexit()
    tr=TorRequest(password=HashedControlPassword)
    # Reset Tor.
    tr.reset_identity()
    # Check new ip.
    response = tr.get('http://ipecho.net/plain')
    ip = response.text
    return(ip)
# EOF

def scrape(url):
    ## Default parameters.
    DRIVER = '/home/twesleyb/bin/chromium/chromedriver.exe'
    # Create webdriver.
    # Options allow us to pass undetected by reCaptcha.
    # https://stackoverflow.com/questions/53039551/selenium-webdriver-modifying-navigator-webdriver-flag-to-prevent-selenium-detec/53040904#53040904
    options = webdriver.ChromeOptions() 
    #options.add_argument("--headless")
    options.add_argument('log-level=' + str(LOG_LEVEL))
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options,executable_path=DRIVER)
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
    html = driver.page_source
    return(html)
#EOF

# Order of opperations:
# Randomize IP.
# Init webdriver
# Do captcha.
# Scrape html.
# Store in dictionary.
# Repeat.
data=list()

zip_code = 27519
ip = randomize_ip(TORPASS)
print("IP address is set to: {}".format(ip))
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

