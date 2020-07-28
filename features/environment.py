from selenium import webdriver
import os
import shutil
from datetime import datetime


def before_all(context):
    try:
        shutil.rmtree(os.path.abspath(r'.\Screenshots'))
    except FileNotFoundError:
        os.mkdir(r'.\Screenshots')
    context.driver = webdriver.Chrome(os.path.abspath('chromedriver.exe'))
    context.driver.maximize_window()


def after_step(context, step):
    make_screen(context, step.name)


def after_all(context):
    context.driver.quit()


def make_screen(context, screen_name):
    time_now = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
    context.browser.get_screenshot_as_file(os.path.abspath(rf'.\Screenshots\{screen_name}_{time_now}.png'))