from selenium.webdriver.common.by import By
from .base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class MainPage(BasePage):
    errors = {"Ошибка логина": (By.XPATH, "//*[@data-tooltip='Пожалуйста, введите действительный электронный адрес']"),
              "Ошибка пароля": (By.XPATH, "//*[@data-tooltip='Используйте 4-15 символов, включая как минимум 2"
                                          " буквы и 2 цифры.']"),
              "Ошибка данных": (By.XPATH, "//*[@id='serverErrors'][text()='Неверный логин"
                                          " или пароль, повторите попытку']")}

    drop_lists_locators = {'Котировки': (By.XPATH, '//*[@class="nav"][text()="Котировки"]'),
                           'Акции': (By.XPATH, '//*[@href="/equities/"][text()="Акции"]')}

    buttons_locators = {"Вход": (By.XPATH, "//*[@class='newButton orange'][text()='Вход']")}

    articles_locators = {"Россия": (By.XPATH, "//*[@href='/equities/russia']"),
                         "Вход": (By.XPATH, "//*[@class='login bold']")}

    inputs_locators = {"Поле логина": (By.ID, 'loginFormUser_email'),
                       "Поле пароля": (By.ID, 'loginForm_password')}

    pathes = {"выпадающий список": drop_lists_locators,
              "пункт": articles_locators,
              "крестик": buttons_locators,
              "кнопку": buttons_locators,
              "ошибка": errors}

    def __init__(self, context):
        BasePage.__init__(self, context, base_url='https://ru.investing.com/')

    def input_data(self, context, text, text1):
        WebDriverWait(context.browser, 3).until(EC.presence_of_element_located(self.inputs_locators[text]))
        self.find_element(*self.inputs_locators[text]).send_keys(text1)

    def clear_inputs(self, context, text):
        WebDriverWait(context.browser, 3).until(EC.presence_of_element_located(self.inputs_locators[text]))
        self.find_element(*self.inputs_locators[text]).clear()

    def assert_page(self, context, element_name, value):
        WebDriverWait(context.browser, 3).until(EC.presence_of_element_located(self.pathes[element_name][value]))
        assert self.find_element(*self.pathes[element_name][value])

    def hover_element(self, context, element_type, value):
        WebDriverWait(context.browser, 3).until(EC.presence_of_element_located(self.pathes[element_type][value]))
        ActionChains(context.browser).move_to_element(self.find_element(*self.pathes[element_type][value])).perform()

    def press_element(self, context, element_type, value):
        WebDriverWait(context.browser, 3).until(EC.presence_of_element_located(self.pathes[element_type][value]))
        self.find_element(*self.pathes[element_type][value]).click()
