# FROM:
# https://stackoverflow.com/questions/15316304/open-tor-browser-with-selenium

# Imports.
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# Paths to stuff.
torrc = '/mnt/c/Users/User/Downloads/Tor Browser/Browser/TorBrowser/Data/Tor'
firefox = '/mnt/c/Users/User/Downloads/Tor Browser/Browser/firefox.exe'
gecko = '/mnt/c/Program Files/Mozilla Firefox/geckodriver.exe'

# Set some privacy settings
profile = FirefoxProfile(torrc)
profile.set_preference( "places.history.enabled", False )
profile.set_preference( "privacy.clearOnShutdown.offlineApps", True )
profile.set_preference( "privacy.clearOnShutdown.passwords", True )
profile.set_preference( "privacy.clearOnShutdown.siteSettings", True )   
profile.set_preference( "privacy.sanitize.sanitizeOnShutdown", True )
profile.set_preference( "signon.rememberSignons", False )
profile.set_preference( "network.cookie.lifetimePolicy", 2 )
profile.set_preference( "network.dns.disablePrefetch", True )
profile.set_preference( "network.http.sendRefererHeader", 0 )
profile.set_preference( "javascript.enabled", False )

# set socks proxy
profile.set_preference( "network.proxy.type", 1 )
profile.set_preference( "network.proxy.socks_version", 5 )
profile.set_preference( "network.proxy.socks", '127.0.0.1' )
profile.set_preference( "network.proxy.socks_port", 9150 )
profile.set_preference( "network.proxy.socks_remote_dns", True )

# get a huge speed increase by not downloading images
profile.set_preference( "permissions.default.image", 2 )

# Other options:
options = Options()
options.set_headless(headless=True)

# Create driver.
binary = FirefoxBinary(firefox)
driver = webdriver.Firefox(firefox_binary=binary,
        firefox_profile=profile,
        executable_path=gecko,
        options=options)

driver.get("https://check.torproject.org/")




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
