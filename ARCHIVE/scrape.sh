#!/bin/bash

# Need to pass cookies from webpage to wget.
url="https://www.zillow.com/greensboro-nc/"
#zip_code="27310" 
#url="https://www.zillow.com/homes/"$zip_code"_rb/"
#https://www.zillow.com/homes/oak-ridge_rb/
wget -O "result.html" -x --load-cookies cookies.txt "$url"
