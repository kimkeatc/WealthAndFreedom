filepath = r'C:\Users\kimke\OneDrive\Documents\investment and trading\stocks and equity\sandbox\WealthAndFreedom\module\bursa\securities_equities\docs\2020-03-20.pdf'

import tabula
df = tabula.read_pdf(filepath, pages=3,multiple_tables=True)#, output_format="json")
print(df)
