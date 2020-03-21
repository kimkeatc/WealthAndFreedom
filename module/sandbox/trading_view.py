import pandas
import requests

base_url = 'https://www.tradingview.com/markets/stocks-malaysia/sectorandindustry-industry/'
base_html = requests.get(base_url).text
base_df = pandas.read_html(base_html)[0]


df = base_df[['Unnamed: 0', 'Unnamed: 5']]
df.columns = ['industry', 'sector']
df.reset_index(drop=True, inplace=True)
df.sort_values(by=['sector'], inplace=True)


list_ = []

for i in range(len(df)):
    industry = df.iloc[i, 0]
    sector = df.iloc[i, 1]
    industry = industry.lower()
    industry_ori = industry
    industry = industry.replace('&', '').replace(' ', '-').replace('/', '-').replace(':', '').replace('--', '-')
    industry_url = 'https://www.tradingview.com/markets/stocks-malaysia/sectorandindustry-industry/' + industry
    response = requests.get(industry_url)
    print('+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+')
    print(f'{sector} - {industry} - {response.status_code}')
    industry_df = pandas.read_html(response.text)[0]
    
    companies = industry_df['Unnamed: 0'].to_list()
    for company in companies:
        temp = company.split('  ')
        temp = [sector, industry_ori] + temp
        print(temp)
        list_.append(temp)

df = pandas.DataFrame(list_, columns=['sector', 'industry', 'stockcode', 'company'])
df.to_excel(r'C:\Users\kimke\Desktop\trading_view.xlsx', index=False)
