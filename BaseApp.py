from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class BasePage:
    def __init__(self, driver):
        self.driver   = driver
        self.base_url = "https://sbis.ru/"


    def find_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator),
            message=f"Can't find element by locator {locator}")


    def find_elements(self, locator, time=10):
        return WebDriverWait(self.driver,time).until(EC.presence_of_all_elements_located(locator),
            message=f"Can't find elements by locator {locator}")
    

    def find_clickable_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(EC.element_to_be_clickable(locator),
            message=f"Can't find elements by locator {locator}")
    

    def switch_window(self, index):
        window_after = self.driver.window_handles[index]
        self.driver.switch_to.window(window_after)


    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(1)


    def go_to_site(self, url = ""):
        url = self.base_url if url == "" else url
        return self.driver.get(url)