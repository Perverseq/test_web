from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import json
TIMEOUT = 60


@when('зайти на сайт "{site}"')
def step_impl(context, site):
    context.browser.get(site)


@then('навести на "{element_name}" "{text}"')
def step_impl(context, element_name, text):
    drop_lists = {'Котировки': '//*[@class="nav"][text()="Котировки"]',
                  'Акции': '//*[@href="/equities/"][text()="Акции"]'}
    pathes = {'выпадающий список': drop_lists}
    element = WebDriverWait(context.browser, TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, pathes[element_name][text])))
    hov = ActionChains(context.browser).move_to_element(element)
    hov.perform()


@then('нажать на "{element_name}" "{text}"')
def step_impl(context, element_name, text):
    articles = {'Россия': '//*[@href="/equities/russia"]',
                "Вход": "//*[@class='login bold']"}
    buttons = {"Вход": "//*[@class='newButton orange'][text()='Вход']"}
    pathes = {'пункт': articles,
              'кнопку': buttons}
    element = WebDriverWait(context.browser, TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, pathes[element_name][text])))
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
    for el in iter(WebDriverWait(context.browser, TIMEOUT).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tr[starts-with(@id, 'pair')]")))):
        eq_name = el.find_element_by_xpath(f".//a").text
        eq_price = el.find_element_by_xpath(f".//td[contains(@class, 'last')]").text
        context.new_prices[eq_name] = eq_price
    conn = sqlite3.connect(r'.\stocks')
    try:
        cursor = conn.cursor()
        for name, price in cursor.execute('SELECT * FROM stock_price'):
            price_now = float(context.new_prices[name].replace('.', '').replace(',', '.'))
            price_from_db = (float(price.replace('.', '').replace(',', '.')))
            if (price_now / price_from_db) > (1 + (int(percent) / 100)):
                context.report_data[name] = price_now
    finally:
        conn.close()


@then('выгрузить данные в "{filename}"')
def step_impl(context, filename):
    with open(filename, 'w') as outfile:
        json.dump(context.report_data, outfile)


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
    el = WebDriverWait(context.browser, TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, inputs[element_name])))
    el.send_keys(value)


@then('очистить "{element_name}"')
def step_impl(context, element_name):
    inputs = {"Поле логина": 'loginFormUser_email',
              "Поле пароля": 'loginForm_password'}
    context.browser.find_element_by_id(inputs[element_name]).clear()
