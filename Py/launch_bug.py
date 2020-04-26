def launch_bug(url,executable_path,headless=False):
    # Create a chrome webdriver.
    # Options allow us to pass undetected by reCaptcha.
    # https://stackoverflow.com/questions/53039551/selenium-webdriver-modifying-navigator-webdriver-flag-to-prevent-selenium-detec/53040904#53040904
    # Imports.
    import sys
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    # Create options to be passed to webdriver.
    options = webdriver.ChromeOptions() 
    if headless:
        options.add_argument('--headless')
        options.add_argument('log-level=3')
        options.add_experimental_option('excludeSwitches',['enable-logging'])
    else:
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
    # EIF
    driver = webdriver.Chrome(options=options,executable_path=executable_path)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
      "source": """
          Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                        })
            """
            })
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browser1"}})
    driver.get(url)
    print("Launched chromium at: {}".format(url),file=sys.stderr)
    return driver
#EOF
