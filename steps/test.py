from behave import *
from lib.pages import *


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
    context.page.press_element(context, element_name, text)


@then('проверить "{element_name}" "{value}"')
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