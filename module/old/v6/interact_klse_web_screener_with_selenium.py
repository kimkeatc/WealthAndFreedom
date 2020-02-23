import datetime
import logging
import os
import pandas
import sys
import traceback
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys_path

class MarketBoard:
    ace_market = "Ace Market"
    bond_and_loan = "Bond & Loan"
    etf = "ETF"
    leap_market = "Leap Market"
    main_market = "Main Market"
    structured_warrants = "Structured Warrants"

    def board_list(self):
        return [self.ace_market, self.bond_and_loan, self.etf,
                self.leap_market, self.main_market, self.structured_warrants]

class WebDriverType:
    chrome = "chrome"
    
class KLSE(MarketBoard, WebDriverType):

    default_webdriver = WebDriverType().chrome

    def __init__(self, driver_type=None):
        super(WebDriverType, self).__init__()
        self.driver_type = driver_type if driver_type else self.default_webdriver
        if self.driver_type == self.chrome:
            self.driver_cls = webdriver.Chrome
            self.driver_path = self.get_webdriver_path_chrome()

    def whole_market_info(self, export_path=None, force_update=False):
        
        temp = []
        _board_list = self.board_list()
        timestamp = str(datetime.datetime.now().date())

        # To load board info
        for index, board in enumerate(_board_list):
            logging.info("Loading markets on board %i out of %i:- '%s'" % (index+1, len(_board_list), board))
            board_df = self.board_info(board)

            # Either board information failed to get retrieve - it will return error immediately.
            if board_df is None:
                raise Exception("Failed to load board '%s'" % board)
            board_df["Board"] = board
            temp.append(board_df)

        # To merge all board into one table
        logging.info("All the board information successfully loaded...begin to merge into single table...")
        merge_df = pandas.concat(temp)
        merge_df['Code'] = '\'' + merge_df['Code'].astype(str)
        merge_df['Date'] = timestamp

        # Rearrange the column based on sequence
        header_sequence = ["Date", "Code", "Name", "Price", "Volume",
                           "Category", "Board", "52week", "EPS", "DPS",
                           "NTA", "PE", "DY", "ROE", "PTBV", "MCap.(M)", "URL"]
        merge_df = merge_df[header_sequence]

        # Export to file
        if export_path:
            if not os.path.exists(export_path) or force_update:
                logging.info("Exporting whole market info to %s" % export_path)
                merge_df.to_csv(export_path, index=False)
            
        return merge_df

    def board_info(self, board):
        _board_selection_field_name = "board"
        _submit_button_field_name = "submit"
        
        try:
            d = self.run_process()
            d.get(self.url_stock_screener_page())
            
            WebDriverWait(d, 3).until(EC.presence_of_element_located((By.NAME, _board_selection_field_name)))
            
            board_selection_field = webdriver.support.select.Select(d.find_element_by_name(_board_selection_field_name))
            board_selection_field.select_by_visible_text(board)
            
            submit_button = d.find_element_by_id(_submit_button_field_name)
            submit_button.click()
            
            WebDriverWait(d, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="result"]/div')))
            page_source = d.page_source
            d.quit()
        except TimeoutException:
            d.quit()
            logging.error("Loading time taken too long.")
            return None
        except Exception:
            d.quit()
            logging.error(traceback.format_exc())
            return None
        return self.post_process_board_page_source_info(page_source)

    def post_process_board_page_source_info(self, page_source):
        tree = html.fromstring(page_source)
        header_list = [h.text.strip() for h in tree.xpath('//*[@id="result"]/div/div/table/thead/tr/th[*]/div/div')]
        header_list = [h for h in header_list if h and h != "Indicators"] + ["URL"]
        stock_list = []
        for tr in tree.xpath('//*[@id="result"]/div/table/tbody/tr'):
            temp = {}
            for index, td in enumerate(tr.iter('td')):
                if 'title' not in td.attrib.keys():
                    continue
                title_attrib = td.attrib["title"]
                if title_attrib.startswith("Price"):
                    title_attrib = "Price"
                if title_attrib == "Market Capital":
                    title_attrib = "MCap.(M)"
                if index == 0:
                    for a in td.iter('a'):
                        temp["URL"] = self.url_stock_screener_page() + a.attrib["href"]
                        if title_attrib:
                            temp["Name"] = title_attrib
                            title_attrib = "Name"
                        else:
                            temp["Name"] = a.text
                if title_attrib and title_attrib != "Name":
                    temp[title_attrib] = td.text
            try:
                stock = [temp[h] for h in header_list]
                stock_list.append(stock)
            except Exception:
                logging.error(traceback.format_exc())
                return None
        return pandas.DataFrame(stock_list, columns=header_list)

    def stock_market_info(self, zipped_stock_list, export_path, total_size):
        record_df = pandas.read_csv(export_path, keep_default_na=False) if os.path.exists(export_path) else pandas.DataFrame()
        if not record_df.empty:
            record_df["Code"] = record_df["Code"].str[1:]

        stock_info = []
        failed_index = None
        timestamp = str(datetime.datetime.now().date())
        try:
            d = self.run_process()
            for index, (code, url) in enumerate(zipped_stock_list):
                logging.info("")
                logging.info("Searching stock %i out of %i: '%s'" % (index+1, total_size, code))
                logging.info("URL: %s" % url)
                info = self.get_stock_info(d, url)
                if info is None:
                    raise Exception("Failed to retrieve stock '%s' info." % code)
                stock_info.append(info)
        except Exception:
            failed_index = index
            logging.error(traceback.format_exc())
        finally:
            d.quit()

        new_df = pandas.DataFrame(stock_info)
        if not new_df.empty:
            merge_df = pandas.concat([record_df, new_df], sort=True)
            logging.info("Exporting whole market info to %s" % export_path)
            merge_df['Code'] = '\'' + merge_df['Code'].astype(str)
            merge_df['Date'] = timestamp

            # Rearrange the column based on sequence
            header_sequence = ["Date", "Code", "Name (Short)", "Name (Full)", "Perfect Pillar",
                               "Open", "High", "Low", "Close", "Volume",
                               "Tick Size", "Change value", "Change value (%)", "Change status",
                               "Average Volume", "52w", "DPS", "DY", "EPS", "Market Cap", "P/E",
                               "PSR", "PTBV", "Price Bid/Ask", "ROE", "RPS", "RSI(14)",
                               "Relative Volume", "Stochastic(14)", "Volume (B/S)", "URL"]
            merge_df = merge_df[header_sequence]
            merge_df.to_csv(export_path, index=False)
        return failed_index

    def get_stock_info(self, webdriver, url):
        try:
            webdriver.get(url)
            WebDriverWait(webdriver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="page"]/div[2]/div[1]')))
            temp = self.post_process_stock_page_source_info(webdriver.page_source)
            temp["URL"] = url
            return temp
        except TimeoutException:
            logging.error("Loading time taken too long.")
            return None
        except Exception:
            logging.error(traceback.format_exc())
            return None

    def post_process_stock_page_source_info(self, page_source):
        stock_info = {}
        tree = html.fromstring(page_source)

        # Row data
        short_name_and_code = tree.xpath('//*[@id="page"]/div[2]/div[1]/div[1]/div[1]/h1')[0].text
        full_name = tree.xpath('//*[@id="page"]/div[2]/div[1]/div[1]/div[1]/span')[0].text
        close_price = tree.xpath('//*[@id="price"]')[0].text
        stock_price_status = tree.xpath('//*[@id="price_header"]')[0].attrib["class"]
        price_changes_value_and_percentage = tree.xpath('//*[@id="priceDiff"]')[0].text
        
        short_name = short_name_and_code[0: short_name_and_code.rfind("(")]
        code = short_name_and_code[short_name_and_code.rfind("(") + 1: short_name_and_code.rfind(")")]
        price_changes_value = price_changes_value_and_percentage[0: price_changes_value_and_percentage.rfind("(")]
        price_changes_percentage = price_changes_value_and_percentage[price_changes_value_and_percentage.rfind("(") + 1: price_changes_value_and_percentage.rfind(")")]

        open_price = float(close_price) - float(price_changes_value)

        stock_info["Name (Short)"] = short_name
        stock_info["Name (Full)"] = full_name
        stock_info["Code"] = code
        stock_info["Close"] = close_price
        stock_info["Open"] = open_price
        stock_info["Change value"] = price_changes_value
        stock_info["Change value (%)"] = price_changes_percentage
        stock_info["Change status"] = stock_price_status

        stock_info["Perfect Pillar"] = ""

        per_tick = self.tick_size(open_price)
        try:
            tick_size = int(abs(float(price_changes_value)) / per_tick)
            stock_info["Tick Size"] = tick_size
        except Exception:
            logging.error(traceback.format_exc())
            return None
        
        # Table data
        for div in tree.xpath('//*[@id="page"]/div[2]/div[1]/div[2]/div[1]/div'):
            for index, table in enumerate(div.iter('table')):
                if index in [0, 2]:
                    for tbody in table.iter('tbody'):
                        for tr in tbody.iter('tr'):
                            info_name = None
                            info_value = None
                            for index, td in enumerate(tr.iter('td')):
                                
                                if td.text:
                                    if index == 0:
                                        info_name = td.text.strip()
                                    else:
                                        info_value = td.text.strip()
                            if info_name:
                                stock_info[info_name] = info_value      
        return stock_info

    def tick_size(self, price):
        if price >= 100:
            return 0.1
        elif price >= 10:
            return 0.02
        elif price >= 1:
            return 0.01
        elif price < 1:
            return 0.005
        else:
            return None

    def get_webdriver_path_chrome(self):
        cls = sys_path._ppath()
        return cls.get_path(cls.webdriver_chrome_path)

    def run_process(self):
        return self.driver_cls(self.driver_path)

    def url_home_page(self):
        return "https://www.klsescreener.com/v2/markets"

    def url_stock_screener_page(self):
        return "https://www.klsescreener.com"
