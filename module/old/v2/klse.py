# -*- coding: utf-8 -*-

__module__ = ''
__description__ = '''
'''

__author__ = ''
__contact__ = ''

__credits__ = []

__version__ = ''
__date__ = ''
__status__ = 'Development'

from os.path import exists

from project import Project
Project().PathInitialize()

import requests
import pandas

from filename_management import FileNameManagement

STOCK_CODE_URL = 'https://www.klsescreener.com/v2/charting/chart/{stock_id}'


class ModuleApi(FileNameManagement):

    def __init__(self, basename):
        FileNameManagement.__init__(self, basename)

    def getAllMarket(self):
        _url = 'https://www.klsescreener.com/v2/screener/quote_results'
        response = requests.post(_url)
        if response.status_code == 200:
            return pandas.read_html(response.text)

    def exportAllMarket(self):
        if not exists(self.getKlseStockFilePath()):
            df = self.getAllMarket()
            df = df[0].iloc[:, :-2]
            df['Code'] = '\'' + df['Code'].astype(str)
            df['Date'] = self.basename
            df.to_csv(self.getKlseStockFilePath(), index=False)


if __name__ == '__main__':
    pass
