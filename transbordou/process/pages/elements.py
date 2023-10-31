from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium_tools.page_objects import Element
from selenium_tools.selenium_plus.plus import wait_chrome_download


class DowloandHistory(Element):
    btn_submit = (By.XPATH, "/html/body/div/form/input[2]")
    checkbox_all_stations = (By.ID, "all_check")
    select_year_all_stations = (By.ID, "all_choice")

    @wait_chrome_download(timeout=10)
    def download_specific_station(self, year: int, station: int):
        select_year = (By.ID, f"id_{station}-choice")
        select_station = (By.ID, f"id_{station}-check")
        iframe = self.find_element((By.TAG_NAME, "iframe"))
        self.change_frame(iframe)
        self.find_element(select_station).click()
        element = self.find_element(select_year)
        select = Select(element)
        select.select_by_value(str(year))
        self.find_element(self.btn_submit).click()
        sleep(2)

    @wait_chrome_download(timeout=10)
    def download_history_all_stations(self, year: int):
        self.driver.caps["options"]
        iframe = self.find_element((By.TAG_NAME, "iframe"))
        self.change_frame(iframe)
        self.find_element(self.checkbox_all_stations).click()
        element = self.find_element(self.select_year_all_stations)
        select = Select(element)
        select.select_by_value(str(year))
        self.find_element(self.btn_submit).click()
        sleep(5)
