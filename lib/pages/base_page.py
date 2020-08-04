from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import traceback


class BasePage(object):
    locators_dictionary = {
        "ru.investing.com": "https://ru.investing.com/"}

    def __init__(self, context, base_url='http://www.seleniumframework.com'):
        self.base_url = base_url
        self.browser = context.browser
        self.timeout = 10

    def find_element(self, *loc):
        return self.browser.find_element(*loc)

    def find_elements(self, *loc):
        return self.browser.find_elements(*loc)

    def visit(self, text):
        self.browser.get(self.locators_dictionary[text])

    def __getattr__(self, what):
        try:
            if what in self.locator_dictionary.keys():
                try:
                    _element = WebDriverWait(self.browser, self.timeout).until(
                        EC.presence_of_element_located(self.locator_dictionary[what])
                    )
                except(TimeoutException, StaleElementReferenceException):
                    traceback.print_exc()
                try:
                    _element = WebDriverWait(self.browser, self.timeout).until(
                        EC.visibility_of_element_located(self.locator_dictionary[what])
                    )
                except(TimeoutException, StaleElementReferenceException):
                    traceback.print_exc()
                return self.find_element(*self.locator_dictionary[what])
        except AttributeError:
            super(BasePage, self).__getattribute__("method_missing")(what)

    def method_missing(self, what):
        print("No %s here!" % what)
