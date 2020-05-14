#!/usr/bin/env python3
""" Download report as pdf, convert it to text, and extract its key results. """

import os
import re
import sys
import subprocess


def zzz(t=None, tmin=1, tmax=1.5):
    """ Take a nap. """
    import random
    from time import sleep

    if t is None:
        t = random.uniform(tmin, tmax)
    sleep(t)


# EOF


def get_report_url(driver, result=0):
    """ Get url for the supplemental report associated with an address."""
    # Find parcel report by number.
    button = driver.find_element_by_id("report{}".format(result))
    # Open report in a new tab.
    button.click()
    zzz(5)
    # Switch to new tab and get its url.
    driver.switch_to.window(driver.window_handles[-1])
    zzz()
    url = driver.current_url
    # Close the tab and switch back to main window.
    driver.close()
    zzz()
    driver.switch_to.window(driver.window_handles[-1])
    return url


# EOF


def download_report(url, output_pdf=".temp.pdf"):
    """ Get supplemental data associated with an address."""
    # Download report with wget.
    cmd = ["wget", "--quiet", "-O", ".temp.pdf", url]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    response = process.communicate()
    stdout, stderr = [r.decode("utf-8").strip() for r in response]
    return stderr


def convert_report(input_pdf=".temp.pdf", output_txt=".temp.txt"):
    """ Convert report.pdf to report.text."""
    cmd = ["pdftotext", "-raw", "-nopgbrk", input_pdf, output_txt]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    response = process.communicate()
    stdout, stderr = [r.decode("utf-8").strip() for r in response]
    return stderr


# EOF


def get_kv_pair(string, key):
    """ Extract key-value pairs from a string. """
    value = string.split(key)[1].strip().split(" ")[0].strip()
    pair = {key: value}
    return pair


# EOF


def parse_report(input_text=".temp.txt"):
    """ Parse the text output of pdftotext. """
    # Read result from pdftotext.
    with open(input_text, "r") as myfile:
        text_list = myfile.readlines()
        myfile.close()
    # Coerce list to a single string.
    string = " ".join(text_list)
    # We will values for the following keys.
    keys = [
        "PIN",
        "Parcel ID",
        "Acreage",
        "Land Use",
        "Land Value",
        "Land Use",
        "Deed Book",
        "Deed Page",
        "Plat Book",
        "Plat Page",
        "Subdivision",
        "Land Value",
        "Building Value",
        "Total Value",
        "Sale Price",
    ]
    results_list = [get_kv_pair(string, key) for key in keys]
    results = {k: v for d in results_list for k, v in d.items()}
    return results


# EOF


def get_report(driver):
    """ Wrap-up all the work done above in a single function. """
    # Get report url.
    url = get_report_url(driver)
    # Download report as pdf.
    response = download_report(url)
    # Convert pdf report to text.
    response = convert_report()
    # Extract key-value pairs from text.
    results = parse_report()
    return results


# EOF
