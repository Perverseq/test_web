import sqlite3
import json


class Storage:
    prices_from_db = dict()
    actual_prices = dict()
    report_data = list()
    dividends = dict()
    loaded_from_json = list()
    scenario_results = dict()
    scenario_results_json = dict()

    def __init__(self):
        conn = sqlite3.connect(r'.\stocks')
        cursor = conn.cursor()
        for name, price in cursor.execute('SELECT * FROM stock_price'):
            self.prices_from_db[name] = price
        conn.close()

    def print_size(self):
        print(self.__sizeof__())

    def save_file(self, value, filename):
        with open(filename, 'r+', encoding='utf-8') as outfile:
            if filename == 'dividends.json':
                try:
                    self.dividends = json.load(outfile)
                    value.update(self.dividends)
                    outfile.seek(0)
                    outfile.truncate()
                except ValueError:
                    print('Dividens empty')
            json.dump(value, outfile, ensure_ascii=False)
