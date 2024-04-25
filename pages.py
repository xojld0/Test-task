from BaseApp import BasePage

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import time
import re
import os
import requests


class SbisLocators:
    LOCATOR_DIV_POWER_IN_PEOPLE = (By.XPATH, '//div[contains(@class, "tensor_ru-Index__block4-content") and contains(@class, "tensor_ru-Index__card")]')
    LOCATOR_TENSOR_RU_LOADED    = (By.XPATH, "//div[contains(@id, 'wasaby-content')]")
    LOCATOR_WORK_BLOCK          = (By.XPATH, '//div[contains(@class, "tensor_ru-container") and contains(@class, "tensor_ru-section") and contains(@class, "tensor_ru-About__block3")]')

    LOCATOR_SBISREGION_LINK     = (By.XPATH, '//span[contains(@class, "sbis_ru-Region-Chooser__text") and contains(@class, "sbis_ru-link")]')
    LOCATOR_SBISREGION_SPAN     = (By.XPATH, '//span[@title="Камчатский край"]')
    LOCATOR_SBISREGION_LOADED   = (By.XPATH, "//div[contains(@id, 'wasaby-content')]")
    LOCATOR_SBISREGION_NAME     = (By.XPATH, '//div[@id="city-id-1" or @id="city-id-2" or @id="city-id-3"]')

    LOCATOR_DOWNLOADS_LINK      = (By.XPATH, '//a[contains(@class, "sbisru-Footer__link") and contains(text(), "Скачать локальные версии")]')
    LOCATOR_DOWNLOADS_LOADED    = (By.XPATH, "//div[contains(@id, 'container')]")
    LOCATOR_DOWNLOAD_TABS       = (By.XPATH, '//div[contains(@class, "controls-TabButton") and contains(@class, "controls-TabButton__right-align") and contains(@class, "controls-ListView__item")]')
    LOCATOR_DOWNLOAD_LINK       = (By.XPATH, '//a[contains(@class, "sbis_ru-DownloadNew-loadLink__link") and contains(@class, "js-link")]')


class SbisHelper(BasePage): 
    def find_power_in_people_block(self):
        page_divs = self.find_elements(SbisLocators.LOCATOR_DIV_POWER_IN_PEOPLE)

        for div in page_divs:
            paragraph = div.find_elements(By.XPATH, './/p[contains(@class, "tensor_ru-Index__card-title") and contains(@class, "tensor_ru-pb-16")]')

            for block in paragraph:
                if block.text == "Сила в людях":
                    return div

        return None
    

    def go_to_tensor_ru(self, power_in_people_div):
        # find & click "More detail" link inside "Power in people" block
        details_link = power_in_people_div.find_element(By.XPATH, './/a[contains(@class, "tensor_ru-link") and contains(@class, "tensor_ru-Index__link")]')
        self.scroll_to_element(details_link)
        details_link.click()

        page_loaded = False

        # waiting for page loading after click
        try:
            self.find_element(SbisLocators.LOCATOR_TENSOR_RU_LOADED)
            page_loaded = True
        except TimeoutException:
            page_loaded = False

        return page_loaded
    

    def find_work_block(self):
        page_divs = self.find_elements(SbisLocators.LOCATOR_WORK_BLOCK)

        for div in page_divs:
            h2 = div.find_element(By.XPATH, './/h2[contains(@class, "tensor_ru-header-h2")]')

            if h2.text == 'Работаем':
                return div
            

    def check_image_size(self, div):
        imagesGrid = div.find_element(By.XPATH, './/div[contains(@class, "s-Grid-container")]')
        self.scroll_to_element(imagesGrid)
        imagesBlocks = imagesGrid.find_elements(By.XPATH, './/img[contains(@class, "tensor_ru-About__block3-image") and contains(@class, "new_lazy loaded")]')
    
        # check first image size
        first_image_width  = int(imagesBlocks[0].get_attribute('width'))
        first_image_height = int(imagesBlocks[0].get_attribute('height'))

        # check every image size
        for image in imagesBlocks[1:]:  # skip first image, because we already got its size
            width  = int(image.get_attribute('width'))
            height = int(image.get_attribute('height'))

            if width != first_image_width or height != first_image_height:
                return False
        else:
            return True
        
    
    def change_region(self):
        self.find_element(SbisLocators.LOCATOR_SBISREGION_LINK).click()
        self.find_clickable_element(SbisLocators.LOCATOR_SBISREGION_SPAN).click()

        page_loaded = False

        try:
            self.find_element(SbisLocators.LOCATOR_SBISREGION_LOADED)
            page_loaded = True
        except TimeoutException:
            page_loaded = False
        
        time.sleep(1)

        return page_loaded
    

    def check_url(self, pattern):
        return re.search(pattern, self.driver.current_url)
    

    def check_region_partners(self):
        region_partnes = self.find_elements((By.XPATH, '//div[contains(@class, "sbisru-Contacts-List__col-1")]'))

        is_partners_correct_title   = False
        is_partners_correct_address = False

        for div in region_partnes:
            title   = div.find_element(By.XPATH, './/div[contains(@class, "sbisru-Contacts-List__name")]')
            address = div.find_element(By.XPATH, './/div[contains(@class, "sbisru-Contacts-List__address")]')

            if title.get_attribute('title') == "СБИС - Камчатка":
                is_partners_correct_title = True

            if address.get_attribute('title') == "ул.Ленинская, 59, оф.202, 205":
                is_partners_correct_address = True
        
        return is_partners_correct_title and is_partners_correct_address
    

    def go_to_downloads(self):
        downloads_link = self.find_element(SbisLocators.LOCATOR_DOWNLOADS_LINK)
        self.scroll_to_element(downloads_link)
        downloads_link.click()

        page_loaded = False

        try:
            self.find_element(SbisLocators.LOCATOR_DOWNLOADS_LOADED)
            page_loaded = True
        except TimeoutException:
            page_loaded = False

        return page_loaded
    

    def change_donwload_tab(self):
        download_tabs = self.find_elements(SbisLocators.LOCATOR_DOWNLOAD_TABS)

        for tab in download_tabs:
            tabText = tab.find_element(By.XPATH, './/div[contains(@class, "controls-TabButton__caption")]').text

            if tabText == "СБИС Плагин":
                time.sleep(2)
                tabButton = tab.find_element(By.XPATH, './/div[contains(@class, "controls-tabButton__overlay")]')
                tabButton.click()
                time.sleep(1)
                return True

        return False
    

    def donwload_and_check_file_size(self, file_url):
        file_name   = "sbisplugin-setup-web.exe"
        folder_path = os.path.dirname(os.path.abspath(__file__))
        file_path   = os.path.join(folder_path, file_name)

        response    = requests.get(file_url, stream=True)

        with open(file_path, 'wb') as f:
            chunk_size = 1024
            #total_size = int(response.headers.get('content-length', 0))
            progress = 0

            # for chunk in response.iter_content(chunk_size=chunk_size):
            #     f.write(chunk)
            #     progress += len(chunk)

            #     print(f"Прогресс: {progress}/{total_size} байт", end='\r', flush=True)

        file_size_mb     = os.path.getsize(file_path) / (1024 * 1024)
        expected_size_mb = 7.12

        os.remove(file_path)

        return round(file_size_mb, 2) == expected_size_mb