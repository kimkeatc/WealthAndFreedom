import datetime
import pandas

begin = datetime.datetime(2009, 3, 31)
until = datetime.datetime(2020, 12, 31)
# until = datetime.datetime(2009, 4, 5)

timestamp = []

temp = begin
while temp.timestamp() <= until.timestamp():
    timestamp.append(int(temp.timestamp()))
    temp = temp + datetime.timedelta(days=1)

df = pandas.DataFrame(timestamp)
df.to_excel('timestamp.xlsx', index=False)
print('done')
