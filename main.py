import gspread
import pandas as pd
import time
from automatized.credentials import get_googlesheet_worksheet
from automatized.sheets import get_googlesheet_df
from automatized.sheets import update_googlesheet_row_range
from automatized.sheets import get_column_sheet_indexes
from automatized.process import flow

# Get a Google Sheet
sheet = get_googlesheet_worksheet(
    'api.json', 'Automated Dashboard Covit-19', 'GlobalReport')

# ProcessData
result = flow()

columns = []
for c in result.columns:
    columns.append(c)

sheet.insert_row(values=columns,index=1)

i = 2
for index, row in result.iterrows():
    my_list =[] 
    for c in result.columns:
        my_list.append(str(row[c]))
    sheet.insert_row(values=my_list,index=i)
    i += 1
    if i % 35 == 0:
        time.sleep(100)

# print(result)
# update_googlesheet_row_range(sheet,df)
