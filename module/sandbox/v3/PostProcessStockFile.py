from enum import Enum
import pandas
import sys

import Project
Project.sys_path_initialize()

from Bursa import attributes


class StockAttribute(Enum):

    MarketStatus = 0
    TickSize = 1
    TickSizeRemark = 2


class StockRemarkAttribute(Enum):

    OpenAndClosePriceMismatch = 0

class PriceRange(Enum):

    LessThanOne = 0
    OneToLessThanTen = 1
    TenToLessThanHundred = 2
    MoreThanHundred = 3


class PriceRangeClassifier:

    @staticmethod
    def classify(value):
        _priceRange_cls = PriceRange
        if value < 1.00:
            return _priceRange_cls(0).value
        elif value < 10.00:
            return _priceRange_cls(1).value
        elif value < 100.00:
            return _priceRange_cls(2).value
        elif value >= 100.00:
            return _priceRange_cls(3).value
        else:
            raise ValueError("Unexpected price %s" % value)


def CalcTickSize(row):

    data = []

    _stock_attr = attributes.StockAttribute

    change_price = row[_stock_attr(3).name]
    open_price = row[_stock_attr(11).name]
    close_price = row[_stock_attr(17).name]

    if change_price == '0.000':
        return 0

    open_price = float(open_price)
    close_price = float(close_price)

    open_price_category = PriceRangeClassifier().classify(open_price)
    close_price_category = PriceRangeClassifier().classify(close_price)
    if open_price_category < close_price_category:
        if open_price_category == 0:
            temp = [open_price, 1.00, 0.005]
        elif open_price_category == 1:
            temp = [open_price, 10.00, 0.01]
        elif open_price_category == 2:
            temp = [open_price, 100.00, 0.02]
        data.append(temp)
        if close_price_category == 1:
            temp = [1.00, close_price, 0.01]
        elif close_price_category == 2:
            temp = [10.00, close_price, 0.02]
        elif close_price_category == 3:
            temp = [100.00, close_price, 0.1]
        data.append(temp)
    elif open_price_category > close_price_category:
        if open_price_category == 1:
            temp = [1.00, open_price, 0.01]
        elif open_price_category == 2:
            temp = [10.00, open_price, 0.02]
        data.append(temp)
        if close_price_category == 0:
            temp = [close_price, 1.00, 0.005]
        elif close_price_category == 1:
            temp = [close_price, 10.00, 0.01]
        elif close_price_category == 2:
            temp = [close_price, 100.00, 0.02]
        data.append(temp)
    else:
        if open_price_category == 0:
            tick = 0.005
        elif open_price_category == 1:
            tick = 0.01
        elif open_price_category == 2:
            tick = 0.02
        elif open_price_category == 3:
            tick = 0.10
        else:
            raise ValueError("Per tick value not defined.")

        data.append([open_price, close_price, tick])

    count = 0

    for index, info in enumerate(data):
        open_price = info[0]
        close_price = info[1]
        tick = info[2]
        size = abs(close_price - open_price) / tick
        count += size

    return count


def TickSizeRemark(row):

    _stock_attr = attributes.StockAttribute
    _new_stock_attr = StockAttribute
    _remark_attr = StockRemarkAttribute

    tick_size = row[_new_stock_attr(1).name]
    open_price = row[_stock_attr(11).name]
    close_price = row[_stock_attr(17).name]

    if tick_size == 0 and open_price != close_price:
        return _remark_attr(0).name
    return None


def OpenMarketLbl(row):

    _market_attr = attributes.OpenStockMarketStatusLabel
    _stock_attr = attributes.StockAttribute

    last_closed_price = row[_stock_attr(10).name]
    open_price = row[_stock_attr(11).name]

    if open_price == '-':
        return _market_attr(1).name

    if last_closed_price == '-':
        last_closed_price = open_price

    last_closed_price = float(last_closed_price)
    open_price = float(open_price)

    if last_closed_price == open_price:
        return _market_attr(2).name
    elif last_closed_price < open_price:
        return _market_attr(3).name
    elif last_closed_price > open_price:
        return _market_attr(4).name
    else:
        return _market_attr(0).name


def PostProcess(inFile, outFile):

    _stock_attr = attributes.StockAttribute
    _extra_stock_attr = StockAttribute

    # Read dataframe
    dataframe = pandas.read_csv(inFile, index_col=None)

    # Replace empty volume to zero
    dataframe.loc[dataframe[_stock_attr(5).name] == '-', _stock_attr(5).name] = 0

    # Replace no change to zero
    dataframe.loc[dataframe[_stock_attr(3).name] == '-', _stock_attr(3).name] = '0.000'
    dataframe.loc[dataframe[_stock_attr(4).name] == '-', _stock_attr(4).name] = '0.00'

    # Label open market status
    dataframe[_extra_stock_attr(0).name] = dataframe.apply (lambda row: OpenMarketLbl(row), axis=1)

    # Calculate tick size and remark
    dataframe[_extra_stock_attr(1).name]= dataframe.apply (lambda row: CalcTickSize(row), axis=1)
    dataframe[_extra_stock_attr(2).name]= dataframe.apply (lambda row: TickSizeRemark(row), axis=1)

    dataframe.to_csv(outFile, index=False)
    return 0


def FiavestEOD(inFile, outFile):

    _stock_attr = attributes.StockAttribute
    _extra_stock_attr = StockAttribute

    # Read dataframe
    dataframe = pandas.read_csv(inFile, index_col=None)
    dataframe[_stock_attr(5).name] = dataframe[_stock_attr(5).name].str.replace(',', '').astype(int)
    result = dataframe[(dataframe[_stock_attr(5).name] >= 40000) & (dataframe[_extra_stock_attr(1).name] >= 8)]

    result = result.astype({_stock_attr(11).name:'float64', _stock_attr(17).name:'float64'})
    result = result[(result[_stock_attr(17).name] > result[_stock_attr(11).name])]

    result = result.drop(['ChangePercentage', 'BuyVolume', 'Buy', 'Sell', 'SellVolume', 'Date', 'Time'], axis=1)
    print(result.head())

    header = ['Market', 'Sector', 'Company', 'Code', 'LACP', 'Open', 'High', 'Low', 'Close', 'Volume', 'MarketStatus', 'Change', 'TickSize', 'TickSizeRemark', 'Remark', 'BursaURL']
    result = result[header]
    result.to_csv(outFile, index=False)


if __name__ == "__main__":
    pass
