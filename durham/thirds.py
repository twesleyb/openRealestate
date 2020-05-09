#!/usr/bin/env python3
''' It's so easy. '''

from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.firefox.options import Options

# Additional imports
from utils.zzz import *
#from scrape.launch_gecko import *
from scrape.load_durham_addresses import *
from scrape.find_address import *

# When you launch your Firefox browser, it loads your save preferences.
# On Windows these are often found in %APPDATA%\Mozilla\Firefox\Profiles\.

# By default Firefox will prompt you when downloading a file.
# After changing this setting, your handlers.json file will be modified.

# Initially nothing is in the profile directory.
# When you launch the driver, user.js is created.

# What are the minimum requirements for a profile?

## Input parameters:
# NOTE: Firefox executable needs to be in the same directory as geckodriver, 
# or set as en environmental variable. (Is it set on Windows side?)
gecko = '/mnt/c/Program Files/Mozilla Firefox/geckodriver.exe'
addr_data = '/home/twesleyb/projects/open-realestate/data/durham.csv'
output_json = '/home/twesleyb/open-realestate/data/durham-realestate.json'
output_err = '/home/twesleyb/open-realestate/data/durham-not-found.json'

## Create firefox profile.
# NOTE: (1) Calls to FirefoxProfile() create a temporary firefox profile, 
# which is saved in /tmp/. e.g.: /tmpt/tmpizzfipxs
# You can see its path with: profile.path
# NOTE: (2) You can pass a path to FirefoxProfile.
# If you do this, a temporary copy of the profile is made. For example,
# > profile.path
# '/tmp/tmpvo_h1gzw/webdriver-py-profilecopy'

profile = FirefoxProfile('/home/twesleyb/downloads/myprofile/')

#profile.set_preference("browser.download.folderList", 2)
#profile.set_preference("browser.download.dir",'/mnt/d/projects/downloads')
#profile.set_preference("browser.download.panel.shown", False)
#profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
#        "text/csv;application/vnd.ms-excel;application/msword")
#profile.update_preferences()

## Create firefox options.
options = Options()
#options.add_argument('--headless')

## Create webdriver.
driver = webdriver.Firefox(executable_path=gecko,
        options=options,firefox_profile=profile)

## Navigate to durham gomaps
gomaps = 'http://maps2.roktech.net/durhamnc_gomaps4/'
driver.get(gomaps)

## Load address list.
addr_list = load_durham_addresses(addr_data)

## Get an address.
address = addr_list[0]

# Search for address.
response = find_address(driver,address)

# Check response.
response

# Increase buffer distance.
#add_buffer(driver,buffer_dist=1000)

# Download results.
driver.find_element_by_id('exportToExcelbtn').click()


def add_buffer(driver,buffer_dist=500):
    ''' Add buffer distance to current search results. '''
    from time import sleep
    # Open buffer input box.
    button = driver.find_element_by_id("buffer0")
    button.click(); sleep(5)
    # Drop down - select parcels.
    drop_down = driver.find_element_by_id("activeLayersBuffer")
    xpath = "//select[@name='activeLayersBuffer']/option[text()='Parcels']"
    drop_down.find_element_by_xpath(xpath).click(); sleep(1)
    driver.find_element_by_id("buferdistance").send_keys(buffer_dist)
    sleep(1)
    driver.find_element_by_id("buffersearchbtn").click()
    sleep(5)
    # Number of results.
    n = int(driver.find_element_by_id("numberofResults").text.split(" ")[0])
    return n
# EOF

def export_results(driver):
    ''' Downloads results for currently selected parcels. '''
    from time import sleep
    # Download results.
    button = driver.find_element_by_id('exportToExcelbtn')
    button.click()
    sleep(3)
# EOF

 # Get html source.
 html = driver.page_source
 # Parse with bs4.
 soup = BeautifulSoup(html,'html')

table = soup.find_all('div', attrs={'id':'keyinformation'})
table = soup.find_all('div', attrs={'id':'keyinformation'})

foo = soup.find_all('li', attrs = {'class':'clearfix data-list-row'})
x = foo[1]
x.find_all('span',attrs = {'class':'title'})
x.find_all('span',attrs = {'class':'value'})




# Loop through address list, scrape report data.
while len(addr_list) > 0:
    # Status report.
    address = addr_list.pop(0)
    msg = ' '.join([address.get('NUMBER'), address.get('STREET'),
        address.get('CITY'), address.get('POSTCODE')])
    print('Searching for: {}...'.format(msg),file=sys.stderr)
    # Search for an address.
    response = find_address(driver,address)
    # If address was not found--skip loop iteration.
    if response is None:
        # Append address to file.
        append_results(address,output_err)
        driver.refresh()
        zzz()
        continue # skips current iteration.
    # Status:
    print("Address found. Collecting parcel report...\n",file=sys.stderr)
    results = get_report(driver)
    # Add to address dictionary.
    address.update(results)
    # Append results to json file.
    append_results(address, output_json)
    # Rinse and repeat.
    driver.refresh()
# EOL
