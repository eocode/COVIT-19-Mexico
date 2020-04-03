from oauth2client.service_account import ServiceAccountCredentials
import gspread

def get_googlesheet_worksheet(json_keyfile_name, sheet_name, worksheet_name):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_name, scope)
    
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).worksheet(worksheet_name)
    return sheet