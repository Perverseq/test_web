from selenium.webdriver.common.by import By
from .base_page import BasePage
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
TIMEOUT = 60

class EquitiesPage(BasePage):
    titles = {"Россия - акции": (By.XPATH, "//*[contains(text(), 'Россия - акции')]")}

    pathes = {"заголовок": titles}

    def __init__(self, context):
        BasePage.__init__(self, context, base_url='https://ru.investing.com/equities/russia')

    def assert_page(self, element_name, value):
        assert self.find_element(*self.pathes[element_name][value])

    def save_json_file(self, context, filename):
        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(context.report_data, outfile, ensure_ascii=False)

    def gather_equities_prices(self, context):
        for el in iter(WebDriverWait(context.browser, TIMEOUT).until(
                EC.presence_of_all_elements_located((By.XPATH, "//tr[starts-with(@id, 'pair')]")))):
            eq_name = el.find_element_by_xpath(f".//a").text
            eq_price = el.find_element_by_xpath(f".//td[contains(@class, 'last')]").text
            context.new_prices[eq_name] = eq_price

    def compare_equities_prices(self, context, percent):
        conn = sqlite3.connect(r'.\stocks')
        try:
            cursor = conn.cursor()
            for name, price in cursor.execute('SELECT * FROM stock_price'):
                price_now = float(context.new_prices[name].replace('.', '').replace(',', '.'))
                price_from_db = (float(price.replace('.', '').replace(',', '.')))
                if (price_now / price_from_db) > (1 + (int(percent) / 100)):
                    context.report_data[name] = price_now
        finally:
            conn.close()
