def scrape_zillow(driver,zip_code):
    url = "https://www.zillow.com/homes/{}_rb".format(zip_code)
    driver.get(url)
    html = driver.page_source
    return(html, driver)
#EOF
