# -*- coding: utf-8 -*-

from project import Folder, File, Project


class FileNameManagement:

    def __init__(self, basename):
        self.basename = basename
        self.basepath = Folder(Project().SubFolder.logs.path, basename).path

    def getMarketFileName(self, market):
        return '%s.csv' % market

    def getMarketFilePath(self, market):
        return File(self.basepath, self.getMarketFileName(market)).path

    def getBursaAllMarketFileName(self):
        return 'bursa_screener.csv'

    def getBursaAllMarketFilePath(self):
        return File(self.basepath, self.getBursaAllMarketFileName()).path

    def getBursaPLCMarketFileName(self):
        return 'bursa_public_listed_companies.csv'

    def getBursaPLCMarketFilePath(self):
        return File(self.basepath, self.getBursaPLCMarketFileName()).path

    def getStockFolder(self):
        return Folder(self.basepath, 'stocks').path

    def getStockFileName(self, stockid):
        return '%s.csv' % stockid

    def getStockFilePath(self, stockid):
        return File(self.getStockFolder(), self.getMarketFileName(stockid)).path

    def getKlseStockFileName(self):
        return 'klse_screener.csv'

    def getKlseStockFilePath(self):
        return File(self.basepath, self.getKlseStockFileName()).path


if __name__ == '__main__':
    pass
