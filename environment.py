from helpers import make_screen
from storage_class import Storage
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from behave import fixture
from selenium import webdriver
from behave import use_fixture
import json


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
        print('\n Starting Firefox for test...')
        context.browser = webdriver.Firefox(options=options)
    else:
        raise
    yield context.browser
    print("\nQuit browser...")
    context.browser.quit()


def before_tag(context, tag):
    if tag == "browser":
        use_fixture(browser, context)


def before_all(context):
    context.storage = Storage()


def after_step(context, step):
    make_screen(context, step.name)


def after_scenario(context, scenario):
    steps_amount = len(scenario.steps)
    context.storage.scenario_results[scenario.name] = [str(scenario.status)[7:], steps_amount, str(scenario.duration)]


def after_all(context):
    # сохраняем результаты по сценариям в отчет
    with open('.\\result.json', 'r+', encoding='utf-8') as outfile:
        print(context.storage.scenario_results)
        try:
            context.storage.scenario_results_json = json.load(outfile)
            context.storage.scenario_results.update(context.storage.scenario_results_json)
            outfile.seek(0)
            outfile.truncate()
        except ValueError:
            print('results empty')
        json.dump(context.storage.scenario_results, outfile, ensure_ascii=False)
