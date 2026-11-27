from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import qa_config as C
from .base_page import BasePage


class RegisterPage(BasePage):
    PATH = C.ROUTES["register"]
    USERNAME = (By.NAME, C.F_USERNAME)
    PASSWORD = (By.NAME, C.F_PASSWORD)
    SUBMIT = (By.CSS_SELECTOR, "form button[type=submit], form input[type=submit]")

    def register(self, username, password=C.PASSWORD):
        self.open()
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        button = self.find(self.SUBMIT)
        button.click()
        self.wait.until(EC.staleness_of(button))      # page reloaded (success or error)
        return self


class LoginPage(RegisterPage):
    PATH = C.ROUTES["login"]

    def login(self, username, password=C.PASSWORD):
        return self.register(username, password)


def logout(driver):
    driver.get(C.BASE_URL + C.ROUTES["logout"])
