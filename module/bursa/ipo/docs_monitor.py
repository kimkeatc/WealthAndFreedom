from os.path import abspath, join
from pathlib import Path
import datetime
import pandas
import os

DOCS_FOLDERPATH = abspath(Path(__file__).resolve().parent.joinpath('docs'))
IPO_SUMMARY_FILENAME = 'ipo_summary.xlsx'
IPO_SUMMARY_FILEPATH = abspath(join(DOCS_FOLDERPATH, '..', IPO_SUMMARY_FILENAME))


def monitoring():

    df = pandas.DataFrame()
    header = None
    
    for index, filename in enumerate(os.listdir(DOCS_FOLDERPATH)):

        print('Reading file #%i named: %s' % (index+1, filename))
        filepath = join(DOCS_FOLDERPATH, filename)

        _df = pandas.read_excel(filepath, index=False, header=None)

        if header is None:
            header = _df.head(2)
            header.drop([0], axis=1, inplace=True)
            header.reset_index(inplace=True, drop=True)

        _df = _df.loc[3:]
        _df.drop([0], axis=1, inplace=True)
        _df.reset_index(inplace=True, drop=True)

        df = pandas.concat([_df, df])
        df.reset_index(inplace=True, drop=True)

    df = pandas.concat([header, df])
    df.to_excel(IPO_SUMMARY_FILEPATH, index=False, header=False)

    
if __name__ == '__main__':
    monitoring()
