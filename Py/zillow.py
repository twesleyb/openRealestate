#!/usr/bin/env python3

import re
import argparse
import requests
from lxml import html
import unicodecsv as csv

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
    ''' Clean-up cookie.txt generated from Chrome extension.
    From: https://stackoverflow.com/questions/14742899/using-cookies-txt-file-with-python-requests
    Returns a dictionary of key value pairs compatible with requests.'''
    cookie = {}
    with open (cookie_dough, 'r') as fp:
        for line in fp:
            if not re.match(r'^\#', line):
                lineFields = line.strip().split('\t')
                if len(lineFields) == 7: 
                    cookie[lineFields[5]] = lineFields[6]
    return cookie

def parse(zipcode,filter=None):
    ''' Do the scraping.  '''
    if filter=="newest":
        url = "https://www.zillow.com/homes/for_sale/{0}/0_singlestory/days_sort".format(zipcode)
    elif filter == "cheapest":
        url = "https://www.zillow.com/homes/for_sale/{0}/0_singlestory/pricea_sort/".format(zipcode)
    else:
        url = "https://www.zillow.com/homes/for_sale/{0}_rb/?fromHomePage=true&shouldFireSellPageImplicitClaimGA=false&fromHomePageTab=buy".format(zipcode)
    
    for i in range(5):
        # try:
        session = requests.Session()
        response = session.get(url,headers=HEADERS,cookies=cookies)
        print(response.status_code)
        parser = html.fromstring(response.text)
        search_results = parser.xpath("//div[@id='search-results']//article")
        properties_list = []
        # Loop: 
        for properties in search_results:
            raw_address = properties.xpath(".//span[@itemprop='address']//span[@itemprop='streetAddress']//text()")
            raw_city = properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressLocality']//text()")
            raw_state= properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressRegion']//text()")
            raw_postal_code= properties.xpath(".//span[@itemprop='address']//span[@itemprop='postalCode']//text()")
            raw_price = properties.xpath(".//span[@class='zsg-photo-card-price']//text()")
            raw_info = properties.xpath(".//span[@class='zsg-photo-card-info']//text()")
            raw_broker_name = properties.xpath(".//span[@class='zsg-photo-card-broker-name']//text()")
            url = properties.xpath(".//a[contains(@class,'overlay-link')]/@href")
            raw_title = properties.xpath(".//h4//text()")
            # Extract key data. 
            address = ' '.join(' '.join(raw_address).split()) if raw_address else None
            city = ''.join(raw_city).strip() if raw_city else None
            state = ''.join(raw_state).strip() if raw_state else None
            postal_code = ''.join(raw_postal_code).strip() if raw_postal_code else None
            price = ''.join(raw_price).strip() if raw_price else None
            info = ' '.join(' '.join(raw_info).split()).replace(u"\xb7",',')
            broker = ''.join(raw_broker_name).strip() if raw_broker_name else None
            title = ''.join(raw_title) if raw_title else None
            property_url = "https://www.zillow.com"+url[0] if url else None 
            is_forsale = properties.xpath('.//span[@class="zsg-icon-for-sale"]')
            properties = {
                            'address':address,
                            'city':city,
                            'state':state,
                            'postal_code':postal_code,
                            'price':price,
                            'facts and features':info,
                            'real estate provider':broker,
                            'url':property_url,
                            'title':title
            }
            if is_forsale:
                properties_list.append(properties)
        return properties_list
        # except:
        #     print ("Failed to process the page",url)

if __name__=="__main__":
    argparser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    argparser.add_argument('zipcode',help = 'zipcode to be scraped')
    argparser.add_argument('cookies',help = 'cookie.txt file to be used.')
    sortorder_help = """
    available sort orders are :
    newest : Latest property details,
    cheapest : Properties with cheapest price
    """
    argparser.add_argument('sort',nargs='?',help = sortorder_help,default ='Homes For You')
    args = argparser.parse_args()
    zipcode = args.zipcode
    cookies = bake(args.cookies)
    sort = args.sort
    print ("Fetching data for %s"%(zipcode))
    scraped_data = parse(zipcode,sort)
    print ("Writing data to output file")
    with open("properties-%s.csv"%(zipcode),'wb')as csvfile:
        fieldnames = ['title','address','city','state','postal_code','price','facts and features','real estate provider','url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in  scraped_data:
            writer.writerow(row)
# DONE
