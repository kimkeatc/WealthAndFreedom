# -*- coding: utf-8 -*-
__description__ = '''
'''

from os.path import basename, exists, join, splitext
import logging
import os
import shutil
import sys

__author__ = 'Chin Kim Keat'
__contact__ = 'kim.keat.chin@outlook.com'

__module__ = sys.modules[__name__]

from module.bursa import ModuleApi as BursaModuleApi
from module.klse import ModuleApi as KlseModuleApi
from module.project import Project
from module.master import Master
from module import Utility

Project().PathInitialize()

import pandas

_DATE_FORMATTED = Utility.getNowTime('%Y%m%d')
_DATED_LOG_FOLDER = join(Project().SubFolder.logs.path, _DATE_FORMATTED)

_MODULE_LOG_FILE = splitext(basename(__module__.__file__))[0] + '.log'
_DATED_MODULE_LOG_FILEPATH = join(_DATED_LOG_FOLDER, _MODULE_LOG_FILE)

_DATE_DF = pandas.read_excel(Project().holidaysFilepath())


def getDateIndex(date):
    _date = pandas.to_datetime(date, format='%Y%m%d')
    return _DATE_DF[_DATE_DF['Date'] == _date].index[0]


def updateResource(bursaInst):

    _last_update_date_index = 0
    _today_date_index = getDateIndex(_DATE_FORMATTED)

    _src_path = bursaInst.getStockFolder()
    if not exists(_src_path):
        logging.info(f'Sourcing directory not found... {_src_path}')
        return 1

    if not os.listdir(_src_path):
        logging.info(f'Empty stocks profile inside sourcing directory...')
        return 1

    _last_update_file_path = Project().lastUpdateFilepath()
    if exists(_last_update_file_path):
        with open(_last_update_file_path, 'r') as f:
            _last_update_date = f.read()
        logging.warning(f'Data was updated in {_last_update_date}')
        _last_update_date_index = getDateIndex(_last_update_date)

    if _today_date_index >= _last_update_date_index:
        logging.info('Going to update all the resource data...')

        shutil.copytree(_src_path, Project().SubFolder.data.path, copy_function=shutil.copy)
        with open(_last_update_file_path, 'w') as f:
            f.write(_DATE_FORMATTED)


def dataCollection(basename):
    # Initialize bursa api
    bursaModuleApi = BursaModuleApi(basename)
    klseModuleApi = KlseModuleApi(basename)

    logging.info('Screening markets from KLSE dashboard...')
    klseModuleApi.exportAllMarket()

    logging.info('Screening markets from Bursa dashboard...')
    bursaModuleApi.getAllMarkets()

    logging.info('Getting market historical chart...')
    if bursaModuleApi.getStocksHistory():
        raise EOFError('Failed to finish collecting all market historical chart...')

    logging.info('Updating open price on ace, leap and main markets stock...')
    bursaModuleApi.updatePublicListedCompanyOpenPrice()

    # updateResource(bursaModuleApi)

    logging.info('Finished getting market historical chart...')


def run():

    # Setup logging
    logger = Utility.LoggerSetup()
    logger.addStreamHandler()
    if not exists(_DATED_LOG_FOLDER):
        Utility.folderCreation(_DATED_LOG_FOLDER, 0o770)
    logger.addFileHandler(_DATED_MODULE_LOG_FILEPATH, 'w', logging.DEBUG)

    logging.info('')
    logging.info(f'Running date {_DATE_FORMATTED}')
    logging.info(f'Folder path: {_DATED_LOG_FOLDER}')
    logging.info('')

    # Data collection
    dataCollection(_DATE_FORMATTED)

    # Handler master file

    return 0


if __name__ == '__main__':
    print('Executing project named %s...' % __module__.__file__)
    returncode = run()
    print('Finished executing project...')
    sys.exit(returncode)
