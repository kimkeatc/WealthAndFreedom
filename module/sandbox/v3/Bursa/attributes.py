from enum import Enum


class Market:

    def __init__(self):
        _attr = MarketAttribute
        for index, attr in enumerate(_attr):
            attr_name = _attr(index).name
            setattr(self, attr_name, None)


class Index:

    def __init__(self):
        _attr = IndexAttribute
        for index, attr in enumerate(_attr):
            attr_name = _attr(index).name
            setattr(self, attr_name, None)


class Company:

    def __init__(self):
        _attr = CompanyAttribute
        for index, attr in enumerate(_attr):
            attr_name = _attr(index).name
            setattr(self, attr_name, None)


class Stock:

    def __init__(self):
        _attr = StockAttribute
        for index, attr in enumerate(_attr):
            attr_name = _attr(index).name
            setattr(self, attr_name, None)


class MarketAttribute(Enum):

    main_market = 0
    ace_market = 1
    leap_market = 2

    @staticmethod
    def List():
        return list(map(lambda c: c.name, MarketAttribute))


class IndexAttribute(Enum):
    
    Number = 0
    Name = 1
    Close = 2
    Open = 3
    Change = 4
    ChangePercentage = 5
    High = 6
    Low = 7

    @staticmethod
    def List():
        return list(map(lambda c: c.name, IndexAttribute))


class CompanyAttribute(Enum):

    Name = 0
    Code = 1
    BursaURL = 2
    Page = 3

    @staticmethod
    def List():
        return list(map(lambda c: c.name, CompanyAttribute))


class StockAttribute(Enum):

    Market = 0
    Sector = 1
    Code = 2
    Change = 3
    ChangePercentage = 4
    Volume = 5
    BuyVolume = 6
    Buy = 7
    Sell = 8
    SellVolume = 9
    LACP = 10
    Open = 11
    High = 12
    Low = 13
    Remark = 14
    Date = 15
    Time = 16
    Close = 17
    Company = 18

    @staticmethod
    def List():
        return list(map(lambda c: c.name, StockAttribute))

class OpenStockMarketStatusLabel(Enum):
    
    NotAvailable = 0
    MarketClosed = 1
    MarketNoChange = 2
    MarketGapUp = 3
    MarketGapDown = 4


if __name__ == "__main__":
    pass
