#!/usr/bin/env python3

# Using selenium + tor.
# Install with tbselenium with pip. Insure that you use the pip in your virtual
# environment.
# $ $(which pip) install tbselenium

# Paths to stuff.
# I tried putting geck on the Linux side of things and adding it to my path, but
# this didn't work...
#tor = '/mnt/c/oprojects/zillow_scraper/extensions/tor-browser_en-US'

tor = '/mnt/c/Users/User/Downloads/Tor Browser/Browser'
firefox = '/mnt/c/Program Files/Mozilla Firefox/firefox.exe'


# Selenium + tor
#tor="/usr/bin/tor"
#tor="/usr/sbin/tor"
#tor="/etc/tor"
tor="/usr/share/tor"
#tor="/usr/share/man/man1/tor.1.gz"
from tbselenium.tbdriver import TorBrowserDriver
with TorBrowserDriver(tor) as driver:
    driver.get('https://check.torproject.org')

## Driving tor with selenium.

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# Paths to tor-firefox and geckodriver.
firefox = '/mnt/c/Users/User/Downloads/Tor Browser/Browser/firefox.exe'
gecko = '/mnt/c/Program Files/Mozilla Firefox/geckodriver.exe'

driver = webdriver.Firefox(firefox_binary=binary,executable_path=gecko)

driver = webdriver.Firefox(executable_path=gecko)

# Create webdriver.
binary = FirefoxBinary(firefox)
driver = webdriver.Firefox(firefox_binary=binary,executable_path=gecko)

# Results in an ERROR :
# SessionNotCreatedException: Message: Unable to find a matching set of capabilities

# But this works...
driver = webdriver.Firefox(executable_path=gecko)
url="https://www.google.com/"
driver.get(url)

# But, it isn't through tor.
driver.get('https://check.torproject.org')
