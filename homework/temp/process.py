from os.path import join
import os
import pandas

src = r'C:\Users\kimke\Desktop\temp\src'

def calculate_direction(s):
    if s.vol == '-':
        return None
    elif s.open == s.close:
        return 'No change'
    elif s.open > s.close:
        return 'Down'
    elif s.open < s.close:
        return 'Up'
    
def calculate_pillar(s):
    return (s.close - s.open)/s.open

def calculate_body(s):
    try:
        return (s.close - s.open)/(s.high - s.low)
    except:
        return None
    

def calculate_upper_shadow(s):
    try:
        return (s.high - s.close)/(s.close - s.open)
    except:
        return None

for filename in os.listdir(src):
    print(filename)
    filepath = join(src, filename)
    df = pandas.read_excel(filepath, converters={'id': str})
    df['direction'] = df.apply(calculate_direction, axis=1)
    df['pillar'] = df.apply(calculate_pillar, axis=1)
    df['body'] = df.apply(calculate_body, axis=1)
    df['upper_shadow'] = df.apply(calculate_upper_shadow, axis=1)
    df.to_excel(filepath, index=False)
