# -*- coding: utf-8 -*-

from os.path import abspath, dirname, exists, join
import sys

_MODULE_FOLDER = abspath(join(dirname(__file__), '..'))
if _MODULE_FOLDER not in sys.path:
    sys.path.append(_MODULE_FOLDER)

import Utility
Utility.MyProject().system_path_initialize()

import requests
import pandas

pandas.set_option('display.max_rows', 1000)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)
pandas.set_option('float_format', '{:.3f}'.format)
pandas.set_option('expand_frame_repr', False)

SCREENER_API_URL = 'https://www.klsescreener.com/v2/screener/quote_results'
STOCK_CHART_URL = 'https://www.klsescreener.com/v2/charting/chart/'
STOCK_CODE_CHART_URL = STOCK_CHART_URL + '{stockcode}'

STOCK_API_HISTORY_URL = 'https://www.klsescreener.com/v2/trading_view/history?symbol={stockcode}&resolution={start_time}&from=%i&to={end_time}'
STOCK_API_REMARK_URL = 'https://www.klsescreener.com/v2/trading_view/marks?symbol={stockcode}&from={start_time}&to={end_time}&resolution=D'


class KlseApi:

    def __init__(self):
        pass

    def screenerResultPostProcessing(self, series):
        args = series['Name'].split(' ')
        name, status = args[0], args[-1]
        if status == name:
            status = ''

        args = series['Category'].split(' ')
        sector = ' '.join(args[0: -2])[:-1]
        market = ' '.join(args[-2:])

        series['Name'] = name
        series['Sector'] = sector
        series['Market'] = market
        series['Status'] = status
        series['Charting URL'] = STOCK_CHART_URL + series['Code']
        return series

    def getScreener(self):
        r = requests.post(SCREENER_API_URL)
        r.raise_for_status()
        df = pandas.read_html(r.text)
        df = df[0].iloc[:, :-2]
        return df

    def exportScreener(self, ioLogfolder):
        df = self.getScreener()
        df.insert(0, 'Date', ioLogfolder.name)
        df.insert(0, 'Reference Index', ioLogfolder.ref_index)
        df = df.apply(self.screenerResultPostProcessing, axis=1)
        df.to_excel(self.exportFilepath(basepath=ioLogfolder.path), index=False)

    def exportScreenerIfNotExists(self, ioLogfolder):
        if not exists(self.exportFilepath(basepath=ioLogfolder.path)):
            self.exportScreener(ioLogfolder)

    def exportFilepath(self, basepath='', filename='klse_screener.xlsx'):
        return Utility._File(basepath, filename).path


if __name__ == '__main__':
    pass
