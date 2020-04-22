#!/bin/bash

# How often do we need to retrieve cookies?
#zip_code="27514" #works
#zip_code="27704" #works
zip_code="27310" # not work at 6:58-59
url="https://www.zillow.com/homes/"$zip_code"_rb/"
wget -O "result.html" -x --load-cookies cookies.txt "$url"
