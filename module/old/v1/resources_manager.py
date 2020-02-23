# -*- coding: utf-8 -*-

from datetime import datetime
from os.path import join, exists
import json
import logging
import os
import shutil

import Utility
Utility.Project().system_path_initialize()

import pandas
import numpy


class StockProfile:

    def __init__(self, foldername):
        self.foldername = foldername
        if not exists(self.stockfolder().path):
            Utility.makeFolder(self.stockfolder().path)
        if not exists(self.profile().path):
            df = pandas.DataFrame()
            df.to_excel(self.profile().path, index=False)

    def stockfolder(self):
        return Utility._Folder(Utility.Project().subfolder().resource_profile_folder.path, self.foldername)

    def profile(self):
        return Utility._File(self.stockfolder().path, 'historical.xlsx')

    def json_update(self, filepath):
        df = ResourceCentral.load_json_historical_data(filepath)
        df.insert(1, 'Date', numpy.nan)
        df['Date'] = df['date'].apply(lambda d: datetime.fromtimestamp(d / 1e3).strftime('%Y-%m-%d'))
        df.to_excel(self.profile().path, index=False)

class ResourceCentral:

    def __init__(self):
        _last_update = self.getLastUpdate()
        index, ref_index, date_fmt = _last_update.split(':')

        self.last_update_index = int(index)
        self.last_update_date_fmt = date_fmt
        self.last_update_ref_index = int(ref_index)

    def getLastUpdate(self):
        with open(__class__.recordFile().path, 'r') as f:
            date = f.read()
        return date

    def setLastUpdate(self, date):
        with open(__class__.recordFile().path, 'w') as f:
            f.write(date)

    def updateTracker(self):
        df = pandas.read_excel(__class__.trackerFile().path, converters={'Code': str})
        for filename in os.listdir(__class__.resource_src_folder().path):
            stock_code = filename.split('.')[0]
            filepath = join(__class__.resource_src_folder().path, filename)

            if df[df['Code'] == stock_code].empty:
                logging.warning(f'New stock code {stock_code} detected...')
                _df = __class__.load_json_historical_data(filepath)
                df = df.append({'Record start date': datetime.fromtimestamp(_df.iloc[0]['date'] / 1e3).strftime('%Y-%m-%d'),
                                'Name': _df.iloc[0]['name'],
                                'Code': stock_code}, ignore_index=True)
        df = df.sort_values('Code')
        df.to_excel(__class__.trackerFile().path, index=False)

    @staticmethod
    def load_json_historical_data(filepath):
        with open(filepath) as f:
            json_content = json.load(f)
        df = pandas.DataFrame(json_content['historical_data']['data'])
        return df

    @staticmethod
    def trackerFile():
        return Utility.Project().resource_tracker()

    @staticmethod
    def recordFile():
        return Utility.Project().resource_record()

    @staticmethod
    def resource_src_folder():
        return Utility.Project().subfolder().resource_src_folder

    @staticmethod
    def update_raw_data(src):

        for filename in os.listdir(src):
            filepath = join(src, filename)

            logging.info(f'Going to update raw data file name {filename}')
            shutil.copy(filepath, __class__.resource_src_folder().path)

    def updateStockProfile(self):
        _df = pandas.read_excel(__class__.trackerFile().path, converters={'Code': str})
        folderpath = __class__.resource_src_folder().path
        for index, filename in enumerate(os.listdir(folderpath)):
            filepath = join(folderpath, filename)
            stockcode = filename.split('.')[0]
            stockname = _df[_df['Code'] == stockcode]['Name'].values[0]
            stockfolder = f'{stockname}-{stockcode}'

            logging.info(f'Updating {stockfolder}...')
            stock = StockProfile(stockfolder)
            stock.json_update(filepath)

    def exportSummary(self):
        df = pandas.DataFrame()

        basefolder = Utility.Project().subfolder().resource_profile_folder.path
        for index, stockfolder in enumerate(os.listdir(basefolder)):
            stock = StockProfile(stockfolder)
            _df = pandas.read_excel(stock.profile().path, converters={'id': str})
            df = pandas.concat([df, _df], ignore_index=True)

        lstDate = set(df['Date'].to_list())        
        basefolder = Utility.Project().subfolder().resource_summary_folder.path
        for foldername in set(df['Date'].to_list()):
            filepath = join(basefolder, foldername + '.xlsx')
            if not exists(filepath):
                _df = df[df['Date'] == foldername]
                _df.to_excel(filepath, index=False)


if __name__ == '__main__':
    pass
