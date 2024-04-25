from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest

from pages import SbisHelper  # Page Object
from pages import SbisLocators  # Locators


def test_first_condition(browser):
    sbis_main_page = SbisHelper(browser)
    sbis_main_page.go_to_site()
    sbis_main_page.find_clickable_element((By.LINK_TEXT, 'Контакты')).click() # find & click on "Contacts" link
    sbis_main_page.find_clickable_element((By.XPATH, '//a[@title="tensor.ru"]/img')).click() # find & click on "Tensor" banner
    sbis_main_page.switch_window(1) # Change window to tensor.ru
    power_in_people_div = sbis_main_page.find_power_in_people_block()
    
    assert power_in_people_div != None
    assert sbis_main_page.go_to_tensor_ru(power_in_people_div) 

    work_block = sbis_main_page.find_work_block()
    assert work_block != None
    assert sbis_main_page.check_image_size(work_block)


def test_second_condition(browser):
    sbis_main_page = SbisHelper(browser)
    sbis_main_page.go_to_site('https://sbis.ru/contacts')

    assert sbis_main_page.find_element(SbisLocators.LOCATOR_SBISREGION_NAME).text == "Калининград"
    assert sbis_main_page.change_region()
    assert sbis_main_page.check_url(r"41-kamchatskij-kraj")
    assert sbis_main_page.find_element(SbisLocators.LOCATOR_SBISREGION_NAME).text == "Петропавловск-Камчатский"
    assert sbis_main_page.check_region_partners()


def test_third_condition(browser):
    sbis_main_page = SbisHelper(browser)
    sbis_main_page.go_to_site()

    assert sbis_main_page.go_to_downloads()
    assert sbis_main_page.change_donwload_tab()

    downloadLink = sbis_main_page.find_element(SbisLocators.LOCATOR_DOWNLOAD_LINK).get_attribute('href')
    assert sbis_main_page.donwload_and_check_file_size(downloadLink)