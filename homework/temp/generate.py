from os.path import join
import pandas

basepath = r'C:\Users\kimke\OneDrive\Documents\investment and trading\stocks and equity\WealthAndFreedom\resources\profile'
dest = r'C:\Users\kimke\Desktop\temp\temp'
df = pandas.read_excel('tracker.xlsx', converters={'Stock Code': str})

content = ''
for index, row in df.iterrows():
    foldername = row['Stock Name'] + '-' + row['Stock Code']
    folderpath = join(basepath, foldername)
    filepath = join(folderpath, 'historical.xlsx')
    _df = pandas.read_excel(filepath, converters={'id': str})
    _df['vol'] = _df['vol'].astype(str)
    _df = _df[_df['Date'] >= row['Date']]
    _df = _df.drop(['date', 'id', 'name'], axis=1)
    _df = _df.set_index(['Date'])
    _df = _df.T
    content = content + '<br><h2><a href=\'%s\'>%s</a></h2><hr>' % ('https://www.klsescreener.com/v2/charting/chart/%s' % row['Stock Code'], foldername )+ _df.to_html()

    _df.to_csv(join(dest, foldername + '.csv'), index=False)

with open('homework.html', 'w') as f:
    f.write(content)

