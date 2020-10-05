import os
import subprocess
import json
import timeit
from helpers import create_file, create_dir
from multiprocessing import Pool


def get_features():
    features = [os.path.join(os.path.abspath('features'), feature) for feature in os.listdir('features')]
    return features


def get_tags():
    tags = list()
    features = get_features()
    for feature in features:
        with open(feature) as f:
            tag_in_file = [tag for tag in (stroke.rstrip().lstrip() for
                                           stroke in f.readlines() if
                                           (stroke.rstrip().lstrip().startswith('@'))
                                           and stroke.rstrip().lstrip() not in ('@browser', '@bad'))]
            tags += tag_in_file
    return sorted(tags)


def timer(func):
    def wrapper(tag):
        start_time = timeit.default_timer()
        func(tag)
        elapsed = timeit.default_timer() - start_time
        return elapsed
    return wrapper


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
