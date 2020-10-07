import subprocess
import json
import timeit
from helpers import create_file, create_dir
from multiprocessing import Pool


def start_serial(tag):
    cmd = f'behave --no-skipped --no-capture -t {tag}'
    subprocess.Popen(cmd).communicate()


def start_parallel(company):
    cmd = f'behave --no-skipped --no-capture -t @threads --define company="{company}"'
    subprocess.Popen(cmd).communicate()


if __name__ == '__main__':
    create_dir('.\\Screenshots')
    create_file(".\\report.json")
    create_file(".\\result.json")
    create_file(".\\dividends.json")
    start_serial('@first')
    start_time = timeit.default_timer()
    with open('.\\report.json', 'r', encoding='utf-8') as outfile:
        loaded_from_json = list(json.load(outfile))
    with Pool(4) as p:
        p.map(start_parallel, loaded_from_json)
    elapsed = timeit.default_timer() - start_time
    start_serial('@third')
    start_serial('@fourth')
    with open('.\\result.json', 'r+', encoding='utf-8') as outfile:
        scenario_results_json = json.load(outfile)
        scenario_results_json['Сбор информации о дивидендах'][2] = str(elapsed)
        outfile.seek(0)
        outfile.truncate()
        json.dump(scenario_results_json, outfile, ensure_ascii=False)
