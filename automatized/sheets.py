import gspread
import pandas as pd

def get_googlesheet_df(worksheet, header_row = None):
    all_values = worksheet.get_all_values()
    
    df = pd.DataFrame.from_records(all_values)
    
    df.index = range(1, len(df) + 1)
    
    if header_row is not None:
        columns = all_values[header_row]
        df.columns = columns
        df = df.drop(df.index[0:header_row + 1])
    
    return df