# -*- coding: utf-8 -*-

from os.path import abspath, dirname, exists, join
import sys

_MODULE_FOLDER = abspath(join(dirname(__file__), '..'))
if _MODULE_FOLDER not in sys.path:
    sys.path.append(_MODULE_FOLDER)

import utility
utility.MyProject().system_path_initialize()

import pandas

pandas.set_option('display.max_rows', 1000)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)
pandas.set_option('float_format', '{:.3f}'.format)
pandas.set_option('expand_frame_repr', False)


def getDirection(_open, _close):
    if float(_open) == float(_close):
        return 'no change'
    elif float(_open) > float(_close):
        return 'decrease'
    elif float(_open) < float(_close):
        return 'increase'


def getDirectionScore(direction, score):
    if direction == 'increase':
        return score
    else:
        return 0

def get30sen(_open, _close, score):
    if float(_open) >= 0.3:
        return score
    else:
        return 0
        
    
def process(basepath):
    print('Processing %s' % basepath)
    src_filepath = join(basepath, 'daily.xlsx')
    dst_filepath = join(basepath, 'xt.xlsx')
    klse_filepath = join(basepath, 'klse_screener.xlsx')

    dfKlse = pandas.read_excel(klse_filepath, converters={'Code': str})
    dfKlse = dfKlse[['Code', 'Sector', 'Market', 'Charting URL']]
    #dfKlse.rename(columns={'Code': 'id'}, inplace=True)
    #print(dfKlse)

    df = pandas.read_excel(src_filepath, converters={'id': str})
    df['pillar'] = ((df['close'] - df['open']) / df['open']) *100
    df['body'] = ((df['close'] - df['open'])/(df['high'] - df['low'])) * 100
    df['upper_shadow'] = ((df['high'] - df['close'])/(df['close'] - df['open'])) * 100

    df['direction'] = df.apply(lambda s: getDirection(s['open'],s['close']),axis=1)
    df['pillar_score'] = df['pillar'].apply(lambda p: 1 if p >= 6 and p <= 15 else 0.5 if p >= 5 and p <= 15 else 0)
    df['body_score'] = df['body'].apply(lambda p: 1 if p >= 70 else 0.5 if p >= 60 else 0)
    df['upper_shadow_score'] = df['upper_shadow'].apply(lambda p: 1 if p <= 30 and p >= 0 else 0)
    df['score'] = df['pillar_score'] + df['body_score'] + df['upper_shadow_score']
    df['score'] = df.apply(lambda s: getDirectionScore(s['direction'],s['score']),axis=1)
    df['score'] = df.apply(lambda s: get30sen(s['open'],s['close'], s['score']),axis=1)
    
    df.sort_values(by='score', inplace=True, ascending=False)
    df = df.merge(dfKlse, left_on='id', right_on='Code')
    df.to_excel(dst_filepath, index=False)
        

def main():
    logsfolder = utility.MyProject().logsFolder
    for folder in logsfolder.listdir()[-1:]:
        basepath = join(logsfolder.path, folder)
        process(basepath)
        

if __name__ == '__main__':
    main()
