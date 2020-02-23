from os.path import abspath, dirname, join
import datetime
import logging
import pandas
import sys

_MODULE_FOLDER = abspath(dirname(__file__))
if _MODULE_FOLDER not in sys.path:
    sys.path.append(_MODULE_FOLDER)

import Market

_START_DATE = datetime.date(year=1994, month=1, day=3)
_TODAY_DATE = datetime.date.today()
_END_DATE = datetime.date(year=2020, month=12, day=31)

_NOW = datetime.datetime.now()

_COMPARE = _TODAY_DATE - _START_DATE
_DATE_DIFF = _COMPARE.days


class FileTable:

    tblHeader_date = 'Date'
    tblHeader_day = 'Day'
    tblHeader_status = 'Status'

    def __init__(self, date, status):
        setattr(self, self.tblHeader_date, date)
        setattr(self, self.tblHeader_status, status)
        self.setDay()

        date = date.strftime('%Y%m%d')
        setattr(self, self.tblHeader_date, date)  # Reformat date value

    def setDay(self):
        date = getattr(self, self.tblHeader_date)
        day = date.strftime('%A')
        setattr(self, self.tblHeader_day, day)


class Record(FileTable):

    def __init__(self, name, from_date, until_date):
        self.record = []
        self.name = name
        self.from_date = from_date
        self.until_date = until_date

    @property
    def path(self):
        return abspath(join(_MODULE_FOLDER, self.name))

    def update(self):
        return None  # Placeholder, NOP

    def getDateRange(self):

        _range = []

        start = self.from_date
        end = self.until_date

        delta = end - start

        for i in range(delta.days + 1):
            day = start + datetime.timedelta(days=i)
            _range.append(day)

        return _range

    def addRecord(self, date, status):
        cls = FileTable(date, status)
        self.record.append(cls)


class _CalendarFile(Record):

    name = 'calendar.csv'
    start_date = _START_DATE
    end_date = _END_DATE

    def __init__(self):
        super().__init__(self.name, self.start_date, self.end_date)

    def update(self, exportFile=True):

        date_range = self.getDateRange()

        for index, date in enumerate(date_range):

            status = Market.MarketOperation().getOperatingStatus(date)
            self.addRecord(date, status)

        df = pandas.DataFrame([vars(record) for record in self.record])
        print(df.head())

        if exportFile:
            df.to_csv(self.path)


class _MarketFile(Record):

    name = 'market.csv'
    start_date = _START_DATE
    today_date = _TODAY_DATE

    def __init__(self):
        super().__init__(self.name, self.start_date, self.today_date)

    def update(self, exportFile=True):

        date_range = self.getDateRange()

        for index, date in enumerate(date_range):

            status = Market.MarketOperation().getOperatingStatus(date)
            if status == Market.MarketOperationStatus.Open.name:
                self.addRecord(date, status)

        df = pandas.DataFrame([vars(record) for record in self.record])
        print(df.tail())

        if exportFile:
            df.to_csv(self.path)


class Module:

    def __init__(self):
        pass

    def MarketFile(self):
        return _MarketFile()

    def CalendarFile(self):
        return _CalendarFile()

    def FilesUpdateTrialRun(self):
        # Calendar Module
        c = self.CalendarFile()
        c.update(exportFile=False)

        # Market Module
        m = self.MarketFile()
        m.update(exportFile=False)

    def FilesUpdate(self):
        # Calendar Module
        c = self.CalendarFile()
        c.update()
        logging.info('Successfully updated file %s' % c.path)

        # Market Module
        m = self.MarketFile()
        m.update()
        logging.info('Successfully updated file %s' % m.path)


if __name__ == '__main__':
    # Module().FilesUpdate()  # Unmask this line if want to update the files
    pass
