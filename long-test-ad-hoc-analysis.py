import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

tdf = pd.read_json("transaction-data-adhoc-analysis.json") 
tdf = tdf.sort_values(by = "transaction_date", ascending = True)

'''To Clean and Reorganize the Data File'''

tdf_fix = tdf.copy()
tdf_fix_1 = tdf_fix["transaction_items"].str.split(";")
tdf_fix = tdf_fix.assign(transaction_items=tdf_fix_1)
tdf_fix = tdf_fix[tdf_fix["transaction_items"].apply(len)==1]
tdf_fix['transaction_items'] = [','.join(map(str, l)) for l in tdf_fix['transaction_items']]
tdf_fix["item_quantity"] = tdf_fix["transaction_items"].str[-5:]
tdf_fix["item_quantity"] = tdf_fix["item_quantity"].str.strip(',)(x')
tdf_fix["item_quantity"] = tdf_fix["item_quantity"].astype(int)
tdf_fix["transaction_items"] = tdf_fix["transaction_items"].str[:-5]
tdf_fix = tdf_fix.explode("transaction_items").reset_index(drop=True)

tdf_fix

'''Item Index for the Table Below'''
item_list = tdf_fix[["transaction_items", "item_quantity", "transaction_value"]]
item_list = item_list.drop_duplicates(subset = "transaction_items", keep = "first")
item_index = list(item_list["transaction_items"].values)
item_index_1 = set(item_list["transaction_items"])
item_list = item_list['transaction_value'] / item_list["item_quantity"]
item_list.index = item_index
item_list = item_list.sort_values()

'''Table below is for adding a column for "Month" in order to make it easier to create charts and graphs'''
tdf_new = tdf.assign(transaction_items=tdf.transaction_items.str.split(";")).explode('transaction_items').reset_index(drop=True)
tdf_new["item_quantity"] = tdf_new["transaction_items"].str[-5:]
tdf_new["item_quantity"] = tdf_new["item_quantity"].str.strip(',)(x')
tdf_new["item_quantity"] = tdf_new["item_quantity"].astype(int)
tdf_new["transaction_items"] = tdf_new["transaction_items"].str[:-5]
tdf_new["Total Sales"] = tdf_new["item_quantity"] * tdf_new["transaction_items"].apply(lambda x: item_list.loc[x])
tdf_new["Month"] = tdf_new["transaction_date"].str[6:7]

tdf_new

'''First Chart: Total Quantity per Items Sold in a Month'''
tdf_new_pivot = tdf_new["item_quantity"].groupby([tdf_2.transaction_items, tdf_2.Month]).agg(sum)

ax = tdf_new_pivot.unstack(level=0).plot(kind='bar')

'''Second Chart: Total Value per Items Sold in a Month'''
tdf_new_pivot_2 = tdf_new["Total Sales"].groupby([tdf_2.transaction_items, tdf_2.Month]).agg(sum)

ax = tdf_new_pivot_2.unstack(level=0).plot(kind='bar')

tdf_customer = tdf_new[['name']].groupby([tdf_new.Month]).nunique()
tdf_customer = tdf_new[['name']].groupby([tdf_new.Month]).nunique()
tdf_customer_1 = tdf_new[['item_quantity']].groupby([tdf_new.name, tdf_new.Month]).agg(sum)

customer_index = pd.MultiIndex.from_product(tdf_customer_1.index.levels)
customer_tdf = tdf_customer_1.reindex(customer_index)
customer_tdf = customer_tdf.fillna(0).astype(int)
Engaged = tdf_new[['name']].groupby([tdf_new.Month]).nunique()
customer_tdf['Exists'] = customer_tdf['item_quantity'].apply(lambda x: True if x >0 else False)
customer_tdf = customer_tdf.unstack(['name'])
customer_tdf = customer_tdf['Exists']
customer_tdf.index = customer_tdf.index.map(int)
repeaters = customer_tdf.apply(lambda x: [0 if i==1 else (1 if x[i-1] and x[i] else 0)for i in x.index]).transpose().sum()
inactives = customer_tdf.apply(lambda x: [0 if i==1 else ((1 if x[i]==0 else 0) if any(x[:i]) else 0) for i in x.index]).transpose().sum()
engaged = customer_tdf.apply(lambda x: [1 if all(x[:i]) else 0 for i in x.index]).transpose().sum()

data = {"Engaged":engaged, "Repeaters":repeaters, "Inactive":inactives}
cdf = pd.DataFrame(data)

cdf

tdf_new_2 = tdf_new[['Total Sales','item_quantity']].groupby([tdf_new.Month]).agg(sum).reset_index()

tdf_new_2

'''Third Chart: Total Item Quantities Sold per Month'''
y_pos = np.arange(len(tdf_new_2["item_quantity"]))

plt.bar(y_pos, tdf_new_2['item_quantity'], align = 'center', alpha = 0.5)
plt.xticks(y_pos, tdf_new_2['Month'])
plt.ylabel('Item Quantity')
plt.title('Item Quantity by Month')
plt.rcParams["figure.figsize"] = (100,50)
plt.rcParams.update({'font.size': 100})
plt.show()

'''Fourth Chart: Total Value of Items Sold per Month'''
y_pos = np.arange(len(tdf_new_2['Total Sales']))

plt.bar(y_pos, tdf_new_2['Total Sales'], align = 'center', alpha = 0.5)
plt.xticks(y_pos, tdf_new_2['Month'])
plt.ylabel('Total Sales')
plt.title('Total Sales by Month')
plt.rcParams["figure.figsize"] = (100,50)
plt.rcParams.update({'font.size': 100})
plt.show()

tdf_new_3 = tdf_new[['Total Sales','item_quantity']].groupby([tdf_new.transaction_items]).agg(sum)
tdf_new_3 = tdf_new_3.reset_index()

tdf_new_3

'''Fifth Chart: Quantity of Item Sold'''
y_pos = np.arange(len(tdf_new_3['item_quantity']))

plt.bar(y_pos, tdf_new_3['item_quantity'], align = 'center', alpha = 0.5)
plt.xticks(y_pos, tdf_new_3['transaction_items'])
plt.ylabel('Item Quantities')
plt.title('Item Quantities by Object Type')
plt.rcParams["figure.figsize"] = (100,50)
plt.rcParams.update({'font.size': 40})
plt.show()

'''Sixth Chart: Total Sales per Item'''
y_pos = np.arange(len(tdf_new_3['Total Sales']))

plt.bar(y_pos, tdf_new_3['Total Sales'], align = 'center', alpha = 0.5)
plt.xticks(y_pos, tdf_new_3['transaction_items'])
plt.ylabel('Total Sales')
plt.title('Total Sales by Object Type')
plt.rcParams["figure.figsize"] = (100,50)
plt.rcParams.update({'font.size': 40})
plt.show()

'''Seventh Chart: Breakdown of Items in Total Quantities of Items Sold per Month'''

tdf_new.pivot_table(index = ["Month"], columns = 'transaction_items', values = 'Total Sales', aggfunc = 'sum').plot(kind = 'bar', stacked = True)

'''Eighth Chart: Breakdown of Items in Total Value of Quantities of Items Sold per Month'''
tdf_new_5 = tdf_new.pivot_table(index=["Month"], columns='transaction_items', values='item_quantity', aggfunc='sum')
tdf_new_5.plot(kind='bar', stacked=True)
