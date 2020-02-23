import logging

from Folders import Webdriver
from Project import Project
project = Project().path_initialize()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BursaWebpage:

    @property
    def official(self):
        return "http://www.bursamalaysia.com"

    @property
    def pn17_and_gn3_companies(self):
        return "http://www.bursamalaysia.com/market/listed-companies/list-of-companies/pn17-and-gn3-companies/"
    
    @property
    def ace_market(self):
        return "http://www.bursamalaysia.com/market/listed-companies/list-of-companies/ace-market/"

    @property
    def leap_market(self):
        return "http://www.bursamalaysia.com/market/listed-companies/list-of-companies/leap-market/"

    @property
    def main_market(self):
        return "http://www.bursamalaysia.com/market/listed-companies/list-of-companies/main-market/"


class BursaWebdriver(Webdriver):

    def __init__(self):
        super().__init__()

    def get_page_content(self, page, wait=None, driver=None):
        terminate = False
        
        if not driver:
            terminate = True
            driver_path = Webdriver().chrome_driver().path()
            driver = webdriver.Chrome(driver_path)

        driver.get(page)

        if wait:

            try:
                if wait == "market_info":
                    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "bm_equities_prices_table")))
            except TimeoutException:
                logging.error("Timeout... Failed to load page %s" % page)
                driver.quit()
                return None
            except Exception as e:
                logging.error(e)
                driver.quit()
                return None

        content = driver.page_source
        if terminate:
            driver.quit()

        return content


class Bursa(BursaWebpage, BursaWebdriver):

    def __init__(self):
        super().__init__()
        
    def get_ace_market(self):
        webpage = self.ace_market
        content = self.get_page_content(webpage, wait="market_info")
        return content
        
    def get_leap_market(self):
        webpage = self.leap_market
        content = self.get_page_content(webpage, wait="market_info")
        return content

    def get_main_market(self):
        webpage = self.main_market
        content = self.get_page_content(webpage, wait="market_info")
        return content


if __name__ == "__main__":
    print(Bursa().get_ace_market())
