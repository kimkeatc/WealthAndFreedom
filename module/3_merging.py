from os.path import abspath, dirname, exists, join
import utility
import pandas
import os

src_basefolder = join(abspath(join(dirname(__file__), '..')), 'logs',
                      '2020-04-29', 'temp')
dst_basefolder = join(abspath(join(dirname(__file__), '..')), 'data')

for filename in os.listdir(src_basefolder):
    print(filename)
    src_filepath = join(src_basefolder, filename)
    dst_filepath = join(dst_basefolder, filename)

    if exists(dst_filepath):
        src_df = pandas.read_excel(src_filepath, converters={'id': str})
        dst_df = pandas.read_excel(dst_filepath, converters={'id': str})

        #df = pandas.merge(src_df, dst_df, on=['timestamp', 'date', 'id', 'name', 'open', 'high', 'low', 'close', 'vol'], how='right')
        df = pandas.concat([src_df, dst_df])
        df.drop_duplicates(subset=['timestamp'], keep='last', inplace=True)
        df.sort_values(by=['timestamp'], inplace=True)
        df.reset_index(drop=True, inplace=True)
    else:
        df = pandas.read_excel(src_filepath)
    df.to_excel(dst_filepath, index=False)
