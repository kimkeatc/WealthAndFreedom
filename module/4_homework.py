from os.path import abspath, dirname, join
import utility
import pandas

src_basefolderpath = join(abspath(join(dirname(__file__), '..')), 'logs', '2020-03-26', 'daily.xlsx')
dst_basefolderpath = join(abspath(join(dirname(__file__), '..')), 'data')

with open(join(dirname(__file__), 'monitor.txt'), 'r') as f:
    content = f.readlines()

df = pandas.read_excel(src_basefolderpath, converters={'id': str})

homework_df = pandas.DataFrame()

for line in content:
    line = line.replace('\n', '')
    date, stockname = line.split(',')
    series = df[df['name'] == stockname]
    filename = series['id'].values[0] + '.xlsx'
    filepath = join(dst_basefolderpath, filename)
    _df = pandas.read_excel(filepath, converters={'id': str})
    if _df['name'][0] == stockname:
        print('Reading %s...' % stockname)
    else:
        print('ERROR !!!!!!!!')
        break
    _df = _df[_df['date'] >= date]
    _df['vol'] = _df['vol'] / 100
    _df['vol'] = _df['vol'].astype(int)
    _df.drop(columns=['timestamp'])
    _df.reset_index(drop=True, inplace=True)
    homework_df = pandas.concat([homework_df, _df])
    print(homework_df)

homework_df.T.to_excel(join(dirname(__file__), 'monitor.xlsx'), index=False)
print('done')
