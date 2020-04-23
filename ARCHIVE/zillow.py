#!/usr/bin/env python3

import re
#import argparse
import requests
from lxml import html

# Parameters:
zip_code=27704
cookie_file = 'cookies.txt'
sort="newest"
url = "https://www.zillow.com/homes/for_sale/{0}/0_singlestory/days_sort".format(zip_code)

# Defaults:
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

def bake(cookie_dough):
    ''' Clean-up cookie.txt generated from the cookies.txt chrome extension.
    Adapted from: https://stackoverflow.com/questions/14742899/using-cookies-txt-file-with-python-requests
    Returns a dictionary of key value pairs that is compatible with requests.'''
    cookies = {}
    with open (cookie_dough, 'r') as fp:
        for line in fp:
            if not re.match(r'^\#', line): # discard lines starting with #
                lineFields = line.strip().split('\t')
                if len(lineFields) == 7:  # if less than 7 elements discard.
                    cookies[lineFields[5]] = lineFields[6]
    return cookies

# Connect to zillow.com.
cookies = bake(cookie_file)
session = requests.Session()
page = session.get(url,headers=HEADERS,cookies=cookies)
response = page.status_code

# Stop if there is a problem.
if response is not 200: 
    raise SystemExit('Error: Problem connecting to zillow.com.')

print(page.text)

import sys
sys.exit

# Parse webpage.
#soup = BeautifulSoup(page.content,"lxml")

parser = html.fromstring(page.text)

#parser.xpath("//div[@id='search-results']//article")

#roperties.xpath(".//span[@itemprop='address']//span[@itemprop='streetAddress']//text()")

