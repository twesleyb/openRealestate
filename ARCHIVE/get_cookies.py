def get_cookies(url,chromium_path):
    ''' Get a websites cookies with Selenium. '''
    ## Default parameters.
    LOG_LEVEL = 3
    # Chrome options and path to chromedriver.
    chrome = chromium_path 
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('log-level=' + str(LOG_LEVEL))
    chrome_options.add_experimental_option('excludeSwitches',['enable-logging'])
    # Start headless chromedriver session.
    driver = webdriver.Chrome(executable_path=chrome,options=chrome_options)
    driver.get(url)
    cookies = driver.get_cookies()
    return(cookies)
# EOF
