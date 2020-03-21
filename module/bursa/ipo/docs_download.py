from os.path import abspath, join
from pathlib import Path
import datetime
import requests
import pandas

DOCS_FOLDERPATH = abspath(Path(__file__).resolve().parent.joinpath('docs'))
IPO_FILENAME = 'ipo_{year}.xlsx'
BASE_URL = 'https://www.bursamalaysia.com/listing/listing_resources/ipo/ipo_summary?year={year}&per_page=50&page={page_number}'


def docs_download(year, page_number=1):

    print('+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+')
    print(f'Download IPO company list year {year}')
    print('+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+')

    while page_number:

        filename = IPO_FILENAME.format(year=year)
        filepath = join(DOCS_FOLDERPATH, filename)

        url = BASE_URL.format(year=year, page_number=page_number)
        print(f'Page number #{page_number}: {url}')

        try:
            response = requests.get(url)
            response.raise_for_status()
        except Exception as e:
            print('Access failure...')
            break
        
        page_number += 1

        df = pandas.read_html(response.text)
        df = df[0]
        if df.empty:
            print(f'Page empty...')
            break
        df.to_excel(filepath)


def yearly_download():

    date_ = datetime.datetime.now()
    year = date_.strftime('%Y')
    docs_download(year)


if __name__ == '__main__':
    yearly_download()
