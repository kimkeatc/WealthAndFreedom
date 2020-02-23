from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os.path import abspath, exists, join
from pathlib import Path
import ast
import json
import logging
import numpy
import os
import pandas
import sys
import threading

_CURRENT_PATH = Path(__file__).resolve().parent
_PARENT_PATH = _CURRENT_PATH.parent

for path in [_CURRENT_PATH, _PARENT_PATH]:
    path = abspath(path)
    if path not in sys.path:
        sys.path.append(path)

import Project
Project.sys_path_initialize()

from weblink import BursaWebpage
import attributes


class SeleniumUtil:

    def __init__(self):
        pass

    def getDriver(self):
        project = Project.Project()
        chromeDriver = project.driver.webdriver.Chrome.driver_path()
        driver = webdriver.Chrome(chromeDriver)
        return driver

class API(SeleniumUtil, BursaWebpage):

    def __init__(self):
        super().__init__()

    def getAllMarket(self, path):
        """
        Arguments:-
            path {str} - Excel file path to be export the queried whole market data.
        Raises:-
            None
        Returns:
            0 - passed
            1 - failed
        """

        _marketUrl = BursaWebpage()
        marketTypes = attributes.MarketAttribute.List()
        marketURLs = [_marketUrl.main_market, _marketUrl.ace_market, _marketUrl.leap_market]

        # Phase 1: To get all whole market data
        contents = {}
        for marketType, marketURL in zip(marketTypes, marketURLs):
            logging.info("To get %s information." % marketType)
            content = self.getPageContent_waitEquitiesPricesTable_ID(marketURL)
            if not content:
                logging.error("Unable to get %s information." % marketType)
                return 1
            else:
                content = self.parsePageContent_EquitiesPricesTable(content)
            contents[marketType] = content
        
        logging.info("Successfully retreiving all whole market infomation.")

        # Phase 2: To consolidate all data
        counter = 1
        result = {}
        _attrCls = attributes.CompanyAttribute
        attrLength = len(_attrCls)

        for marketType, marketAttr in contents.items():
            logging.info("Size of %s : %s" % (marketType, attrLength))
            for index, market in enumerate(marketAttr):
                data = [marketType]
                for sub_index in range(attrLength):
                    attrName = _attrCls(sub_index).name
                    attrValue = getattr(marketAttr[market], attrName)
                    data.append(attrValue)
                result[str(counter).zfill(3)] = data
                counter += 1

        logging.info("Successfully consolidate all whole market infomation.")

        # Phase 3: To export data into file
        header = _attrCls.List()
        header.insert(0, "BoardType")
        dataframe = pandas.DataFrame.from_dict(result, orient='index', columns=header)
        dataframe.to_csv(path, index=False)
        logging.info("Successfully export whole market information.")
        return 0

    def getPageContent_waitEquitiesPricesTable_ID(self, url):
        """
        Arguments:-
            url {str} - URL link
        Raises:-
            TimeoutException - Timeout on loading the webpage
        Returns:
            content {str} - html page content
        """
        content = None
        driver = self.getDriver()
        driver.get(url)
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'bm_list_of_companies_container')))
            content = driver.page_source
        except TimeoutException:
            logging.error("Timeout error.")
        finally:
            driver.quit()
            return content

    def parsePageContent_EquitiesPricesTable(self, content):
        """
        Arguments:-
            content {str} - html content
        Raises:-
            None
        Returns:
            contents {dict} - Stock markets class
        """
        contents = {}
        tree = html.fromstring(content)
        tr_s_html = tree.xpath('//*[@id="bm_equities_prices_table"]/tbody/tr[*]')
        for index, tr in enumerate(tr_s_html):
            skip_this_round = False
            company = attributes.Company()
            for sub_index, a in enumerate(tr.xpath('td[*]/a')):
                if sub_index % 2:
                    page = a.text
                else:
                    url = a.attrib["href"]
                    if "javascript: void(0)" in url:
                        skip_this_round = True
                        break
                    url = "%s%s" % (self.official, url)
                    name = a.text
                    code = url.split("=")[-1]
                    code = "'%s" % str(code).zfill(4)
            if not skip_this_round:
                data = (name, code, url, page)
                companyAttr = attributes.CompanyAttribute.List()                                                                                                                                                                                                                                                                                                              
                for item, attr in zip(data, companyAttr):
                    setattr(company, attr, item)
                contents[index] = company
        return contents

    def getIndices(self, path):
        """
        Arguments:-
            path {str} - Excel file path to be export the queried whole market data.
        Raises:-
            None
        Returns:
            0 - passed
        """
        url = self.indices

        # Phase 1: To get html page content
        html_content = self.getPageContent_waitIndicesPricesTable_ID(url)
        logging.info("Successfully to get indices prices html table.")

        # Phase 2: To get indices table data
        content = self.parsePageContent_IndicesPricesTable(html_content)
        logging.info("Successfully to get indices prices table info.")

        # Phase 3: To consolidate all data
        logging.info("Successfully export indices market information.")
        result = {}
        _attrCls = attributes.IndexAttribute
        attrLength = len(_attrCls)
        for index, indices in enumerate(content):
            logging.info("Size of indices : %s" % attrLength)
            data = []
            for sub_index in range(attrLength):
                attrName = _attrCls(sub_index).name
                attrValue = getattr(indices, attrName)
                data.append(attrValue)
            result[str(index).zfill(2)] = data

        # Phase 4: To export data into file
        header = _attrCls.List()
        dataframe = pandas.DataFrame.from_dict(result, orient='index', columns=header)
        dataframe.to_csv(path, index=False)
        logging.info("Successfully export indices information.")

        return 0

    def getPageContent_waitIndicesPricesTable_ID(self, url):
        """
        Arguments:-
            url {str} - URL link
        Raises:-
            TimeoutException - Timeout on loading the webpage
        Returns:
            content {str} - html page content
        """
        content = None
        driver = self.getDriver()
        driver.get(url)
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'bm_indices_prices_table')))
            content = driver.page_source
        except TimeoutException:
            logging.error("Timeout error.")
        finally:
            driver.quit()
            return content

    def parsePageContent_IndicesPricesTable(self, content):
        """
        Arguments:-
            content {str} - html content
        Raises:-
            None
        Returns:
            contents {list} - Index class
        """
        contents = []
        tree = html.fromstring(content)
        tr_s_html = tree.xpath('//*[@id="bm_indices_prices_table"]/tbody/tr[*]')
        for index, tr in enumerate(tr_s_html):
            Index = attributes.Index()
            for sub_index, td in enumerate(tr.xpath('td')):
                attribute_name = attributes.IndexAttribute(sub_index).name
                attribute_value = td.text
                setattr(Index, attribute_name, attribute_value)
            contents.append(Index)
        return contents

    def getPN17GN3List(self, pn17_path, gn3_path):
        """
        Arguments:-
            path {str} - Excel file path to be export the queried pn17 market data.
        Raises:-
            None
        Returns:
            0 - passed
        """
        url = self.pn17_and_gn3_companies

        # Phase 1: To get html page content
        html_content = self.getPageContent_pg17gn3ContentTable(url)
        logging.info("Successfully to get PN17 and GN3 html table.")

        # Phase 2: To get table data
        content = self.parsePageContent_pg17gn3ContentTable(html_content)
        logging.info("Successfully to get PN17 and GN3 table info.")

        # Phase 3: To export PN17 data into file
        dataframe = pandas.DataFrame.from_dict(content[0])
        dataframe.to_csv(pn17_path, index=False)
        logging.info("Successfully export PN17 information.")

        # Phase 4: To export GN3 data into file
        dataframe = pandas.DataFrame.from_dict(content[1])
        dataframe.to_csv(gn3_path, index=False)
        logging.info("Successfully export GN3 information.")

    def getPageContent_pg17gn3ContentTable(self, url):
        """
        Arguments:-
            url {str} - URL link
        Raises:-
            TimeoutException - Timeout on loading the webpage
        Returns:
            content {str} - html page content
        """
        content = None
        driver = self.getDriver()
        driver.get(url)
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'bm_content_container')))
            content = driver.page_source
        except TimeoutException:
            logging.error("Timeout error.")
        finally:
            driver.quit()
            return content

    def parsePageContent_pg17gn3ContentTable(self, content):
        """
        Arguments:-
            content {str} - html content
        Raises:-
            None
        Returns:
            contents {list} - Index class
        """
        contents = []
        tree = html.fromstring(content)
        date_html = tree.xpath('//*[@id="bm_content_container"]/p[1]')

        # Phase 1: To get last update date
        date = date_html[0].text
        date = date.split(" ")
        date = " ".join(date[2:])

        # Phase 2: To get pn17 company list
        pn17 = []
        pn17_html = tree.xpath('//*[@id="bm_content_container"]/ol[1]/li')
        for index, data in enumerate(pn17_html):
            pn17.append(data.text)
        contents.append({"PN17": pn17})

        # Phase 3: To get gn3 company list
        gn3 = []
        gn3_html = tree.xpath('//*[@id="bm_content_container"]/ol[2]/li')
        for index, data in enumerate(gn3_html):
            gn3.append(data.text)
        contents.append({"GN3": gn3})

        return contents

    def getAllStock(self, basefolder, referenceFile):
        """
        Arguments:-
            basefolder {str} - Base folder to export individual stock information
            referenceFile {str} - Master excel sheet to be refer on all stock markets
        Raises:-
            None
        Returns:
            0 - passed
        """
        finish = False
        maximumThreads = 6
        _attrCompany = attributes.CompanyAttribute

        # Phase 1: Reading reference excel file
        dataframe = pandas.read_csv(referenceFile)

        # Phase 2: To get all the stock code and url list
        names, codes, filepaths, urls = [], [], [], []
        for index, row in dataframe.iterrows():
            name = row[_attrCompany(0).name]
            code = row[_attrCompany(1).name]
            url = row[_attrCompany(2).name]
            filepath = join(basefolder, "_%s.txt" % str(index + 1))
            if not exists(filepath):
                names.append(name)
                codes.append(code)
                urls.append(url)
                filepaths.append(filepath)
        
        # Phase 3: To fill up dummy value
        remainingSize = len(codes)
        if remainingSize == 0:
            return 0
        elif remainingSize < maximumThreads:
            maximumThreads = 1
        dummySize = maximumThreads - (remainingSize % maximumThreads)
        dummy = [None] * dummySize
        names += dummy
        codes += dummy
        filepaths += dummy
        urls += dummy
        
        # Phase 4: To split job
        names = numpy.split(numpy.array(names), maximumThreads)
        codes = numpy.split(numpy.array(codes), maximumThreads)
        filepaths = numpy.split(numpy.array(filepaths), maximumThreads)
        urls = numpy.split(numpy.array(urls), maximumThreads)
        drivers = []

        # Phase 5: Creating threads
        threadList = []
        for index in range(maximumThreads):
            driver = self.getDriver()
            drivers.append(driver)
            thread = threading.Thread(target=self.getStockInfo, args=(names[index], codes[index], filepaths[index],urls[index],drivers[index],))
            threadList.append(thread)

        # Phase 6: Start execute each thread
        for thread in threadList:
            thread.start()
        for thread in threadList:
            thread.join()
        for driver in drivers:
            driver.quit()

        logging.info("Successfully download stock info.")

    def getStockInfo(self, names, codes, filepaths, urls, driver):
        """
        Arguments:-
            names {list} - Company name list
            codes {list} - Code list
            filepaths {list} - File paths
            urls {list} - URL link
            driver {class} - Webdriver
        Raises:-
            TimeoutException - Timeout on loading the webpage
        Returns:
            None
        """
        for name, code, filepath, url in zip(names, codes, filepaths, urls):
            try:
                content = self.getPageContent_stockInfo(url, driver)
                if not content:
                    continue
                content = self.parsePageContent_stockInfo(name, content)
                with open(filepath, "w") as f:
                    f.write(str(vars(content)))
            except Exception as e:
                logging.error(e)

    def getPageContent_stockInfo(self, url, driver=None):
        """
        Arguments:-
            url {str} - URL link
            driver {class} - Webdriver
        Raises:-
            TimeoutException - Timeout on loading the webpage
        Returns:
            None
        """
        content = None
        if not url:
            return content
        terminate = True
        if driver:
            terminate = False
        else:
            driver = self.getDriver()
        driver.get(url)
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'bm_stock_overview')))
            content = driver.page_source
        except TimeoutException:
            logging.error("Timeout error.")
        finally:
            if terminate:
                driver.quit()
            return content

    def parsePageContent_stockInfo(self, name, content):
        """
        Arguments:-
            content {str} - html content
        Raises:-
            TimeoutException - Timeout on loading the webpage
        Returns:
            stock {class} - Stock class
        """
        tree = html.fromstring(content)

        time_html = tree.xpath('//*[@id="bm_content_container"]/div[6]/div[1]/p[1]')
        last_done_html = tree.xpath('//*[@id="bm_content_container"]/div[6]/div[1]/p[2]/strong/span')
        table_html = tree.xpath('//*[@id="bm_content_container"]/div[6]/div[1]/table/tbody/tr[*]/td')

        _stockAttr = attributes.StockAttribute
        stock = attributes.Stock()

        date_and_time = time_html[0].text
        date_and_time = date_and_time.split(" ")
        date = " ".join(date_and_time[:-1])
        time = date_and_time[-1]

        close_price_and_change = last_done_html[0].text
        close_price_and_change = close_price_and_change.split(" ")
        close_price = close_price_and_change[0]

        setattr(stock, _stockAttr(15).name, date)
        setattr(stock, _stockAttr(16).name, time)
        setattr(stock, _stockAttr(17).name, close_price)
        setattr(stock, _stockAttr(18).name, name)

        for index, attr in enumerate(table_html):
            attribute_name = _stockAttr(index).name
            attribute_value = attr.text
            setattr(stock, attribute_name, attribute_value)
        return stock

    def combineAllStock(self, path, basefolder, referenceFile):
        """
        Arguments:-
            path {str} - Export file directory
            basefolder {str} - Base folder to export individual stock information
            referenceFile {str} - Master excel sheet to be refer on all stock markets
        Raises:-
            None
        Returns:
            0 - passed
        """
        _attrCompany = attributes.CompanyAttribute

        # Phase 1: Reading reference excel file
        dataframe = pandas.read_csv(referenceFile)

        # Phase 2: To get all the stock information
        codes, filepaths, urls = [], [], []
        contents = []
        remove_list = []
        for index, row in dataframe.iterrows():
            name = row[_attrCompany(0).name]
            code = row[_attrCompany(1).name]
            filepath = join(basefolder, "_%s.txt" % str(index + 1))

            logging.info("Read stock code '%s' - '%s'" % (code[1:], name))
            if not exists(filepath):
                error_msg = "File not found... %s" % filepath
                raise ValueError(error_msg)

            with open(filepath, "r") as f:
                content = f.read()
            content = ast.literal_eval(content)
            contents.append(content)
            remove_list.append(filepath)

        # Phase 3: To export into excel file
        dataframe = pandas.DataFrame(contents)
        dataframe.to_csv(path, index=False)
        logging.info("Successfully export all stock information.")

        # Phase 4: To remove data file
        for path in remove_list:
            os.remove(path)

    def combineAllStock_enhance(self, path, reference_path):

        _company_attr = attributes.CompanyAttribute

        df = pandas.read_csv(path)
        ref_df = pandas.read_csv(reference_path)

        df[_company_attr(1).name] = ref_df[_company_attr(1).name]
        df[_company_attr(2).name] = ref_df[_company_attr(2).name]
        df.to_csv(path, index=False)


if __name__ == "__main__":
    pass
