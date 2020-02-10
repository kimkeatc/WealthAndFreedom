import Utility
import pandas
import os

src_basefolder = r'C:\Users\kimke\OneDrive\Documents\investment and trading\stocks and equity\sandbox\WealthAndFreedom\logs\2020-02-10\daily.xlsx'
dst_basefolder = r'C:\Users\kimke\OneDrive\Documents\investment and trading\stocks and equity\sandbox\WealthAndFreedom\data'

with open(r'C:\Users\kimke\OneDrive\Documents\investment and trading\stocks and equity\sandbox\WealthAndFreedom\module\monitor.txt', 'r') as f:
    content = f.readlines()

df = pandas.read_excel(src_basefolder, converters={'id': str})

homework_df = pandas.DataFrame()

for line in content:
    line = line.replace('\n', '')
    date, stockname = line.split(',')
    series = df[df['name'] == stockname]
    filename = series['id'].values[0] + '.xlsx'
    filepath = os.path.join(dst_basefolder, filename)
    _df = pandas.read_excel(filepath, converters={'id': str})
    if _df['name'][0] == stockname:
        print('Reading %s...' % stockname)
    else:
        print('ERROR !!!!!!!!')
        break
    _df = _df[_df['date'] >= date]
    homework_df = pandas.concat([homework_df, _df])
    print(homework_df)
homework_df.T.to_excel(r'C:\Users\kimke\OneDrive\Documents\investment and trading\stocks and equity\sandbox\WealthAndFreedom\module\monitor.xlsx', index=False)
print('done')
    
