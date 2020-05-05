#!/usr/bin/env python3

import os
import subprocess

def zzz(t=None,tmin=1,tmax=1.5):
    ''' Take a nap. '''
    import random
    from time import sleep
    if t is None:
        t = random.uniform(tmin,tmax)
    sleep(t)
#EOF

def get_report_url(driver,result=0):
    ''' Get supplemental data associated with an address.
    NOTE: Utilizes wget and pdftotext command line utilities.'''
    # Find parcel report by number.
    button = driver.find_element_by_id("report{}".format(result))
    # Open report in a new tab.
    button.click()
    zzz(5)
    # Switch to new tab and get its url.
    driver.switch_to.window(driver.window_handles[-1])
    zzz()
    url=driver.current_url
    # Close the tab and switch back to main window.
    driver.close()
    zzz()
    driver.switch_to.window(driver.window_handles[-1])
    return(url)
# EOF
