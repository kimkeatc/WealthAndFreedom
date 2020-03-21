# -*- coding: utf-8 -*-

from os.path import abspath, dirname, exists, join
from multiprocessing.pool import ThreadPool
from bursa import bursa
from klse import klse
import threading
import logging
import json
import sys
import os

_MODULE_FOLDER = abspath(join(dirname(__file__), '..'))
if _MODULE_FOLDER not in sys.path:
    sys.path.append(_MODULE_FOLDER)

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import namespace
import utility
utility.MyProject().system_path_initialize()
threadLocal = threading.local()

import requests
import pandas

pandas.set_option('display.max_rows', 1000)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)
pandas.set_option('float_format', '{:.3f}'.format)
pandas.set_option('expand_frame_repr', False)

STOCK_API_BASE_URL = 'https://ws20.bursamalaysia.com/api/v2/stock_price_data?stock_code'


def loadDataFrame(filepath):
    df = pandas.read_excel(filepath)
    df = df[df['Market'].isin([namespace.ACE_MARKET, namespace.LEAP_MARKET, namespace.MAIN_MARKET])]
    df = df[df['Code'].astype(str).str.isdigit()]
    return df


def getWebdriver():
    driver = getattr(threadLocal, 'driver', None)
    if driver is None:
        _capabilities = DesiredCapabilities.CHROME
        _capabilities['loggingPrefs'] = {'performance': 'ALL'}
        _options = Options()
        _options.add_experimental_option('w3c', False)
        _options.add_argument("--headless")

        driver = webdriver.Chrome(utility.MyProject().chromeWebdriver.path,
                                  desired_capabilities=_capabilities,
                                  options=_options)
        setattr(threadLocal, 'driver', driver)
    return driver

def getPerformanceNetworkURL(pkg):
    args = pkg.split(';')
    filepath, url = args[0], args[1]
    if exists(filepath):
        return
    if exists(filepath.replace('.txt', '.xlsx')):
        return

    driver = getWebdriver()
    try:
        driver.get(url)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'highcharts-plot-background')))
    except TimeoutException:
        return

    for network in driver.get_log('performance'):
        if STOCK_API_BASE_URL in str(network):
            url = json.loads(network['message'])['message']['params']['request']['url']
            if not url:
                return
            break

    with open(filepath, 'w') as f:
        f.write(url)

def getHistoricalData(filepath):
    if not exists(filepath):
        return
    dst_filepath = filepath.replace('.txt', '.xlsx')
    with open(filepath, 'r') as f:
        url = f.read()
    r = requests.get(url)
    df = pandas.DataFrame(r.json()['historical_data']['data'])
    df.insert(0, 'timestamp', df['date'].div(1000).astype(int))
    df['date'] = pandas.to_datetime(df['timestamp'], unit='s').dt.strftime('%Y-%m-%d')
    df = df.tail(10)

    df.to_excel(dst_filepath, index=False)
    os.remove(filepath)


def main(basefolder):
    logging.info('Loading dataframe...')
    filepath = bursa.BursaApi().exportFilepath(basefolder)
    df = loadDataFrame(filepath)

    tempFolder = utility._Folder(basefolder, 'temp')
    tempFolder.create()

    df['temp_filepath'] = df['Code'].apply(lambda c: os.path.join(tempFolder.path, c + '.txt'))
    df['package'] = df['temp_filepath'] + ';' + df['URL']

    logging.info('Getting performance urls...')
    ThreadPool(7).map(getPerformanceNetworkURL, df['package'])
    os.system('TASKKILL /IM chromedriver.exe')

    listdir = os.listdir(tempFolder.path)
    if len(listdir) != len(df['package']):
        logging.error('Package data not complete...')
        return 0

    logging.info('Loading performance urls...')
    ThreadPool(7).map(getHistoricalData, df['temp_filepath'])


if __name__ == '__main__':
    pass
