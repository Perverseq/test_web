from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import sqlite3
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


class Storage:
    prices_from_db = dict()
    actual_prices = dict()
    report_data = dict()
    dividends = dict()
    loaded_from_json = list()
    scenario_results = dict()

    def __init__(self):
        conn = sqlite3.connect(r'.\stocks')
        cursor = conn.cursor()
        for name, price in cursor.execute('SELECT * FROM stock_price'):
            self.prices_from_db[name] = price
        conn.close()

    def print_size(self):
        print(self.__sizeof__())

    def save_file(self, value, filename):
        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(value, outfile, ensure_ascii=False)
