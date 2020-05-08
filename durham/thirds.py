#!/usr/bin/env python3
''' It's so easy. '''

## Parameters:
gecko = '/mnt/c/Program Files/Mozilla Firefox/geckodriver.exe'

# Imports
from bs4 import BeautifulSoup  

# Additional functions.
from scrape.launch_gecko import *
from scrape.load_durham_addresses import *
from scrape.find_address import *

## User parameters:
addr_data = '/home/twesleyb/projects/open-realestate/data/durham.csv'
output_json = '/home/twesleyb/open-realestate/data/durham-realestate.json'
output_err = '/home/twesleyb/open-realestate/data/durham-not-found.json'

# Load addresses.
addr_list = load_durham_addresses(addr_data)

# Launch gecko
driver = launch_gecko(gecko_path=gecko,headless=False)

# Get webpage.
url = 'http://maps2.roktech.net/durhamnc_gomaps4/'
driver.get(url)

address = addr_list[0]
response = find_address(driver,address)

# While loop n < 1000
# Increase buffer:
b = 500
# Open buffer input box.
button = driver.find_element_by_id("buffer0")
button.click()
# Drop down - select parcels.
drop_down = driver.find_element_by_id("activeLayersBuffer")
# sleep
drop_down.send_keys('Parcels')
# Set buffer distance.
driver.find_element_by_id("buferdistance").send_keys(b)
# Submit.
driver.find_element_by_id("buffersearchbtn").click()
# Number of results.
n = int(driver.find_element_by_id("numberofResults").text.split(" ")[0])

# Download results.
button = driver.find_element_by_id('exportToExcelbtn')
button.click()


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
