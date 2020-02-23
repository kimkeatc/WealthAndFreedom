__author__ = "Chin, Kim Keat"
__email__ = "kim.keat.chin@outlook.com"
__version__ = "1.0.0"
__status__ = "development"

__file__ = "fiavest"
__description__ = """
Fiavest system - swiss trading plan.
"""

from os.path import exists, join
import logging
import os
import sys

from script import Project
Project.sys_path_initialize()

from script.Bursa import bursa
from script.PostProcessStockFile import PostProcess, FiavestEOD


def main(date="20191202"):

    temp_folder = "temp"

    bursaAPI = bursa.API()
    project = Project.Project()

    data_folder_path = project.data.path
    temp_data_folder_path = join(data_folder_path, temp_folder)
    date_folder_path = join(temp_data_folder_path, date)

    wholemarket_file_path = join(date_folder_path, "WholeMarkets.csv")
    indices_file_path = join(date_folder_path, "Indices.csv")
    pn17_file_path = join(date_folder_path, "pn17.csv")
    gn3_file_path = join(date_folder_path, "gn3.csv")
    stocks_file_path = join(date_folder_path, "Stocks.csv")
    post_processed_stocks_file_path = join(date_folder_path, "PostProcessedStocks.csv")
    eod_file_path = join(date_folder_path, "EOD.csv")

    if not exists(date_folder_path):
        logging.info("Create date folder.")
        os.makedirs(date_folder_path)

    # Step 1: To get whole market
    if not exists(wholemarket_file_path):
        print("[Step 1] To get whole market information.")
        returncode = bursaAPI.getAllMarket(wholemarket_file_path)
        if returncode:
            print("Step 1 failure.")
            return 1

    # Step 2: To get equities indices
    if not exists(indices_file_path):
        print("[Step 2] To get indices information.")
        returncode = bursaAPI.getIndices(indices_file_path)
        if returncode:
            print("Step 2 failure.")
            return 1

    # Step 3: To get pn17 and gn3 list
    if not exists(pn17_file_path) or not exists(gn3_file_path):
        print("[Step 3] To get pn17 and gn3 list")
        returncode = bursaAPI.getPN17GN3List(pn17_file_path, gn3_file_path)
        if returncode:
            print("Step 3 failure.")
            return 1

    # Step 4: To get all stock
    if not exists(stocks_file_path):
        print("[Step 4] To get all stock information.")
        returncode = bursaAPI.getAllStock(date_folder_path, wholemarket_file_path)
        if returncode:
            print("Step 4 failure.")
            return 1

    # Step 5: To combine all stock info into single file
    if not exists(stocks_file_path):
        print("[Step 5] To combine all stocks info into single file.")
        returncode = bursaAPI.combineAllStock(stocks_file_path, date_folder_path, wholemarket_file_path)
        if returncode:
            print("Step 5 failure.")
            return 1
        bursaAPI.combineAllStock_enhance(stocks_file_path, wholemarket_file_path)

    # Step 6: To post process data
    if not exists(post_processed_stocks_file_path):
        print("[Step 6] Data post processing.")
        returncode = PostProcess(stocks_file_path, post_processed_stocks_file_path)
        if returncode:
            print("Step 6 failure.")
            return 1

    # Step 7: Fiavest EOD summary maker
    if not exists(eod_file_path):
        print("[Step 7] Fiavest EOD")
        returncode = FiavestEOD(post_processed_stocks_file_path, eod_file_path)
        if returncode:
            print("Step 7 failure.")
            return 1

    return 0


if __name__ == "__main__":
    print("Executing script %s" % __file__)

    # dates = ['20191018',
    # '20191021', '20191022', '20191023', '20191024', '20191025',
    # '20191029', '20191030', '20191031', '20191101',
    # '20191104', '20191105', '20191106']

    # for date in dates:
    #     returncode = main(date)

    returncode = main()
    sys.exit(returncode)
