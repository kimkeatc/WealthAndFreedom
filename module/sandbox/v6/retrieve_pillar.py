import os
import pandas
import sys

file_name = "market-2019-10-11.csv"
folder_path = r"D:\duck\investment\fiavest\history"
file_path = os.path.join(folder_path, file_name)

print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
print("Begin to load stock table: %s" % file_path)
print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
df = pandas.read_csv(file_path)
df["Code"] = df["Code"].str[1:]
df["Volume"] = df["Volume"].str.replace("-", "0", regex=True)
df["Volume"] = df["Volume"].str.replace(",", "", regex=True).astype(int)
print("\nLoaded successfully... number of counters: %s" % df.shape[0])

print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
print("Looking for counter has 1,000,000 of volume...")
df = df[df["Volume"] >= 2000000]
df["Volume"] = df["Volume"] / 100
print("Filtered successfully... remaining counter: %s" % df.shape[0])

print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
print("Looking for bullish counter...")
df = df[df["Change status"] == "increasing"]
print("Filtered successfully... remaining counter: %s" % df.shape[0])

print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
print("Looking for counter that has close price range from 0.30 to 5.00 ...")
df = df[df["Close"] >= 0.3]
df = df[df["Close"] <= 5.0]
print("Filtered successfully... remaining counter: %s" % df.shape[0])

print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
print("Looking for counter that has equal or more than 4 tick size...")
df = df[df["Tick Size"] >= 8]
print("Filtered successfully... remaining counter: %s" % df.shape[0])

print("")
print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
df.rename(columns={'Name (Short)':'Name'}, inplace=True)
df = df[['Code', 'Name', 'Open', 'High', 'Low', 'Close', 'Volume', 'URL']]
df["Support"] = round((df["Close"] + df["Open"]) / 2.0, 3)
df["Risk"] = df["Support"] * 1.05
df["Risk"] = df["Risk"].map('{:,.3f}'.format)

df = df[['Code', 'Name', 'Open', 'High', 'Low', 'Close', 'Support', 'Volume', 'Risk', 'URL']]
print(df.to_string(index=False))

export_file_name = "pillar-%s" % file_name.replace(".csv", ".xlsx")
export_file_path = os.path.join(folder_path, export_file_name)

print("Export result into file: %s" % export_file_path)
df['Code'] = '\'' + df['Code'].astype(str)
if not os.path.exists(export_file_path):
    df.to_excel(export_file_path, index=False)
    os.system("start %s" % export_file_path)
