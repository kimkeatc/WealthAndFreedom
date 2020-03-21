# -*- coding: utf-8 -*-

from os.path import abspath, exists, join
import logging

import project
project.Project().PathInitialize()

import numpy
import pandas
pandas.set_option('display.max_rows', 1000)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)
pandas.set_option('float_format', '{:.3f}'.format)
pandas.set_option('expand_frame_repr', False)

from filename_management import FileNameManagement
from common import *
import Utility
import bursa
import klse


class Master(FileNameManagement):

    def __init__(self, ref=''):

        if not ref:
            refFolder = project.Project().SubFolder.logs.listdir()[-1]
            ref = join(project.Project().SubFolder.logs.path, refFolder)
        FileNameManagement.__init__(self, ref)

        if not exists (__class__.configFile().path):
            logging.info('Create empty master tracking file...')
            self.setup()

    def setup(self):
        dfKLSE = self.getDataframeKlseScreener()
        dfBursa = self.getDataframeBursaScneener()

        df = pandas.merge(dfKLSE, dfBursa, how='right', on=['Code'])

        df = df[['Name_x', 'Code', 'Category']]
        df = df.rename(columns={'Name_x': 'Name'})

        df.dropna(subset=['Category'], inplace=True)
        df['Sector'] = df['Category'].apply(lambda x: ' '.join(x.split(' ')[0: -2])[:-1])
        df['Market Type'] = df['Category'].apply(lambda x: ' '.join(x.split(' ')[-2:]))
        df.drop(['Category'], axis=1, inplace=True)

        df['Name'] = df['Name'].apply(lambda x: x.split(' ')[0])
        df['Tags'] = numpy.nan
        df['Start_Date'] = numpy.nan
        df.sort_values(['Sector', 'Code'], ascending=[1, 1], inplace=True)
        df.to_excel(__class__.configFile().path, index=False)

    def getDataframeKlseScreener(self):
        return pandas.read_csv(self.getKlseStockFilePath())

    def getDataframeBursaScneener(self):
        df = pandas.DataFrame()
        for market in [BURSA_MARKET_ACE_MARKET, BURSA_MARKET_LEAP_MARKET, BURSA_MARKET_MAIN_MARKET]:
            _df = pandas.read_csv(self.getMarketFilePath(market), dtype={'Code': str})
            df = pandas.concat([df, _df], ignore_index=True)
        return df

    @staticmethod
    def configFile():
        return project.File(project.Project().SubFolder.data.path, 'master.xlsx')


if __name__ == '__main__':
    # https://pythonprogramming.net/more-stock-data-manipulation-python-programming-for-finance/
    cls = Master()

    content = ''

    df = pandas.read_csv(cls.getStockFilePath('6633'))
    df = df.loc[(df['Date'] >= 20191209 )]
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df['Volume'] = df['Volume'].astype(str)
    df['Volume'] = df['Volume'].apply(lambda x: x[0: -2])
    df.reset_index(inplace=True, drop=True)
    df.index += 1
    df = df.T
    content = content + '<h2>LHI (6633) <a href=\'%s\'>Screener</a> </h2><hr>' % klse.STOCK_CODE_URL.format(stock_id='6633') + df.to_html()

    df = pandas.read_csv(cls.getStockFilePath('0008'))
    df = df.loc[(df['Date'] >= 20191210 )]
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df['Volume'] = df['Volume'].astype(str)
    df['Volume'] = df['Volume'].apply(lambda x: x[0: -2])
    df.reset_index(inplace=True, drop=True)
    df.index += 1
    df = df.T
    content = content + '<h2>WILLOW (0008) <a href=\'%s\'>Screener</a> </h2><hr>' % klse.STOCK_CODE_URL.format(stock_id='0008') + df.to_html()

    df = pandas.read_csv(cls.getStockFilePath('0198'))
    df = df.loc[(df['Date'] >= 20191217 )]
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df['Volume'] = df['Volume'].astype(str)
    df['Volume'] = df['Volume'].apply(lambda x: x[0: -2])
    df.reset_index(inplace=True, drop=True)
    df.index += 1
    df = df.T
    content = content + '<h2>GDB (0198) <a href=\'%s\'>Screener</a> </h2><hr>' % klse.STOCK_CODE_URL.format(stock_id='0198') + df.to_html()

    df = pandas.read_csv(cls.getStockFilePath('5070'))
    df = df.loc[(df['Date'] >= 20191218 )]
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df['Volume'] = df['Volume'].astype(str)
    df['Volume'] = df['Volume'].apply(lambda x: x[0: -2])
    df.reset_index(inplace=True, drop=True)
    df.index += 1
    df = df.T
    content = content + '<h2>PRTASCO (5070) <a href=\'%s\'>Screener</a> </h2><hr>' % klse.STOCK_CODE_URL.format(stock_id='5070') + df.to_html()

    df = pandas.read_csv(cls.getStockFilePath('5073'))
    df = df.loc[(df['Date'] >= 20191223 )]
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df['Volume'] = df['Volume'].astype(str)
    df['Volume'] = df['Volume'].apply(lambda x: x[0: -2])
    df.reset_index(inplace=True, drop=True)
    df.index += 1
    df = df.T
    content = content + '<h2>NAIM (5073) <a href=\'%s\'>Screener</a> </h2><hr>' % klse.STOCK_CODE_URL.format(stock_id='5073') + df.to_html()

    df = pandas.read_csv(cls.getStockFilePath('5247'))
    df = df.loc[(df['Date'] >= 20191226 )]
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df['Volume'] = df['Volume'].astype(str)
    df['Volume'] = df['Volume'].apply(lambda x: x[0: -2])
    df.reset_index(inplace=True, drop=True)
    df.index += 1
    df = df.T
    content = content + '<h2>KAREX (5247) <a href=\'%s\'>Screener</a> </h2><hr>' % klse.STOCK_CODE_URL.format(stock_id='5247') + df.to_html()

    df = pandas.read_csv(cls.getStockFilePath('5216'))
    df = df.loc[(df['Date'] >= 20191230 )]
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df['Volume'] = df['Volume'].astype(str)
    df['Volume'] = df['Volume'].apply(lambda x: x[0: -2])
    df.reset_index(inplace=True, drop=True)
    df.index += 1
    df = df.T
    content = content + '<h2>DSONIC (5216) <a href=\'%s\'>Screener</a> </h2><hr>' % klse.STOCK_CODE_URL.format(stock_id='5216') + df.to_html()

    df = pandas.read_csv(cls.getStockFilePath('5222'))
    df = df.loc[(df['Date'] >= 20191230 )]
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df['Volume'] = df['Volume'].astype(str)
    df['Volume'] = df['Volume'].apply(lambda x: x[0: -2])
    df.reset_index(inplace=True, drop=True)
    df.index += 1
    df = df.T
    content = content + '<h2>FGV (5222) <a href=\'%s\'>Screener</a> </h2><hr>' % klse.STOCK_CODE_URL.format(stock_id='5222') + df.to_html()

    df = pandas.read_csv(cls.getStockFilePath('0176'))
    df = df.loc[(df['Date'] >= 20200102 )]
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df['Volume'] = df['Volume'].astype(str)
    df['Volume'] = df['Volume'].apply(lambda x: x[0: -2])
    df.reset_index(inplace=True, drop=True)
    df.index += 1
    df = df.T
    content = content + '<h2>KRONO (0176) <a href=\'%s\'>Screener</a> </h2><hr>' % klse.STOCK_CODE_URL.format(stock_id='0176') + df.to_html()

    df = pandas.read_csv(cls.getStockFilePath('5277'))
    df = df.loc[(df['Date'] >= 20200102 )]
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df['Volume'] = df['Volume'].astype(str)
    df['Volume'] = df['Volume'].apply(lambda x: x[0: -2])
    df.reset_index(inplace=True, drop=True)
    df.index += 1
    df = df.T
    content = content + '<h2>FPGROUP (5277) <a href=\'%s\'>Screener</a> </h2><hr>' % klse.STOCK_CODE_URL.format(stock_id='5277') + df.to_html()

    df = pandas.read_csv(cls.getStockFilePath('0065'))
    df = df.loc[(df['Date'] >= 20200102 )]
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df['Volume'] = df['Volume'].astype(str)
    df['Volume'] = df['Volume'].apply(lambda x: x[0: -2])
    df.reset_index(inplace=True, drop=True)
    df.index += 1
    df = df.T
    content = content + '<h2>EFORCE (0065) <a href=\'%s\'>Screener</a> </h2><hr>' % klse.STOCK_CODE_URL.format(stock_id='0065') + df.to_html()

    df = pandas.read_csv(cls.getStockFilePath('0157'))
    df = df.loc[(df['Date'] >= 20200102 )]
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df['Volume'] = df['Volume'].astype(str)
    df['Volume'] = df['Volume'].apply(lambda x: x[0: -2])
    df.reset_index(inplace=True, drop=True)
    df.index += 1
    df = df.T
    content = content + '<h2>FOCUSP (0157) <a href=\'%s\'>Screener</a> </h2><hr>' % klse.STOCK_CODE_URL.format(stock_id='0157') + df.to_html()

    df = pandas.read_csv(cls.getStockFilePath('5142'))
    df = df.loc[(df['Date'] >= 20200106 )]
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df['Volume'] = df['Volume'].astype(str)
    df['Volume'] = df['Volume'].apply(lambda x: x[0: -2])
    df.reset_index(inplace=True, drop=True)
    df.index += 1
    df = df.T
    content = content + '<h2>WASEONG (5142) <a href=\'%s\'>Screener</a> </h2><hr>' % klse.STOCK_CODE_URL.format(stock_id='5142') + df.to_html()

    with open('homework.html', 'w') as f:
        f.write(content)

    df = pandas.read_html(content)
    df[2].to_csv('homework.csv', index=False)
