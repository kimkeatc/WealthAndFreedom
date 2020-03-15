import os

base = r'C:\Users\kimke\OneDrive\Documents\investment and trading\stocks and equity\sandbox\WealthAndFreedom\data'
new = r'C:\Users\kimke\Desktop\draft\data'

basefile_list = os.listdir(base)
basefile_list = [f.replace('.xlsx', '') for f in basefile_list]


newfile_list = os.listdir(new)
newfile_list = [f.replace('.xlsx', '') for f in newfile_list]

for newfile in newfile_list:
    if newfile not in basefile_list:
        print(newfile)

for basefile in basefile_list:
    if basefile not in newfile_list:
        print(basefile)

