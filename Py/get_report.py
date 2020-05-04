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

def get_report(driver,result=0):

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
    # Download report with wget.
    cmd = ["wget", "--quiet", "-O", ".temp.pdf", url]
    process = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    response = process.communicate()

    # Convert pdf to text.
    cmd = ['pdftotext','-raw','-nopgbrk','.temp.pdf', '.temp.txt']
    process = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    response = process.communicate()

    # Read converted file.
    f = open('.temp.txt','r')
    text = f.readlines()
    f.close()

text = [x for x in text if x != '\n'] # Drop '\n'
text = [x.strip('\n') for x in text] # Remove excess '\n'

# Coerce to single string.
string = ' '.join(text)

keys = ['PIN','Parcel ID','Acreage','Land Use','Land Value','Land Use',
        'Deed Book', 'Deed Page', 'Plat Book', 'Plat Page', 'Subdivision',
        'Land Value', 'Building Value', 'Total Value', 'Sale Price']

import re
delim = '|'.join(keys)
x = re.split(delim,string)
[string.split(key)[1].split(delim) for key in keys]

    # Parse the response.
    #text = text[3:-2] # Drop unnecessary elements.
    #text = [x.strip('\n') for x in text] # Remove excess \n

    # Collect key, value pairs.
    keys = text[::2] 
    vals = text[1::2]
    report = dict(zip(keys,vals))
    # Remove temporary files.
    os.remove('.temp.pdf')
    os.remove('.temp.txt')
    # Return parcel report.
    return(report)
# EOF.
