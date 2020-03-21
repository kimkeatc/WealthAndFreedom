import json
import os
import pandas

basepath = r'C:\Users\kimke\OneDrive\Documents\investment and trading\stocks and equity\WealthAndFreedom\resources\src'

destpath = r'C:\Users\kimke\OneDrive\Documents\investment and trading\stocks and equity\WealthAndFreedom\resources\20200205\new'

for index, filename in enumerate(os.listdir(basepath)):
    print(index + 1)
    filepath = os.path.join(basepath, filename)
    with open(filepath) as f:
        content = json.load(f)
    historical_data = content['historical_data']
    record_count = historical_data['record_count']
    data = historical_data['data']
    df = pandas.DataFrame(data)

    dest_filepath = os.path.join(destpath, filename.replace('.json', '.xlsx'))
    df.to_excel(dest_filepath, index=False)
