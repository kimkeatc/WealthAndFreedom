# -*- coding: utf-8 -*-

from Utility import Project
Project().system_path_initialize()

import requests
import pandas

SCREENER_API_URL = 'https://www.klsescreener.com/v2/screener/quote_results'
STOCK_URL = 'https://www.klsescreener.com/v2/charting/chart/'
STOCK_CODE_URL = STOCK_URL + '{code}'


class ModuleApi:

    def __init__(self, ioLogFolder):
        self.ioLogFolder = ioLogFolder

    def _data_parser(self, series):
        args = series['Name'].split(' ')
        name, status = args[0], args[-1]

        args = series['Category'].split(' ')
        sector = ' '.join(args[0: -2])[:-1]
        market = ' '.join(args[-2:])

        if status == name:
            status = ''

        series['Name'] = name
        series['Sector'] = sector
        series['Market'] = market
        series['Status'] = status

        return series

    def getScreenerResult(self):
        r = requests.post(SCREENER_API_URL)
        r.raise_for_status()
        df = pandas.read_html(r.text)
        df = df[0].iloc[:, :-2]
        return df

    def exportScreenerResult(self):
        df = self.getScreenerResult()
        df.insert(0, 'Date', self.ioLogFolder.basename)

        df = df.apply(self._data_parser, axis=1)
        df['URL'] = STOCK_URL + df['Code'].map(str)
        df.to_excel(self.ioLogFolder.klse_screener_filepath(), index=False)


if __name__ == '__main__':
    pass
