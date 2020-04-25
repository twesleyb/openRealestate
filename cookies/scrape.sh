#!/usr/bin/env bash

# Args.
cookies=$1

# Shorten url.
#long_url="https://www.zillow.com/oak-ridge-nc/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22oak%20ridge%20nc%22%2C%22mapBounds%22%3A%7B%22west%22%3A-80.11103640039154%2C%22east%22%3A-79.87973859960847%2C%22south%22%3A36.106240506607314%2C%22north%22%3A36.24065419576821%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A19713%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22mapZoom%22%3A12%2C%22filterState%22%3A%7B%7D%2C%22isListVisible%22%3Atrue%7D"
#url=$(shorten-url $long_url)
url="https://www.zillow.com/homes/oak-ridge_rb/"

# Scrape.
wget -O zillow.html --quiet -x --load-cookies $cookies "$url"
