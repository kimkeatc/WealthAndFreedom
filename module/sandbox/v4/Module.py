__description__ = """ In-house Malaysia company stocks trade system.
"""

__author__ = 'Chin Kim Keat'
__credits__ = []
__maintainer__ = 'Chin Kim Keat'
__email__ = 'kim.keat.chin@outlook.com'

__contact__ = ''

__py_ver__ = (3, 7)

__module__ = ''
__version__ = '4.0.0'
__date__ = '10 November 2019'
__status__ = 'Development'

import logging

from script import Project

Project.ModuleFiles().ProjectInit()

from script.StockMarket import Market, Record
from script import Utility


def GetStockData():
    pass


def PostProcessStockData():
    pass


def main():

    Utility.Logger().addStreamHandler()

    _now = Record._NOW
    _now_date = _now.strftime('%d %b %Y')
    _now_time = _now.strftime('%H:%M:%S')

    _market_status = Market.MarketOperation().getOperatingStatus(_now)

    logging.info('')
    logging.info('%s' % _now)
    logging.info('Date: %s' % _now_date)
    logging.info('Time: %s' % _now_time)
    logging.info('Market Status: %s' % _market_status)

    # Step 1: Getting all data
    GetStockData()

    # Step 2: Post-process data
    PostProcessStockData()

    return


if __name__ == '__main__':
    main()
