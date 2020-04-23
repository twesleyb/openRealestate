#!/bin/bash

# Need to pass cookies from webpage to wget.
zip_code="27310" 
url="https://www.zillow.com/homes/"$zip_code"_rb/"
wget -O "result.html" -x --load-cookies cookies.txt "$url"
