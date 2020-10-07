import sqlite3
import json


class Storage:
    prices_from_db = dict()         # цены на акции из базы
    actual_prices = dict()          # цены на акции с сайта
    report_data = list()            # названия компаний с выросшими акциями
    dividends = dict()              # дивиденды
    scenario_results = dict()       # информация о сценариях
    scenario_results_json = dict()  # информация о сценариях из json

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
