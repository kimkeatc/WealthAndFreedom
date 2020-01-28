from os.path import join
import pandas

pandas.set_option('display.max_rows', 1000)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)
pandas.set_option('float_format', '{:.3f}'.format)
pandas.set_option('expand_frame_repr', False)

basepath = r'C:\Users\kimke\OneDrive\Documents\investment and trading\stocks and equity\WealthAndFreedom\resources\profile'
dest = r'C:\Users\kimke\OneDrive\Documents\investment and trading\stocks and equity\sandbox\WealthAndFreedom\homework\temp'
df = pandas.read_excel('tracker.xlsx', converters={'Stock Code': str})

x = pandas.DataFrame()
content = ''
for index, row in df.iterrows():
    foldername = row['Stock Name'] + '-' + row['Stock Code']
    folderpath = join(basepath, foldername)
    filepath = join(folderpath, 'historical.xlsx')
    _df = pandas.read_excel(filepath, converters={'id': str})
    _df['vol'] = _df['vol'].astype(str)
    _df = _df[_df['Date'] >= row['Date']]
    _df = _df.drop(['date', 'id'], axis=1)
    _df = _df.set_index(['Date'])
    _df = _df.T
    x = pandas.concat([x, _df], sort=False)
    content = content + '<br><h2><a href=\'%s\'>%s</a></h2><hr>' % ('https://www.klsescreener.com/v2/charting/chart/%s' % row['Stock Code'], foldername )+ _df.to_html()

    _df.to_csv(join(dest, foldername + '.csv'), index=False)


x.to_excel('homework.xlsx', index=False)
with open('homework.html', 'w') as f:
    f.write(content)

