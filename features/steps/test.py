from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import json
TIMEOUT = 60
NEW_PRICES = dict()


@when('зайти на сайт "{site}"')
def step_impl(context, site):
    context.browser.get(site)


@then('навести на "{element_name}" "{text}"')
def step_impl(context, element_name, text):
    drop_lists = {'Котировки': '//*[@class="nav"][text()="Котировки"]',
                  'Акции': '//*[@href="/equities/"][text()="Акции"]'}
    pathes = {'выпадающий список': drop_lists}
    element = WebDriverWait(context.browser, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, pathes[element_name][text])))
    hov = ActionChains(context.browser).move_to_element(element)
    hov.perform()


@then('нажать на "{element_name}" "{text}"')
def step_impl(context, element_name, text):
    articles = {'Россия': '//*[@href="/equities/russia"]',
                "Вход": "//*[@class='login bold']"}
    buttons = {"Вход": "//*[@class='newButton orange'][text()='Вход']"}
    pathes = {'пункт': articles,
              'кнопку': buttons}
    element = WebDriverWait(context.browser, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, pathes[element_name][text])))
    element.click()


@then('проверить "{element_name}" "{value}"')
def step_impl(context, element_name, value):
    titles = {"Россия - акции": "//*[contains(text(), 'Россия - акции')]"}
    errors = {"Ошибка логина": "//*[@data-tooltip='Пожалуйста, введите действительный электронный адрес']",
              "Ошибка пароля": "//*[@data-tooltip='Используйте 4-15 символов, включая как минимум 2 буквы и 2 цифры.']",
              "Ошибка данных": "//*[@id='serverErrors'][text()='Неверный логин или пароль, повторите попытку']"}
    pathes = {"заголовок": titles,
              "ошибка": errors}
    assert context.browser.find_element_by_xpath(pathes[element_name][value])


@then('собрать выросшие на "{percent}" процентов акции')
def step_impl(context, percent):
    prices = {"Lenta Ltd": "//td[@class='pid-962408-last']",
              "Polymetal": "//td[@class='pid-44465-last']",
              "Safmar Fin": "//td[@class='pid-962406-last']",
              "X5 Retail Group": "//td[@class='pid-1061926-last']",
              "АК АЛРОСА": "//td[@class='pid-40423-last']",
              "Аэрофлот": "//td[@class='pid-13679-last']",
              "Банк ВТБ": "//td[@class='pid-13725-last']",
              "Газпром": "//td[@class='pid-13684-last']",
              "Группа Компаний ПИК": "//td[@class='pid-13789-last']",
              "Группа ЛСР": "//td[@class='pid-13688-last']",
              "Детский мир": "//td[@class='pid-996169-last']",
              "Интер РАО ЕЭС ОАО": "//td[@class='pid-13744-last']",
              "ЛУКОЙЛ": "//td[@class='pid-13689-last']",
              "М.видео": "//td[@class='pid-13692-last']",
              "Магнит": "//td[@class='pid-13693-last']",
              "МКБ": "//td[@class='pid-955694-last']",
              "ММК ОАО": "//td[@class='pid-13690-last']",
              "Московская биржа": "//td[@class='pid-44464-last']",
              "МТС": "//td[@class='pid-13691-last']",
              "НЛМК ОАО": "//td[@class='pid-13695-last']",
              "НОВАТЭК": "//td[@class='pid-13697-last']",
              "Норильский никель": "//td[@class='pid-13683-last']",
              "Полюс": "//td[@class='pid-13705-last']",
              "Роснефть": "//td[@class='pid-13707-last']",
              "Ростелеком": "//td[@class='pid-21419-last']",
              "РУСАЛ": "//td[@class='pid-950026-last']",
              "РусГидро": "//td[@class='pid-13754-last']",
              "РуссНефть": "//td[@class='pid-32553-last']",
              "Сбербанк": "//td[@class='pid-13711-last']",
              "Сбербанк (прив.)": "//td[@class='pid-13712-last']",
              "Северсталь": "//td[@class='pid-13713-last']",
              "Система": "//td[@class='pid-13678-last']",
              "Сургутнефтегаз": "//td[@class='pid-13716-last']",
              "Сургутнефтегаз (прив.)": "//td[@class='pid-13717-last']",
              "Татнефть": "//td[@class='pid-13718-last']",
              "Татнефть (прив.)": "//td[@class='pid-13738-last']",
              "ТМК ОАО": "//td[@class='pid-21468-last']",
              "Транснефть (прив.)": "//td[@class='pid-13720-last']",
              "ФосАгро": "//td[@class='pid-21406-last']",
              "ФСК ЕЭС ОАО": "//td[@class='pid-13682-last']",
              "Юнипро": "//td[@class='pid-21302-last']",
              "Яндекс": "//td[@class='pid-102063-last']",
              }
    WebDriverWait(context.browser, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//td[@class='pid-102063-last']")))
    conn = sqlite3.connect(r'.\stocks')
    try:
        cursor = conn.cursor()
        for name, price in cursor.execute('SELECT * FROM stock_price'):
            WebDriverWait(context.browser, TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, prices[name])))
            price_now = float(context.browser.find_element_by_xpath(prices[name]).text.replace('.', '').replace(',', '.'))
            price_from_db = (float(price.replace('.', '').replace(',', '.')))
            if (price_now / price_from_db) > (1 + (int(percent) / 100)):
                NEW_PRICES[name] = price_now
    finally:
        conn.close()

# TODO: попробовать заменить словарь с xpath на "//tr[starts-with(@id, 'pair')]"


@then('выгрузить данные в "{filename}"')
def step_impl(context, filename):
    with open(filename, 'w') as outfile:
        json.dump(NEW_PRICES, outfile)


@then('закрыть "{text}" всплывающее окно')
def step_impl(context, text):
    pathes = {"большое": "//*[@class='popupCloseIcon largeBannerCloser']",
              "маленькое": "//*[@class='popupCloseIcon']"}
    el = WebDriverWait(context.browser, TIMEOUT).until(
        EC.visibility_of_element_located((By.XPATH, pathes[text])))
    el.click()


@then('ввести в "{element_name}" "{value}"')
def step_impl(context, element_name, value):
    inputs = {"Поле логина": 'loginFormUser_email',
              "Поле пароля": 'loginForm_password'}
    el = WebDriverWait(context.browser, TIMEOUT).until(EC.visibility_of_element_located((By.ID, inputs[element_name])))
    el.send_keys(value)


@then('очистить "{element_name}"')
def step_impl(context, element_name):
    inputs = {"Поле логина": 'loginFormUser_email',
              "Поле пароля": 'loginForm_password'}
    context.browser.find_element_by_id(inputs[element_name]).clear()
