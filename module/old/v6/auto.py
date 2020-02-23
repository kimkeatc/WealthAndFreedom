import datetime
import logging
import os
import pandas
import sys
import traceback

from etc.sys_path import _ppath
ppath = _ppath()

from etc import sys_logger
from etc.malaysia_stock_market import MarketStatus
from etc.interact_klse_web_screener_with_selenium import KLSE


def _get_whole_stock_market_file_record(market, date=None):
    """ Given time and date(optional) to constuct whole market file directory."""
    date = date if date else market.timestamp.date()
    record_file_name = "whole-market-%s.csv" % str(date)
    return os.path.join(ppath.history, record_file_name)

def _get_stock_record_file(market, date=None):
    """ Given time and date(optional) to constuct stock market file directory."""    
    date = date if date else market.timestamp.date()
    record_file_name = "market-%s.csv" % str(date)
    return os.path.join(ppath.history, record_file_name)

def _get_last_market_date(market):
    """The function purpose to get the last opened market."""
    date = market.timestamp.date()
    while True:
        date = date - datetime.timedelta(days=1)
        date = datetime.datetime(*date.timetuple()[:6]).date()
        if date.weekday() >= 5 or market.is_holiday(date):
            continue
        return date

def _get_whole_market(market):
    """To get whole KLSE market."""
    record_file_path = _get_whole_stock_market_file_record(market)
    try:
        logging.info("Looking for whole market file: %s" % record_file_path)
        if os.path.exists(record_file_path):
            logging.info("File found... begin to load the information...")
            record = pandas.read_csv(record_file_path)
        else:
            logging.info("File not found... begin to get and export the information into file...")
            record = KLSE().whole_market_info(export_path=record_file_path)
        logging.info("Information retrieved... record as shown.")
        logging.warning(record)
        return 0
    except Exception:
        logging.critical("Failed to retrieve whole market information...")
        logging.error(traceback.format_exc())
        return 1

def _get_stock(market):
    status_code = 0
    date = market.timestamp.date()
    if not market.last_market_is_today:
        date = _get_last_market_date(market)

    stock_checklist_file_path = _get_whole_stock_market_file_record(market, date)
    logging.info("Begin to load reference whole market file: %s" % stock_checklist_file_path)
    
    stock_checklist_df = pandas.read_csv(stock_checklist_file_path)
    stock_record_file_path = _get_stock_record_file(market, date)

    checklist_code = stock_checklist_df["Code"].str[1:].astype(str).to_list()
    checklist_url = stock_checklist_df["URL"].astype(str).to_list()

    if not os.path.exists(stock_record_file_path):
        logging.info("File not found...begin to load information...")
        code_list = checklist_code
        url_list = checklist_url
    else:
        logging.info("File found...")
        stock_record = pandas.read_csv(stock_record_file_path)
        existing_code_list = stock_record["Code"].str[1:].astype(str).to_list()
        existing_url_list = stock_checklist_df["URL"].astype(str).to_list()

        code_list, url_list = [], []
        length_of_existing = len(existing_code_list)
        length_of_full = len(checklist_code)
        if length_of_existing != length_of_full:
            logging.info("File information is not complete...")
            code_list = checklist_code[length_of_existing:]
            url_list = checklist_url[length_of_existing:]
        else:
            logging.info("Information complete...")

    amount_of_stocks = len(code_list)
    if code_list:
        status_code = KLSE().stock_market_info(zip(code_list,url_list), stock_record_file_path, amount_of_stocks)
        
    #while(code_list):
    #    index = None
    #    index = KLSE().stock_market_info(zip(code_list,url_list), stock_record_file_path, amount_of_stocks)
    #    if index is not None:
    #        code_list = code_list[index:]
    #        url_list = url_list[index:]
    #    else:
    #        code_list = None
    #        url_list = None
            
    return 1 if status_code else 0

def _get_activity(market, date=None):
    """ To assign activity to be execute in this run."""
    activity = []

    # To get whole market info
    if not os.path.exists(_get_whole_stock_market_file_record(market)):
        activity.append(_get_whole_market)

    # To get stocks info
    activity.append(_get_stock)
    return activity

def main():

    # More information: http://strftime.org/
    timestamp = datetime.datetime.now()

    ts_day = timestamp.strftime("%A")
    ts_date = timestamp.strftime("%y%m%d")
    ts_time = timestamp.strftime("%H%M%S")
    ts_microsec = timestamp.strftime("%f")
    ts_week = timestamp.strftime("%U")
    
    ts_is_weekend = True if timestamp.weekday() >= 5 else False

    # Project folder initiate
    daily_log_fldr = ppath.daily_log_path("%s_%s_%s") % (ts_week, ts_date, ts_day)
    if ppath.create_path(daily_log_fldr, True):
        print("Failed to create daily log folder.")
        return 1

    # Logger
    logfile_name = "%s_%s_%s.log" % (ts_date, ts_time, ts_microsec)
    logfile_path = os.path.join(daily_log_fldr, logfile_name)
    logger = sys_logger.setup(flog=logfile_path)

    # Initialization
    ms_cls = MarketStatus(timestamp)

    logging.info("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
    logging.info("| Report Summary                            |")
    logging.info("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
    logging.info("| Date:\t%s" % ts_date)
    logging.info("| Time:\t%s" % ts_time)
    logging.info("| Weekend:\t%s(%s)" % (ts_is_weekend, ts_day))
    logging.info("|")
    logging.info("| Any market today:\t{}".format("YES" if ms_cls.is_market_open_today else "NO"))
    market_close_or_open_reason = "| Market status:\t%s" % ms_cls.market_open_status if ms_cls.is_market_open_today else "| Reason:\t\t%s" % ms_cls.reason_on_market_closed
    logging.info(market_close_or_open_reason)
    logging.info("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")

    # Run activity
    activities = _get_activity(ms_cls)
    for index, activity in enumerate(activities):
        logging.info("")
        logging.info("---------------------------------------------")
        logging.info("| Running job #%i out of %i:- %s" % (index+1, len(activities), activity.__name__))
        try:
            if activity(ms_cls):
                raise Exception("Activity run failure.")
        except Exception:
            logging.error(traceback.format_exc())
            return 1
        finally:
            logging.info("---------------------------------------------")
    else:
        logging.info("")
        logging.info("Completed - no more activity to be run.")

    return 0

if __name__ == "__main__":
    sys.exit(main())
