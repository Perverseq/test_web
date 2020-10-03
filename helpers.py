from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
import os
import shutil

#
# def close_small_banner(context):
#     try:
#         WebDriverWait(context.browser, 5).until(
#             EC.presence_of_element_located((By.XPATH, "//*[@class='js-promotion-popup-close closePopup']"))).click()
#     except:
#         print("Маленький баннер не появился.")


def make_screen(context, screen_name):
    short_name = screen_name[:7]
    time_now = datetime.datetime.now().strftime("%d-%m-%Y %H'%M''%S")
    context.browser.get_screenshot_as_file(os.path.abspath(f"./Screenshots/{short_name}_{time_now}.png"))


def create_dir(path):
    if os.path.exists(path):
        shutil.rmtree(os.path.abspath(path))
    os.mkdir(path)


def create_file(path):
    if os.path.exists(path):
        os.remove(path)
    with open(path, 'w', encoding='utf-8'):
        print("Result file was created.")
