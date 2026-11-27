from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import qa_config as C
from .base_page import BasePage


class TaskFormPage(BasePage):
    PATH = C.ROUTES["new_task"]
    TITLE = (By.NAME, C.F_TITLE)
    CATEGORY = (By.NAME, C.F_CATEGORY)
    DUE = (By.NAME, C.F_DUE)
    SAVE = (By.CSS_SELECTOR, "form button[type=submit], form input[type=submit]")

    def create(self, title, category=None, due_iso=None):
        self.open()
        if title:
            self.type(self.TITLE, title)
        if category:
            Select(self.find(self.CATEGORY)).select_by_visible_text(category)
        if due_iso:
            # set the value directly: date-picker typing differs between browsers
            self.driver.execute_script("arguments[0].value = arguments[1];", self.find(self.DUE), due_iso)
        button = self.find(self.SAVE)
        button.click()
        self.wait.until(EC.staleness_of(button))      # wait for the redirect to My Tasks
        return self


class MyTasksPage(BasePage):
    PATH = C.ROUTES["index"]
    ROWS = (By.CSS_SELECTOR, "table tbody tr, table tr")
    CATEGORY_FILTER = (By.NAME, C.Q_CATEGORY)

    def row(self, title):
        self.find((By.TAG_NAME, "body"))
        for r in self.driver.find_elements(*self.ROWS):
            if title in r.text:
                return r
        return None

    def toggle(self, title):
        row = self.row(title)
        row.find_element(By.CSS_SELECTOR, "form[action*='toggle'] button, button.toggle").click()
        self.wait.until(EC.staleness_of(row))

    def delete(self, title, accept=True):
        row = self.row(title)
        row.find_element(By.CSS_SELECTOR, "form[action*='delete'] button, button.delete").click()
        alert = self.wait.until(EC.alert_is_present())
        if accept:
            alert.accept()
            self.wait.until(EC.staleness_of(row))
        else:
            alert.dismiss()

    def filter_category(self, name):
        Select(self.find(self.CATEGORY_FILTER)).select_by_visible_text(name)   # auto-submits
        self.wait.until(lambda d: f"{C.Q_CATEGORY}=" in d.current_url)


class DashboardPage(BasePage):
    PATH = C.ROUTES["dashboard"]

    def counters(self):
        import qa_support as S
        self.open()
        return S.dashboard_counts_from_html(self.driver.page_source)
