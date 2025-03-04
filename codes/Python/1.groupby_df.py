

import pandas as pd

data = {'Product': ['A', 'B', 'A', 'C'],'Price': [10, 20, 15, 30],'Quantity': [5, 3, 2, 4] }

df = pd.DataFrame(data)
#print(df)

df['Total_price'] = df['Price']*df['Quantity']

df = df.groupby('Product')['Total_price'].sum()
print(df)