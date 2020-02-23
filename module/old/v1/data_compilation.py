import json
import os
import pandas

basefolder = r'C:\Users\kimke\OneDrive\Documents\investment and trading\stocks and equity\WealthAndFreedom\logs\2020-02-06'

src_folder = os.path.join(basefolder, 'stocks_profile')

output_file = os.path.join(basefolder, 'compilation.csv')

output_file1 = os.path.join(basefolder, 'compilation1.csv')
output_file2 = os.path.join(basefolder, 'compilation2.csv')

df = pandas.DataFrame()
record = 0

for index, filename in enumerate(os.listdir(src_folder)):
    print(index, filename)
    filepath = os.path.join(src_folder, filename)
    name = filename.split('.')[0]
    with open(filepath, 'r') as f:
        content = json.loads(f.read())
    historical_data = content['historical_data']
    
    record_count = historical_data['record_count']
    record = record + record_count
    print(record, record_count)
    
    data = historical_data['data']
    _df = pandas.DataFrame(data)
    _df['id'] = '\'' + _df['id']
    df = pandas.concat([df, _df])
df.to_csv(output_file, index=False)
        
'''
>>> df[0: 500000].to_csv(output_file1, index=False)
>>> df[500000: 1077407].to_csv(output_file2, index=False)
>>> df[0: 466539].to_csv(output_file1, index=False)
>>> df[466539: 1077407].to_csv(output_file2, index=False)
>>> df[0: 466537].to_csv(output_file1, index=False)
>>> df[466537: 1077407].to_csv(output_file2, index=False)
'''
