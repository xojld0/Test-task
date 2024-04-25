import pytest
from selenium import webdriver

@pytest.fixture(scope="session")
def browser():
    driver_path = 'chromedriver'

    driver = webdriver.Chrome()
    yield driver
    driver.quit()