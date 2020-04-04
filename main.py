import gspread
import pandas as pd
import time
from automatized.credentials import get_googlesheet_worksheet
from automatized.sheets import get_googlesheet_df
from automatized.process import world_data_analyst

# Get a Google Sheet
sheet = get_googlesheet_worksheet(
    'api.json', 'Automated Dashboard Covit-19', 'GlobalReport')

# ProcessData
world_data_analyst(sheet)
