from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import qa_config as C


class BasePage:
    PATH = "/"
    FLASH = (By.CSS_SELECTOR, ".error, .flash, .alert")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, **query):
        q = "&".join(f"{k}={v}" for k, v in query.items())
        self.driver.get(C.BASE_URL + self.PATH + (("?" + q) if q else ""))
        return self

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, value):
        el = self.find(locator)
        el.clear()
        el.send_keys(value)

    @property
    def path(self):
        from urllib.parse import urlparse
        return urlparse(self.driver.current_url).path

    def message(self):
        els = self.driver.find_elements(*self.FLASH)
        return " ".join(e.text for e in els)

    def page_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text
