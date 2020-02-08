import pyodbc

for driver in pyodbc.drivers():
    #print(driver)
    pass

SERVER_NAME = '(LocalDb)\stocks'
DATABASE = 'FBMKLCI'

connection_msg = 'DRIVER={ODBC Driver 17 for SQL Server}; SERVER=%s; DATABASE=%s; Trusted_Connection=yes;' % (SERVER_NAME, DATABASE)
conn = pyodbc.connect(connection_msg)
cursor = conn.cursor()
cursor.execute('''SELECT * FROM main''')
for row in cursor:
    print(row)
#conn.commit()

import pandas
df = pandas.read_sql_query('''SELECT * FROM main''', conn)
df['stockname'] = '1234'
print(df)
df.to_sql('main', conn, if_exists="replace")
cursor.close()
conn.close()
