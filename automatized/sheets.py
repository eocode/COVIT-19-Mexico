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

def get_column_sheet_index(df, column_name):
    return list(df.columns).index(column_name) + 1

def get_column_sheet_indexes(df, column_names):
    result = []
    for column_name in column_names:
        result.append(get_column_sheet_index(df, column_name))
    return result

def update_googlesheet_row_range(worksheet, df, index, sequential_column_names, values):
    # do we have as many values as columns?
    assert (len(sequential_column_names) == len(values))
    
    column_name_index = get_column_sheet_indexes(df, sequential_column_names)
    
    # do we have as many matched columns as their are values
    assert (len(column_name_index) == len(values))
    
    # we need to have a sequential range of columns to update
    min_column_name_index_value = column_name_index[0]
    max_column_name_index_value = column_name_index[len(column_name_index) - 1]
    
    # add +1 to max_column_name_index_value for range generation
    test_range = list(range(min_column_name_index_value, max_column_name_index_value + 1))
    
    # would rather fail assertion than a faulty update
    assert(test_range == column_name_index)
    
    print(index, min_column_name_index_value, index, max_column_name_index_value)
    cell_list = worksheet.range(index, min_column_name_index_value, index, max_column_name_index_value)
    
    for i, cell in enumerate(cell_list):
        print(i, cell.value)
        cell.value = values[i]
    
    # Update in batch
    worksheet.update_cells(cell_list)
    
    return