from selenium import webdriver
import os
import shutil
import datetime


def before_all(context):
    context.report_data = dict()
    context.new_prices = dict()
    try:
        shutil.rmtree(os.path.abspath('.\\Screenshots'))
        os.mkdir('.\\Screenshots')
    except FileNotFoundError:
        os.mkdir('.\\Screenshots')
    context.browser = webdriver.Chrome(os.path.abspath('chromedriver.exe'))
    context.browser.maximize_window()


def after_step(context, step):
    make_screen(context, step.name)


def make_screen(context, screen_name):
    short_name = screen_name[:7]
    time_now = datetime.datetime.now().strftime("%d-%m-%Y %H'%M''%S")
    context.browser.get_screenshot_as_file(os.path.abspath(f"./Screenshots/{short_name}_{time_now}.png"))
