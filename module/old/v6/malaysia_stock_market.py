import datetime
import pandas
from holiday import Holiday


class MarketOpenedOperatingHour:

    def opening_hour(self):
        return datetime.time(9, 00)
    def closing_hour(self):
        return datetime.time(17, 00)
    def closing_hour_with_eod_info(self):
        return datetime.time(17, 15)

class MarketStatus(MarketOpenedOperatingHour, Holiday):

    def __init__(self, timestamp):
        MarketOpenedOperatingHour.__init__(self)
        self.timestamp = timestamp
        self.year_holiday = Holiday(self.timestamp.year).calender
        self.reason_on_market_closed = None
        self.open_market_status = None
        self.holiday = None
        self.last_market_is_today = False
        self.allow_to_get_market_info = True

        self.is_market_open_today = self.market_is_open()
        if self.is_market_open_today:
            self.market_open_status = self.get_open_market_status()
        else:
            self.reason_on_market_closed = self.market_close_status()

    def market_status_weekend_close(self):
        return "Weekend Today."
    def market_status_holiday_close(self, event):
        return "Holiday Today - %s" % event
    def market_status_is_opening_soon(self):
        return "Market is opening soon."
    def market_status_is_closing(self):
        self.last_market_is_today = True
        return "Market is closing."
    def market_status_is_closing_pending_web_info_to_get_update(self):
        self.last_market_is_today = True
        self.allow_to_get_market_info = False
        return "Market is closing - waiting web info to get update."
    def market_status_is_running(self):
        self.last_market_is_today = True
        self.allow_to_get_market_info = False
        return "Market is running."
    
    def get_open_market_status(self):
        if self.timestamp.time() >= self.closing_hour_with_eod_info():
            return self.market_status_is_closing()
        elif self.timestamp.time() >= self.closing_hour():
            return self.market_status_is_closing_pending_web_info_to_get_update()
        elif self.timestamp.time() >= self.opening_hour():
            return self.market_status_is_running()
        else:
            return self.market_status_is_opening_soon()
        
    def is_holiday(self, date):
        return True if date in self.year_holiday.keys() else False

    def market_close_status(self):
        return self.market_status_holiday_close(self.holiday) if self.holiday else self.market_status_weekend_close()

    def market_is_open(self):

        is_weekend_today = True if self.timestamp.weekday() >= 5 else False

        if is_weekend_today:
            return False
        elif self.is_holiday(self.timestamp.date()):
            self.holiday = self.year_holiday[self.timestamp.date()]
            return False
        else:
            return True
