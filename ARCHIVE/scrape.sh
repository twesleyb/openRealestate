#!/bin/bash

# Need to pass cookies from webpage to wget.
zip_code="27310" 
url="https://www.zillow.com/homes/"$zip_code"/"

echo "Scraping data from: $url"
torify wget --quiet -O "result.html" -x --load-cookies cookies.txt "$url"
#torify wget -x --load-cookies cookies.txt -H -r --level=5 --restrict-file-names=windows --convert-links -e robots=off $url
