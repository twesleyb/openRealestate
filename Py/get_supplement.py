#!/usr/bin/env python3

def zzz(t=None,tmin=1,tmax=1.5):
    ''' Take a nap. '''
    import random
    from time import sleep
    if t is None:
        t = random.uniform(tmin,tmax)
    sleep(t)
#EOF

def get_supplement(driver,result=0,data_type="report"):
    ''' Get supplemental data associated with address.'''
    # Find parcel report or tax history by number.
    button = driver.find_element_by_id("{}{}".format(data_type,result))
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
# EOF.
