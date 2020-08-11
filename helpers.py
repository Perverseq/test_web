from selenium import webdriver
import os


def setup_browser(browser, headless):
    if browser == 'chrome':
        if headless == 'True':
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            browser_set = webdriver.Chrome(os.path.abspath('chromedriver.exe'), chrome_options=options)
            return browser_set
        else:
            browser_set = webdriver.Chrome(os.path.abspath('chromedriver.exe'))
            return browser_set
    elif browser == 'firefox':
        if headless == 'True':
            options = webdriver.FirefoxOptions()
            options.add_argument('headless')
            browser_set = webdriver.Firefox(executable_path=os.path.abspath('geckodriver.exe'), firefox_options=options)
            return browser_set
        else:
            browser_set = webdriver.Firefox(executable_path=os.path.abspath('geckodriver.exe'))
            return browser_set
