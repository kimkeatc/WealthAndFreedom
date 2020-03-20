from os.path import abspath, exists, join
from pathlib import Path
import datetime
import requests

DOCS_FOLDERPATH = abspath(Path(__file__).resolve().parent.joinpath('docs'))
BASE_URL = 'https://www.bursamalaysia.com/misc/missftp/securities/securities_equities_{date}.pdf'


def docs_download(date_):

    print(f'Download securities equities date {date_}')

    url = BASE_URL.format(date=date_)
    filename = f'{date_}.pdf'
    filepath = join(DOCS_FOLDERPATH , filename)

    if exists(filepath):
        print('File exists...')
        return

    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print('Download success...')
    except Exception as e:
        print(f'Download failure - Reason: {e}')


def daily_download():
    date_ = datetime.datetime.now()
    date_fmt = date_.strftime('%Y-%m-%d')
    docs_download(date_fmt)


if __name__ == '__main__':
    daily_download()
