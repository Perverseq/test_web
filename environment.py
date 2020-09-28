from helpers import make_screen, create_file, create_dir
from storage_class import Storage
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from behave import fixture
from selenium import webdriver
from behave import use_fixture
import json
from multiprocessing import Process
from subprocess import Popen


@fixture
def browser(context):
    browser_name = context.config.userdata.get('browser', 'chrome')
    headless = context.config.userdata.get('headless', 'False')
    if browser_name == 'chrome':
        options = ChromeOptions()
        if headless == "True":
            options.add_argument("headless")
            print("Chrome will start in headless mode")
        print('\n Starting Chrome for test...')
        context.browser = webdriver.Chrome(options=options)
    elif browser_name == 'firefox':
        options = FirefoxOptions()
        if headless == "True":
            options.add_argument("--headless")
            print("Firefox will start in headless mode")
        else:
            context.browser = webdriver.Firefox(options=options)
            print('\n Starting Firefox for test...')
    else:
        raise
    yield context.browser
    print("\nQuit browser...")
    context.browser.quit()


def before_tag(context, tag):
    if tag == "threads":
        try:
            with open('.\\report.json', 'r', encoding='utf-8') as outfile:
                context.storage.loaded_from_json = list(json.load(outfile).keys())
                print(context.storage.loaded_from_json)
        except ValueError: #
            print('Json file is empty.')
        for context.company in context.storage.loaded_from_json:
            print(context.company)
            Popen(f'behave -tags="@threads" features/dividends.feature')
    if tag == "browser":
        use_fixture(browser, context)


def before_all(context):
    context.storage = Storage()
    create_dir('.\\Screenshots')
    create_file(".\\result.json")
    create_file(".\\dividends.json")


def after_step(context, step):
    make_screen(context, step.name)


def after_scenario(context, scenario):
    steps_amount = len(scenario.steps)
    context.storage.scenario_results[scenario.name] = [str(scenario.status)[7:], steps_amount, str(scenario.duration)]


def after_all(context):
    context.storage.save_file(context.storage.scenario_results, '.\\result.json')
