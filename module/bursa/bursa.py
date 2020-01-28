# -*- coding: utf-8 -*-

from os.path import abspath, dirname, exists, join
from multiprocessing import Process
import logging
import sys
import os

_MODULE_FOLDER = abspath(join(dirname(__file__), '..'))
if _MODULE_FOLDER not in sys.path:
    sys.path.append(_MODULE_FOLDER)

import namespace
import Utility
Utility.MyProject().system_path_initialize()

import requests
import pandas

pandas.set_option('display.max_rows', 1000)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)
pandas.set_option('float_format', '{:.3f}'.format)
pandas.set_option('expand_frame_repr', False)

STOCK_API_BASE_URL = 'https://ws20.bursamalaysia.com/api/v2/stock_price_data?stock_code'
STOCK_URL = 'https://www.bursamalaysia.com/trade/trading_resources/listing_directory/company-profile'
STOCK_CODE_URL = STOCK_URL + '?stock_code={stockcode}'

MARKET_URL = {namespace.ACE_MARKET: 'https://www.bursamalaysia.com/market_information/equities_prices?keyword=&top_stock=&board=ACE-MKT&alphabetical=&sector=&sub_sector=&per_page=50&page={page_number}',
              namespace.LEAP_MARKET: 'https://www.bursamalaysia.com/market_information/equities_prices?keyword=&top_stock=&board=LEAP-MKT&alphabetical=&sector=&sub_sector=&per_page=50&page={page_number}',
              namespace.MAIN_MARKET: 'https://www.bursamalaysia.com/market_information/equities_prices?keyword=&top_stock=&board=MAIN-MKT&alphabetical=&sector=&sub_sector=&per_page=50&page={page_number}',
              namespace.STRUCTURED_WARRANTS: 'https://www.bursamalaysia.com/market_information/equities_prices?keyword=&top_stock=&board=WARRANTS&alphabetical=&sector=&sub_sector=&per_page=50&page={page_number}',
              namespace.ETF: 'https://www.bursamalaysia.com/market_information/equities_prices?keyword=&top_stock=&board=ETF&alphabetical=&sector=&sub_sector=&per_page=50&page={page_number}',
              namespace.BOND: 'https://www.bursamalaysia.com/market_information/equities_prices?keyword=&top_stock=&board=BOND%26LOAN&alphabetical=&sector=&sub_sector=&per_page=50&page={page_number}'
              }


class BursaApi:

    def __init__(self):
        pass

    def screenerResultPostProcessing(self, series):
        args = series['Name'].split(' ')
        name, status = args[0], args[-1]
        if status == name:
            status = ''
        series['Name'] = name
        series['Status'] = status

        series['URL'] = STOCK_CODE_URL.format(stockcode=series['Code'])
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

    def exportMarket(self, ioLogfolder, market):
        market_filepath = self.exportMarketFilepath(market, ioLogfolder.path)
        if not exists(market_filepath):
            df = self.getMarket(market)
            df.drop(['No'], axis=1, inplace=True)
            df.insert(0, 'Date', ioLogfolder.name)
            df.insert(0, 'Reference Index', ioLogfolder.ref_index)
            df['Market'] = market
            df = df.apply(self.screenerResultPostProcessing, axis=1)
            df.to_excel(market_filepath, index=False)

    def exportScreener(self, ioLogfolder):
        processes = []
        for market in MARKET_URL.keys():
            process = Process(target=self.exportMarket, args=(ioLogfolder, market, ))
            processes.append(process)
        for process in processes:
            process.start()
        for process in processes:
            process.join()

        df = pandas.DataFrame()
        for market in MARKET_URL.keys():
            market_filepath = self.exportMarketFilepath(market, ioLogfolder.path)
            _df = pandas.read_excel(market_filepath, converters={'Code': str})
            df = pandas.concat([df, _df], ignore_index=True, sort=False)
        df.to_excel(self.exportFilepath(basepath=ioLogfolder.path), index=False)

    def exportScreenerIfNotExists(self, ioLogfolder):
        if not exists(self.exportFilepath(basepath=ioLogfolder.path)):
            while True:
                try:
                    self.exportScreener(ioLogfolder)
                    break
                except Exception as e:
                    logging.error(e)

            for market in MARKET_URL.keys():
                market_filepath = self.exportMarketFilepath(market, ioLogfolder.path)
                if exists(market_filepath):
                    os.remove(market_filepath)

    def exportMarketFilepath(self, market, basepath=''):
        filename = f'{market}.xlsx'
        return Utility._File(basepath, filename).path

    def exportFilepath(self, basepath='', filename='bursa_screener.xlsx'):
        return Utility._File(basepath, filename).path


if __name__ == '__main__':
    pass
