# -*- coding: utf-8 -*-

__module__ = ''
__description__ = '''In house bursa api module.
'''

__author__ = ''
__contact__ = ''

__credits__ = []

__version__ = ''
__date__ = ''
__status__ = 'Development'

from os.path import exists, join
from datetime import datetime
import json
import logging
import os
import threading

import project
project.Project().PathInitialize()

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from filename_management import FileNameManagement
from selenium.webdriver.common.by import By
from multiprocessing import Process
from selenium import webdriver
import concurrent.futures
from common import *
import requests
import Utility
import pandas
import numpy

BURSA_URL_MAPPING_TABLE = {
    BURSA_MARKET_ACE_MARKET: 'https://www.bursamalaysia.com/market_information/equities_prices?keyword=&top_stock=&board=ACE-MKT&alphabetical=&sector=&sub_sector=&per_page=50&page={page_number}',
    BURSA_MARKET_LEAP_MARKET: 'https://www.bursamalaysia.com/market_information/equities_prices?keyword=&top_stock=&board=LEAP-MKT&alphabetical=&sector=&sub_sector=&per_page=50&page={page_number}',
    BURSA_MARKET_MAIN_MARKET: 'https://www.bursamalaysia.com/market_information/equities_prices?keyword=&top_stock=&board=MAIN-MKT&alphabetical=&sector=&sub_sector=&per_page=50&page={page_number}',
    BURSA_MARKET_STRUCTURED_WARRANTS: 'https://www.bursamalaysia.com/market_information/equities_prices?keyword=&top_stock=&board=WARRANTS&alphabetical=&sector=&sub_sector=&per_page=50&page={page_number}',
    BURSA_MARKET_ETF: 'https://www.bursamalaysia.com/market_information/equities_prices?keyword=&top_stock=&board=ETF&alphabetical=&sector=&sub_sector=&per_page=50&page={page_number}',
    BURSA_MARKET_BOND: 'https://www.bursamalaysia.com/market_information/equities_prices?keyword=&top_stock=&board=BOND%26LOAN&alphabetical=&sector=&sub_sector=&per_page=50&page={page_number}'
}

STOCK_CODE_URL = 'https://www.bursamalaysia.com/trade/trading_resources/listing_directory/company-profile?stock_code={stock_id}'
STOCK_API_BASE_URL = 'https://ws20.bursamalaysia.com/api/v2/stock_price_data?stock_code'


class GetChromeSeleniumDriver:

    path = project.Project().SubFolder.chromeWebdriver.path
    name = 'chromedriver.exe'

    _capabilities = DesiredCapabilities.CHROME
    _capabilities['loggingPrefs'] = {'performance': 'ALL'}
    _options = Options()
    _options.add_experimental_option('w3c', False)
    _options.add_argument("--headless")

    def __init__(self, version='79.0.3945.36'):
        exe_path = join(self.path, version, self.name)
        self.driver = webdriver.Chrome(exe_path, options=self._options,
                                       desired_capabilities=self._capabilities)


class ModuleApi(FileNameManagement):

    def __init__(self, basename):
        FileNameManagement.__init__(self, basename)
        self.webdrivers = []
        self.max_processor = 6

    @staticmethod
    def public_listed_company():
        return [BURSA_MARKET_ACE_MARKET, BURSA_MARKET_MAIN_MARKET, BURSA_MARKET_LEAP_MARKET]

    @staticmethod
    def price_listing_file():
        return project.Folder(project.Project().SubFolder.bin.path, 'price_listing.csv')

    @staticmethod
    def price_listing():
        _filepath = __class__.price_listing_file().path
        df = pandas.read_csv(_filepath, header=None)
        return df[0].to_list()

    def getLocalWebdriver(self):
        threadLocal = threading.local()
        driver = getattr(threadLocal, 'driver', None)
        if driver is None:
            driver = GetChromeSeleniumDriver()
            setattr(threadLocal, 'driver', driver)
        return driver

    def getMarket(self, market, page_number=1):
        df = pandas.DataFrame()
        while page_number:
            url = BURSA_URL_MAPPING_TABLE[market].format(page_number=page_number)
            logging.info(f'[{market}] : Accesing webpage: {url}')
            response = requests.get(url)
            if response.status_code == 200:
                _df = pandas.read_html(response.text, converters={'Code': str, 'stock_id': str})[0]
                if _df.empty:
                    break
                else:
                    _df['Code'] = '\'' + _df['Code'].astype(str)
                    _df['stock_id'] = '\'' + _df['stock_id'].astype(str)
                    df = pandas.concat([df, _df], ignore_index=True)
                    page_number += 1
        return df

    def exportMarket(self, market):
        _filepath = self.getMarketFilePath(market)
        if not exists(_filepath):
            df = self.getMarket(market)
            df['Date'] = self.basename
            df.to_csv(_filepath, index=False)

    def getAllMarkets(self):
        for market in BURSA_URL_MAPPING_TABLE.keys():
            process = Process(target=self.exportMarket, args=(market,))
            process.start()
            process.join()

        if not exists(self.getBursaAllMarketFilePath()):
            df = pandas.DataFrame()
            for market in BURSA_URL_MAPPING_TABLE.keys():
                _df = pandas.read_csv(self.getMarketFilePath(market), dtype={'Code': str})
                df = pandas.concat([df, _df], ignore_index=True, sort=False)
            df.drop(['No'], axis=1, inplace=True)
            df.reset_index(inplace=True, drop=True)
            df.index += 1
            df.to_csv(self.getBursaAllMarketFilePath(), index=False)

        if not exists(self.getBursaPLCMarketFilePath()):
            df = pandas.DataFrame()
            for market in __class__.public_listed_company():
                _df = pandas.read_csv(self.getMarketFilePath(market), dtype={'Code': str})
                df = pandas.concat([df, _df], ignore_index=True)
            df.drop(['No'], axis=1, inplace=True)
            df.to_csv(self.getBursaPLCMarketFilePath(), index=False)
        return 0

    def getStockList(self, market):
        _filepath = self.getMarketFilePath(market)
        df = pandas.read_csv(_filepath, dtype={'Code': str})
        df['Code'] = df['Code'].apply(lambda x: x[1:])
        return df['Code'].to_list()

    def getStocksList(self):
        stocks = []
        for market in __class__.public_listed_company():
            stocks += self.getStockList(market)
        return stocks

    def getMotherStocksList(self):
        _stocks = self.getStocksList()
        stocks = [s for s in _stocks if str(s).isdigit()]
        return stocks

    def scrapingStockHistoryUrl(self, stockid, webdriver):
        url = STOCK_CODE_URL.format(stock_id=stockid)
        logging.info(url)
        driverInst = webdriver
        driverInst.driver.get(url)
        try:
            WebDriverWait(driverInst.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'highcharts-plot-background')))
        except TimeoutException:
            logging.error("Timeout error...")
            self.scrapingStockHistoryUrl(stockid, webdriver)
        for network in driverInst.driver.get_log('performance'):
            if STOCK_API_BASE_URL in str(network):
                url = json.loads(network['message'])['message']['params']['request']['url']
                break
        return url

    def getStockHistory(self, stockid, webdriver):
        url = self.scrapingStockHistoryUrl(stockid, webdriver)
        response = requests.get(url)
        if response.status_code == 200:
            return pandas.DataFrame(response.json()['historical_data']['data'])
        else:
            logging.error(f'Unable to get stock {stockid} history...')
            self.getStockHistory(stockid, webdriver)

    def exportStockHistory(self, stockid, webdriver):
        _filepath = self.getStockFilePath(stockid)
        df = self.getStockHistory(stockid, webdriver)
        df['id'] = '\'' + df['id'].astype(str)
        df.rename(columns={'date': 'Date(int)', 'id': 'Stock ID', 'name': 'Name',
                           'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'vol': 'Volume'}, inplace=True)
        df['Date'] = df['Date(int)'].apply(lambda x: datetime.fromtimestamp(x / 1000).strftime('%Y%m%d'))
        df = df[['Date(int)', 'Date', 'Name', 'Stock ID', 'Open', 'High', 'Low', 'Close', 'Volume']]
        # df['Bid Size'] = df.apply(lambda row: self.getBidSize(row['Open'], row['Close']), axis=1)
        # df['Direction'] = df.apply(lambda row: self.getDirection(row['Open'], row['Close'], row['Volume']), axis=1)
        # for i in range(0, len(df)):
        #     df.loc[i, 'LACP'] = numpy.nan if i == 0 else df.loc[i-1, 'Close']
        # df = df[['Date(int)', 'Date', 'Name', 'Stock ID', 'LACP', 'Open', 'High', 'Low', 'Close', 'Volume', 'Direction', 'Bid Size']]
        df.to_csv(_filepath, index=False)

    def getBidSize(self, open_price, close_price):
        price_list = self.price_listing()
        return abs(price_list.index(float(close_price)) - price_list.index(float(open_price)))

    def getDirection(self, open_price, close_price, volume):
        if volume == '-':
            return STOCK_DIRECTION_CLOSED
        elif open_price == close_price:
            return STOCK_DIRECTION_NO_CHANGE
        elif float(open_price) > float(close_price):
            return STOCK_DIRECTION_DECREATED
        elif float(open_price) < float(close_price):
            return STOCK_DIRECTION_INCREASED
        else:
            return numpy.nan

    def initializeDriver(self):
        self.webdrivers.append(GetChromeSeleniumDriver())

    def getStocksHistory(self):
        if not exists(self.getStockFolder()):
            Utility.folderCreation(self.getStockFolder(), mode=0o770)

        _stocks = self.getMotherStocksList()
        logging.info(f'Market size: %s' % len(_stocks))

        stocks = [s for s in _stocks if not exists(self.getStockFilePath(s))]
        if stocks:
            # Initialize all the webdrivers
            threads = []
            for _ in range(self.max_processor):
                p = threading.Thread(target=self.initializeDriver, args=())
                threads.append(p)
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

            # Begin to download stock history
            with concurrent.futures.ThreadPoolExecutor(self.max_processor) as executor:
                for index, stock in enumerate(stocks):
                    executor.submit(self.exportStockHistory, stock, self.webdrivers[index % self.max_processor])

            # Quit all the webdrivers
            for driverInst in self.webdrivers:
                driverInst.driver.quit()
            return 1 if len(os.listdir(self.getStockFolder())) != len(_stocks) else 0
        else:
            return 0

    def getOpenPrice(self, stockid):
        stockid = stockid[1:]
        _filepath = self.getStockFilePath(stockid)
        if exists(_filepath):
            df = pandas.read_csv(_filepath)
            try:
                result = df[df['Date'].astype(str) == self.basename]['Open'].values[0]
            except Exception:
                result = numpy.nan
            finally:
                return result
        return numpy.nan

    def getClosePrice(self, stockid):
        stockid = stockid[1:]
        _filepath = self.getStockFilePath(stockid)
        if exists(_filepath):
            df = pandas.read_csv(_filepath)
            try:
                result = df[df['Date'].astype(str) == self.basename]['Close'].values[0]
            except Exception:
                result = numpy.nan
            finally:
                return result
        return numpy.nan

    def updatePublicListedCompanyOpenPrice(self):
        _filepath = self.getBursaPLCMarketFilePath()
        df = pandas.read_csv(_filepath)
        df['Open'] = df.apply(lambda row: self.getOpenPrice(row['Code']), axis=1)
        df['Close'] = df.apply(lambda row: self.getClosePrice(row['Code']), axis=1)
        df.to_csv(_filepath, index=False)


if __name__ == '__main__':
    pass
