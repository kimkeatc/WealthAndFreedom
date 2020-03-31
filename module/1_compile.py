from os.path import abspath, dirname, join
import utility
import pandas
import os

basefolder = join(abspath(join(dirname(__file__), '..')), 'logs',
                  '2020-03-31', 'temp')

df = pandas.DataFrame()
for index, filename in enumerate(os.listdir(basefolder)):
    print(index, filename)
    filepath = join(basefolder, filename)
    _df = pandas.read_excel(filepath, converters={'id': str})
    df = pandas.concat([df, _df], sort=False)

dst_basefolder = utility.MyProject().logsFolder.path
for d in df['date'].unique():
    print(d)
    f = utility._Folder(dst_basefolder, d)
    f.create()

    h = utility._File(f.path, 'daily.xlsx')
    if os.path.exists(h.path):
        continue
    _df = df[df['date'].isin([d])]
    _df.to_excel(h.path, index=False)
