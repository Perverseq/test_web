from behave import *
from lib.pages import *
from helpers import close_small_banner
import time


@when('зайти на сайт "{site}"')
def step_impl(context, site):
    context.page = BasePage(context)
    context.page.visit(site)
    close_small_banner(context)


@then('навести на "{element_name}" "{text}"')
def step_impl(context, element_name, text):
    context.page = MainPage(context)
    context.page.hover_element(context, element_name, text)


@then('нажать на "{element_name}" "{text}"')
def step_impl(context, element_name, text):
    context.page = MainPage(context)
    context.page.press_element(context, element_name, text)


@then('проверить "{element_name}" "{value}"')
def step_impl(context, element_name, value):
    if element_name == "ошибка":
        context.page = MainPage(context)
    else:
        context.page = EquitiesPage(context)
    context.page.assert_page(context, element_name, value)


@then('собрать выросшие на "{percent}" процентов акции')
def step_impl(context, percent):
    context.page.gather_equities_prices(context)
    context.page.compare_equities_prices(context, percent)


@then('выгрузить данные в "{filename}"')
def step_impl(context, filename):
    context.page.save_json_file(context, filename)


@then('ввести в "{element_name}" "{value}"')
def step_impl(context, element_name, value):
    context.page = MainPage(context)
    context.page.input_data(context, element_name, value)


@then('очистить "{element_name}"')
def step_impl(context, element_name):
    context.page.clear_inputs(context, element_name)


@when('загрузить данные из "{filename}"')
def step_impl(context, filename):
    with open(filename, 'r', encoding='utf-8') as outfile:
        context.newnew_prices = list(json.load(outfile).items())


@then("собрать дивиденды акций")
def step_impl(context):
    while context.newnew_prices:
        for data in context.newnew_prices:
            eq = WebDriverWait(context.browser, TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, f"//tr[starts-with(@id, 'pair')]//a[text()='{data[0]}']")))
            eq.click()
            close_small_banner(context)
            context.dividends[data[0]] = WebDriverWait(context.browser, TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH,
                '//*[@id="leftColumn"]//*[@class="inlineblock"]/span[text()="Дивиденды"]//following-sibling::*[1]'))
                        ).text
            context.newnew_prices.remove(data)
            context.browser.back()
            close_small_banner(context)


@then('выгрузить дивиденды в "{filename}"')
def step_impl(context, filename):
    with open(filename, 'w', encoding='utf-8') as outfile:
        json.dump(context.dividends, outfile, ensure_ascii=False)
