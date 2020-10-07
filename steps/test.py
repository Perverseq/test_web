from behave import *
from lib.pages import *
import json


@when('зайти на сайт "{site}"')
def step_impl(context, site):
    context.page = BasePage(context)
    context.page.visit(site)


@then('навести на "{element_name}" "{text}"')
def step_impl(context, element_name, text):
    context.page = MainPage(context)
    context.page.hover_element(context, element_name, text)


@then('нажать на "{element_name}" "{text}"')
def step_impl(context, element_name, text):
    context.page = MainPage(context)
    context.page.press_element(element_name, text)


@then('проверить наличие "{element_name}" "{value}"')
def step_impl(context, element_name, value):
    if element_name == "ошибка":
        context.page = MainPage(context)
    else:
        context.page = EquitiesPage(context)
    context.page.assert_page(element_name, value)


@then('собрать выросшие на "{percent}" процентов акции')
def step_impl(context, percent):
    context.page.gather_equities_prices(context)
    context.page.compare_equities_prices(context, percent)


@then('выгрузить "{value}" в "{filename}"')
def step_impl(context, value, filename):
    data = {'акции': context.storage.report_data,
            'дивиденды': context.storage.dividends}
    context.storage.save_file(data[value], filename)


@then('ввести в "{element_name}" "{value}"')
def step_impl(context, element_name, value):
    context.page = MainPage(context)
    context.page.input_data(element_name, value)


@then('очистить "{element_name}"')
def step_impl(context, element_name):
    context.page.clear_inputs(element_name)


@given('загрузить данные из "{filename}"')
def step_impl(context, filename):
    with open(filename, 'r', encoding='utf-8') as outfile:
        context.storage.loaded_from_json = list(json.load(outfile))


@then('перейти на страницу акции компании')
def step_impl(context):
    context.company = context.config.userdata.get('company', None)
    eq = WebDriverWait(context.browser, TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, f"//tr[starts-with(@id, 'pair')]//a[text()='{context.company}']")))
    print(f'xpath //tr[starts-with(@id, "pair")]//a[text()="{context.company}"]')
    eq.click()


@then('собрать дивиденды акции компании')
def step_impl(context):
    context.storage.dividends[context.company] = WebDriverWait(context.browser, TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH,
                '//*[@id="leftColumn"]//*[@class="inlineblock"]/span[text()="Дивиденды"]//following-sibling::*[1]'))
    ).text
