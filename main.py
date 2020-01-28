# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import logging
import sys

from module.fiavest_xt import fiavest_xt
from module.bursa import bursa
from module.klse import klse
from module import namespace
from module import Utility

Utility.MyProject().system_path_initialize()
Utility.Logger().addStreamHandler()

import pandas
import numpy

__module__ = sys.modules[__name__].__file__


class DateTracker:

    def __init__(self):
        self.df = pandas.read_excel(self.configurationFile().path, 'date_track')
        self.ref_index = None
        self.df_index = None
        self.date = None

        self.setDate()

    def configurationFile(self):
        return Utility.MyProject().configurationFile

    def getDate(self):
        df = self.df[self.df['Date'] <= datetime.now().strftime('%Y-%m-%d')]
        df = df[df['Status'] == namespace.Open].tail(1)
        return df

    def setDate(self):
        df = self.getDate()
        self.ref_index = df['Reference Index'].values[0]
        self.df_index = df.index.values[0]
        self.date = df['Date'].dt.strftime('%Y-%m-%d').values[0]


def _data_collection(ioLogfolder):

    logging.info('Getting KLSE screener...')
    klse.KlseApi().exportScreenerIfNotExists(ioLogfolder)

    logging.info('Getting Bursa screener...')
    bursa.BursaApi().exportScreenerIfNotExists(ioLogfolder)
    

def _data_update():
    pass


def _data_analysis():
    pass


def main():
    
    logging.info('+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+')

    _date = DateTracker()

    logFolder = Utility._Folder(Utility.MyProject().logsFolder.path, _date.date)
    logFolder.create()
    logFolder.addAttr('ref_index', _date.ref_index)
    logFolder.addAttr('df_index', _date.df_index)

    # Collecting date
    _data_collection(logFolder)
    
    return 0


if __name__ == '__main__':
    logging.info(f'Executing script {__module__}')
    returncode = main()
    logging.info(f'Finished executing script {__module__} with return code {returncode}...')
    sys.exit(returncode)
