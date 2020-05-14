#!/usr/bin/env python3
""" Default parameters. """

import os

## INPUT DATA:
CITY = "durham"
ROOT = "/home/twesleyb/projects/open-realestate/"
ADDR_DATA = os.path.join(ROOT, CITY, "addresses/{}.csv".format(CITY))

## WEBDRIVER PATHS:
PROFILE = "/home/twesleyb/projects/open-realestate/firefox-profile/"
DRIVER = "/mnt/c/Program Files/Mozilla Firefox/geckodriver.exe"

## GOMAPS URL:
GOMAPS = "http://maps2.roktech.net/durhamnc_gomaps4/"

## INTERMEDIATE FILES:
EXPORT_CSV = os.path.join(ROOT, "downloads/export.csv")

## OUTPUTS:
STDOUT = os.path.join(ROOT, CITY, "data/{}-realestate.json".format(CITY))
STDERR = os.path.join(ROOT, CITY, "data/{}-not-found.json".format(CITY))
