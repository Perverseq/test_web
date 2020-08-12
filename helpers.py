from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os


def setup_browser(browser, headless):
    if browser == 'chrome':
        if headless == 'True':
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            browser_set = webdriver.Chrome(os.path.abspath('chromedriver.exe'), chrome_options=options)
        else:
            browser_set = webdriver.Chrome(os.path.abspath('chromedriver.exe'))
    elif browser == 'firefox':
        if headless == 'True':
            options = webdriver.FirefoxOptions()
            options.add_argument('headless')
            browser_set = webdriver.Firefox(executable_path=os.path.abspath('geckodriver.exe'), firefox_options=options)
        else:
            browser_set = webdriver.Firefox(executable_path=os.path.abspath('geckodriver.exe'))
    return browser_set


def close_small_banner(context):
    try:
        WebDriverWait(context.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[@class='js-promotion-popup-close closePopup']"))).click()
    except:
        print("Маленький баннер не появился.")