import sqlite3
import json


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
