# -*- coding: utf-8 -*-

from multiprocessing import Process
from os.path import exists
import json
import logging
import threading

import namespace
import Utility
Utility.Project().system_path_initialize()

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import concurrent.futures
import requests
import pandas

pandas.set_option('display.max_rows', 1000)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)
pandas.set_option('float_format', '{:.3f}'.format)
pandas.set_option('expand_frame_repr', False)

STOCK_API_BASE_URL = 'https://ws20.bursamalaysia.com/api/v2/stock_price_data?stock_code'
STOCK_URL = 'https://www.bursamalaysia.com/trade/trading_resources/listing_directory/company-profile'
STOCK_CODE_URL = STOCK_URL + '?stock_code={stock_id}'

MARKET_URL = {namespace.ACE_MARKET: 'https://www.bursamalaysia.com/market_information/equities_prices?keyword=&top_stock=&board=ACE-MKT&alphabetical=&sector=&sub_sector=&per_page=50&page={page_number}',
              namespace.LEAP_MARKET: 'https://www.bursamalaysia.com/market_information/equities_prices?keyword=&top_stock=&board=LEAP-MKT&alphabetical=&sector=&sub_sector=&per_page=50&page={page_number}',
              namespace.MAIN_MARKET: 'https://www.bursamalaysia.com/market_information/equities_prices?keyword=&top_stock=&board=MAIN-MKT&alphabetical=&sector=&sub_sector=&per_page=50&page={page_number}',
              namespace.STRUCTURED_WARRANTS: 'https://www.bursamalaysia.com/market_information/equities_prices?keyword=&top_stock=&board=WARRANTS&alphabetical=&sector=&sub_sector=&per_page=50&page={page_number}',
              namespace.ETF: 'https://www.bursamalaysia.com/market_information/equities_prices?keyword=&top_stock=&board=ETF&alphabetical=&sector=&sub_sector=&per_page=50&page={page_number}',
              namespace.BOND: 'https://www.bursamalaysia.com/market_information/equities_prices?keyword=&top_stock=&board=BOND%26LOAN&alphabetical=&sector=&sub_sector=&per_page=50&page={page_number}'
              }


class getChromeSeleniumWebdriver:

    _capabilities = DesiredCapabilities.CHROME
    _capabilities['loggingPrefs'] = {'performance': 'ALL'}
    _options = Options()
    _options.add_experimental_option('w3c', False)
    _options.add_argument("--headless")

    def __init__(self):
        self.driver = webdriver.Chrome(__class__.webdriver().path,
                                       options=self._options,
                                       desired_capabilities=self._capabilities)

    @staticmethod
    def webdriver():
        return Utility.Project().chrome_webdriver()


class ChromeSeleniumWebdriver:

    def __init__(self):
        self.webdrivers = []

    def addDriver(self):
        self.webdrivers.append(getChromeSeleniumWebdriver())

    def stopAllDriver(self):
        for d in self.webdrivers:
            d.driver.quit()


class ModuleApi(ChromeSeleniumWebdriver):

    def __init__(self, ioLogFolder):
        ChromeSeleniumWebdriver.__init__(self)
        self.maximum_processor = 1
        self.ioLogFolder = ioLogFolder

    def _market_data_parser(self, series):
        args = series['Name'].split(' ')
        name, status = args[0], args[-1]
        if status == name:
            status = ''
        series['Name'], series['Status'] = name, status
        return series

    def _addStockUrl(self, series):
        if series['Code'].isdigit():
            series['URL'] = STOCK_CODE_URL.format(stock_id=series['Code'])
        return series

    def getMarket(self, market, page_number=1):
        df = pandas.DataFrame()
        while page_number:
            url = MARKET_URL[market].format(page_number=page_number)
            r = requests.get(url)
            r.raise_for_status()
            _df = pandas.read_html(r.text, converters={'Code': str, 'stock_id': str})[0]
            if _df.empty:
                break
            else:
                df = pandas.concat([df, _df], ignore_index=True)
                page_number += 1
        return df

    def exportMarket(self, market):
        filepath = self.ioLogFolder.bursa_market_filepath(market)
        if not exists(filepath):
            df = self.getMarket(market)
            df.insert(1, 'Date', self.ioLogFolder.basename)
            df['Market'] = market
            df = df.apply(self._market_data_parser, axis=1)
            df.to_excel(filepath, index=False)

    def exportScreenerResult(self):
        processes = []
        for market in MARKET_URL.keys():
            process = Process(target=self.exportMarket, args=(market, ))
            processes.append(process)
        for process in processes:
            process.start()
        for process in processes:
            process.join()

        filepath_all = self.ioLogFolder.bursa_screener_filepath()
        filepath_alm = self.ioLogFolder.ace_leap_main_filepath()
        if not exists(filepath_all) or not exists(filepath_alm):
            dfAll = pandas.DataFrame()
            dfALM = pandas.DataFrame()
            for market in MARKET_URL.keys():
                _df = pandas.read_excel(self.ioLogFolder.bursa_market_filepath(market), converters={'Code': str})
                dfAll = pandas.concat([dfAll, _df], ignore_index=True, sort=False)
                if market in [namespace.ACE_MARKET, namespace.LEAP_MARKET, namespace.MAIN_MARKET]:
                    _df = _df.apply(self._addStockUrl, axis=1)
                    dfALM = pandas.concat([dfALM, _df], ignore_index=True, sort=False)
            dfAll.drop(['No'], axis=1, inplace=True)
            dfALM.drop(['No'], axis=1, inplace=True)
            dfAll.to_excel(filepath_all, index=False)
            dfALM.to_excel(filepath_alm, index=False)

    def getStockHistoricalData(self, url, _driver):
        driver = _driver.driver
        try:
            driver.get(url)
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'highcharts-plot-background')))
        except TimeoutException:
            return

        for network in driver.get_log('performance'):
            if STOCK_API_BASE_URL in str(network):
                url = json.loads(network['message'])['message']['params']['request']['url']
                break
        r = requests.get(url)
        r.raise_for_status()
        return r.json()

    def exportStockHistoricalData(self, path, url, _driver):
        json_text = self.getStockHistoricalData(url, _driver)
        with open(path, 'w') as f:
            json.dump(json_text, f)

    def exportAllStockHistoricalData(self):

        lstStockUrl = []
        lstStockCode = []
        lstStockFilepath = []

        basepath = self.ioLogFolder.profileFolder()
        if not exists(basepath):
            Utility.makeFolder(basepath)

        # Getting the full list
        df = pandas.read_excel(self.ioLogFolder.ace_leap_main_filepath())
        df.dropna(subset=['URL'], inplace=True)
        _lstStockUrl = df['URL'].to_list()
        _lstStockCode = df['Code'].to_list()
        _lstStockFilepath = [self.ioLogFolder.stock_json_filepath(c) for c in _lstStockCode]

        # Filter off collected stock list
        logging.info('Market size: %s' % len(_lstStockCode))
        for code, path, url in zip(_lstStockCode, _lstStockFilepath, _lstStockUrl):
            if not exists(path):
                lstStockUrl.append(url)
                lstStockCode.append(code)
                lstStockFilepath.append(path)

        if len(lstStockCode) == 0:
            return 0

        # Initialize chrome webdriver
        threads = []
        for _ in range(self.maximum_processor):
            thread = threading.Thread(target=self.addDriver, args=())
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        for index, (code, path, url) in enumerate(zip(lstStockCode, lstStockFilepath, lstStockUrl)):
            with concurrent.futures.ThreadPoolExecutor(self.maximum_processor) as executor:
                executor.submit(self.exportStockHistoricalData, path, url, self.webdrivers[index % self.maximum_processor])
        self.stopAllDriver()


if __name__ == '__main__':
    pass
