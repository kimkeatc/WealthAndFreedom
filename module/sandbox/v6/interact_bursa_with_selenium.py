import datetime
import logging
import os
import pandas
import sys
import traceback
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys_path

class MarketBoard:
    ace_market = "Ace Market"
    leap_market = "Leap Market"
    main_market = "Main Market"
    
    def board_list(self):
        return [self.ace_market, self.leap_market, self.main_market]

class WebDriverType:
    chrome = "chrome"

class Bursa(MarketBoard, WebDriverType):

    default_webdriver = WebDriverType().chrome

    def __init__(self, driver_type=None):
        super(WebDriverType, self).__init__()
        self.driver_type = driver_type if driver_type else self.default_webdriver
        if self.driver_type == self.chrome:
            self.driver_cls = webdriver.Chrome
            self.driver_path = self.get_webdriver_path_chrome()

    def get_webdriver_path_chrome(self):
        cls = sys_path._ppath()
        return cls.get_path(cls.webdriver_chrome_path)

    def run_process(self):
        return self.driver_cls(self.driver_path)

    def url_home_page(self):
        return "http://www.bursamalaysia.com/market/"

    def url_stock_screener_page(self):
        return "http://www.bursamalaysia.com/market/listed-companies/list-of-companies"


x = Bursa()
