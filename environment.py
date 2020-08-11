from selenium import webdriver
import os
import shutil
import datetime
import json
from helpers import setup_browser


def before_all(context):
    context.report_data = dict()
    context.new_prices = dict()
    context.scenario_results = dict()
    try:
        shutil.rmtree(os.path.abspath('.\\Screenshots'))
        os.mkdir('.\\Screenshots')
    except FileNotFoundError:
        os.mkdir('.\\Screenshots')
    try:
        os.remove(".\\result.json")
        with open(".\\result.json", 'w', encoding='utf-8'):
            print("Result file was created.")
    except FileNotFoundError:
        with open(".\\result.json", 'w', encoding='utf-8'):
            print("Result file was created.")
    context.browser = setup_browser(context.config.userdata.get('browser', 'chrome'),
                                    context.config.userdata.get('headless', 'False'))
    context.browser.maximize_window()


def after_step(context, step):
    make_screen(context, step.name)


def after_scenario(context, scenario):
    status = ''
    if str(scenario.status) == 'Status.passed':
        status = 'Passed'
    elif str(scenario.status) == 'Status.failed':
        status = 'Failed'
    elif str(scenario.status) == 'Status.skipped':
        status = 'Skipped'
    elif str(scenario.status) == 'Status.untested':
        status = 'Untested'
    steps_amount = len(scenario.steps)
    context.scenario_results[scenario.name] = [status, steps_amount, str(scenario.duration)]


def make_screen(context, screen_name):
    short_name = screen_name[:7]
    time_now = datetime.datetime.now().strftime("%d-%m-%Y %H'%M''%S")
    context.browser.get_screenshot_as_file(os.path.abspath(f"./Screenshots/{short_name}_{time_now}.png"))


def after_all(context):
    with open(".\\result.json", 'a', encoding='utf-8') as outfile:
        json.dump(context.scenario_results, outfile, ensure_ascii=False)
    context.browser.close()
