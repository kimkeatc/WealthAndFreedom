import pandas
import os

src = r'C:\Users\kimke\Desktop\draft\data'
dst = r'C:\Users\kimke\OneDrive\Documents\investment and trading\stocks and equity\sandbox\WealthAndFreedom\data'

for index, filename in enumerate(os.listdir(src)):

    print('Processing file #%i: %s' % (index+1, filename))
    
    src_filepath = os.path.join(src, filename)
    dst_filepath = os.path.join(dst, filename)

    src_df = pandas.read_excel(src_filepath)
    dst_df = pandas.read_excel(dst_filepath, converters={'id': str})

    stockcode = dst_df['id'][0]
    stockname = dst_df['name'][0]

    src_df.insert(loc=1, column='date', value=pandas.to_datetime(src_df['timestamp'], unit='s').dt.strftime('%Y-%m-%d'))
    src_df.insert(loc=2, column='id', value=stockcode)
    src_df.insert(loc=3, column='name', value=stockname)

    df = pandas.concat([src_df, dst_df])
    df.drop_duplicates(subset=['timestamp'], keep='last', inplace=True)
    df.sort_values(by=['timestamp'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    df.to_excel(dst_filepath, index=False)
