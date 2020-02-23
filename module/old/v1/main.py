# -*- coding: utf-8 -*-

from os.path import exists
import datetime
import logging
import sys

from module import klse
from module import bursa
from module import Utility
from module import resources_manager
Utility.Project().system_path_initialize()

import pandas


class DateTracker:

    def __init__(self):

        _df = pandas.read_excel(__class__.filepath(), __class__.sheetname())
        _now = datetime.datetime.now()
        _now_fmt = _now.strftime('%Y-%m-%d')

        self.df = _df
        self.now = _now
        self.now_fmt = _now_fmt

        _now_df = _df[_df['Date'] == _now_fmt]
        self.now_index = _now_df.index.values.astype(int)[0]
        self.now_status = _now_df['Status'].values.astype(str)[0]
        self.now_ref_index = _now_df['Reference Index'].values.astype(int)[0]

    @staticmethod
    def filepath():
        return Utility.Project().config().path

    @staticmethod
    def sheetname():
        return 'date_track'


def _data_collection(ioLogFolder):

    logging.info('')
    logging.info('Proceeding to collect market and stock information...')

    if not exists(ioLogFolder.klse_screener_filepath()):
        logging.info('Exporting KLSE screener info...')
        klseApi = klse.ModuleApi(ioLogFolder)
        klseApi.exportScreenerResult()

    bursaApi = bursa.ModuleApi(ioLogFolder)
    if not exists(ioLogFolder.ace_leap_main_filepath()):
        logging.info('Exporting Bursa screener info...')
        bursaApi.exportScreenerResult()

    logging.info('Collecting stocks historical price...')
    if bursaApi.exportAllStockHistoricalData():
        return 1

    Utility.makeFile(ioLogFolder.finishing_filepath())


def _update_resource_package(basepath, _now):

    _timestamp = f'{_now.now_index}:{_now.now_ref_index}:{_now.now_fmt}'

    logging.info('')

    logging.info('Proceeding to update all the raw data file...')
    resources_manager.ResourceCentral().update_raw_data(basepath.profileFolder())

    logging.info('Updating tracker list...')
    resources_manager.ResourceCentral().updateTracker()

    logging.info('Updating stock historical profile...')
    resources_manager.ResourceCentral().updateStockProfile()
    
    logging.info('Exporting daily summary...')
    resources_manager.ResourceCentral().exportSummary()

    logging.info('Exporting timestamp check point...')
    resources_manager.ResourceCentral().setLastUpdate(_timestamp)


def _analyze_stock_market():
    logging.info('')
    logging.info('Proceeding to analyze the market...')
    logging.info('Finished analyzing the market...')


def main():

    # Initialization
    data_collection = False
    update_resource_package = False
    analyze_stock_market = True

    _project = Utility.Project()
    Utility.Logger().addStreamHandler()

    _dateTracker = DateTracker()

    if _dateTracker.now_ref_index > resources_manager.ResourceCentral().last_update_ref_index:
        update_resource_package = True

    _log = _project.run_log(_dateTracker.now_fmt)
    if not exists(_log.path):
        data_collection = True
        Utility.makeFolder(_log.path)
    elif not exists(_log.finishing_filepath()):
        data_collection = True

    if data_collection and _data_collection(_log):
        logging.error('Failed to collect raw stock market data...')
        return 1

    if update_resource_package:
        _update_resource_package(_log, _dateTracker)

    if analyze_stock_market:
        _analyze_stock_market()

    return 0


if __name__ == '__main__':
    returncode = main()
    sys.exit(returncode)
