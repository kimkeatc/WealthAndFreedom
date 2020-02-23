from project_path import Tool
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback

class Company:

    def __init__(self, name, bursa, webpage, url):
        self.name = name
        self.bursa = bursa
        self.webpage = webpage
        self.url = url

class Webpage:

    def __init__(self, url=None, content=None):
        self.url = url
        self.content = content

    @property
    def by_id(self):
        return "id"

    
class Bursa:

    def __init__(self):
        pass

    def webpage_official(self):
        return "http://www.bursamalaysia.com"

    def webpage_listOfCompanies(self):
        return "%s/market/listed-companies/list-of-companies" % self.webpage_official()

    def webpage_aceMarket(self):
        return "%s/%s" % (self.webpage_listOfCompanies(), self.ace_market)

    def webpage_leapMarket(self):
        return "%s/%s" % (self.webpage_listOfCompanies(), self.leap_market)

    def webpage_mainMarket(self):
        return "%s/%s" % (self.webpage_listOfCompanies(), self.main_market)

    @property
    def ace_market(self):
        return "ace-market"

    @property
    def leap_market(self):
        return "leap-market"

    @property
    def main_market(self):
        return "main-market"

    def get_all_board_companies(self):
        boards = [self.ace_market, self.leap_market, self.main_market]
        contents = []
        for index, board in enumerate(boards):
            cls = self.get_board_companies(board)
            contents.append({board:cls})
        return contents

    def get_board_webpage(self, board):
        boards = {self.ace_market:self.webpage_aceMarket(),
                  self.leap_market:self.webpage_leapMarket(),
                  self.main_market:self.webpage_mainMarket()}
        if board in boards.keys():
            return boards[board]
        else:
            raise IOError("Invalid board given.")

    def get_board_companies(self, board):

        companies = []
        url = self.get_board_webpage(board)
        if url:
            try:
                content = self.get_page_content(url, [{By.ID: "bm_equities_prices_table"}])
            except Exception as e:
                print(e)
                raise Exception("Failed to get page content.")
        else:
            raise IOError("Empty board url.")

        tree = html.fromstring(content)
        for index, tr in enumerate(tree.xpath('//*[@id="bm_equities_prices_table"]/tbody/tr[*]')):
            for item, a in enumerate(tr.xpath('td[*]/a')):
                href = a.attrib["href"]
                text = a.text
                if item == 0:
                    company_name = text
                    bursa_url = "%s/%s" % (self.webpage_official(), href)
                elif item == 1:
                    company_website = text
                    company_url = href
                
            companies.append(Company(company_name, bursa_url, company_website, company_url))

        return Webpage(url, companies)

    def get_webdriver(self, driver_type="chrome"):
        path = None
        if driver_type == "chrome":
            path = Tool().ChromeWebdriver()
        return path

    def get_page_content(self, url, loads=[]):
        content = None
        try:
            driver = webdriver.Chrome(self.get_webdriver())
            driver.get(url)

            for index, load in enumerate(loads):
                for attribute, value in load.items():
                    WebDriverWait(driver, 3).until(EC.presence_of_element_located((attribute, value)))

            content = driver.page_source
        except Exception:
            print(traceback.format_exc())
        finally:
            if "driver" in locals().keys():
                driver.quit()
        return content


boards = Bursa().get_all_board_companies()
for index, temp_dict in enumerate(boards):
    for board, board_cls in temp_dict.items():
        print(board)
        for company in board_cls.content:
            print(company.name)

