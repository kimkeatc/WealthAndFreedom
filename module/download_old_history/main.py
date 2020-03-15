from os.path import dirname, join
import pandas
import requests

pandas.set_option('display.max_rows', 500)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)

proxyDict = {'http': 'proxy.png.intel.com:911',
             'https': 'proxy.png.intel.com:911'}

r = requests.get('https://www.klsescreener.com/v2/screener/quote_results', proxies=proxyDict)
df = pandas.read_html(r.text)[0]

data_folderpath = join(dirname(__file__), 'data')

for stockcode in df['Code'].to_list():
    if not stockcode.isdigit():
        print(stockcode)
        continue
    url = f'https://www.klsescreener.com/v2/trading_view/history?symbol={stockcode}&resolution=D&from=1238428800&to=1583494876'
    r = requests.get(url, proxies=proxyDict)
    t = r.json()['t']
    c = r.json()['c']
    o = r.json()['o']
    h = r.json()['h']
    l = r.json()['l']
    v = r.json()['v']
    df = pandas.DataFrame({'timestamp': t,
                           'open': o,
                           'high': h,
                           'low': l,
                           'close': c,
                           'vol': v})
    filepath = join(data_folderpath, str(stockcode) + '.xlsx')
    df.to_excel(filepath, index=False)
