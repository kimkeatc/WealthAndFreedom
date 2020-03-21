import pandas
import sys_path

class Holiday:

    def __init__(self, year):
        self.year = year
        self.calender = self.get_holiday_list()

    def get_holiday_excel_file(self):
        cls = sys_path._ppath()
        return cls.get_path((cls.holiday_excel_file_path))
        
    def get_holiday_list(self):

        df = pandas.read_excel(self.get_holiday_excel_file(), sheet_name=str(self.year))

        hlist = {}
        for row_index, row_value in df.to_dict(orient="index").items():
            event_name = row_value["Event"]
            event_date = row_value["Date"].date()
            hlist.update({event_date: event_name})
        return hlist
