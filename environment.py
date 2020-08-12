import os
import shutil
import datetime
from helpers import setup_browser, Storage


def before_all(context):
    context.storage = Storage()
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
    steps_amount = len(scenario.steps)
    context.storage.scenario_results[scenario.name] = [str(scenario.status)[7:], steps_amount, str(scenario.duration)]


def make_screen(context, screen_name):
    short_name = screen_name[:7]
    time_now = datetime.datetime.now().strftime("%d-%m-%Y %H'%M''%S")
    context.browser.get_screenshot_as_file(os.path.abspath(f"./Screenshots/{short_name}_{time_now}.png"))


def after_all(context):
    context.storage.save_file(context.storage.scenario_results, '.\\result.json')
    context.browser.close()
