#!/usr/bin/env python3

import os
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def launch_gecko(
    gecko_path, firefox_profile=None, url=None, headless=False, log_path="/dev/null"
):
    """ Launch geckodriver at a specified url. """

    options = Options()

    if headless:
        options.add_argument("--headless")

    driver = webdriver.Firefox(
        executable_path=gecko_path,
        options=options,
        firefox_profile=firefox_profile,
        service_log_path=log_path,
    )

    if url is not None:
        driver.get(url)
        print("Launched gecko at: {}".format(url), file=sys.stderr)

    return driver


# EOF
