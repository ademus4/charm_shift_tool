import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
from datetime import datetime, timedelta

def login():
  json_key = json.load(open('tool-cred.json'))
  scope = ['https://spreadsheets.google.com/feeds']

  credentials = SignedJwtAssertionCredentials(json_key['client_email'], bytes(json_key['private_key'], 'utf-8'), scope)
  gc = gspread.authorize(credentials)
  return gc

def get_date(shift_start):
  now = datetime.now()
  hour = int(str(now.hour) + str(now.minute).zfill(2))
  if hour < shift_start:
    # Shifter from yesterday is still working
    now -= timedelta(hours=24)

  date = str(now.day).zfill(2)+ '/' + str(now.month).zfill(2) + '/' + str(now.year)
  tomorrow = str(now.day+1).zfill(2)+ '/' + str(now.month).zfill(2) + '/' + str(now.year)
  return date, tomorrow

def get_shifter():
 date, tomorrow = get_date(1400)
 gc = login()
 wks = gc.open("CHARM shift schedule 2015")
 sheets = wks.worksheets()
 worksheet = wks.get_worksheet(0)
 user_names = worksheet.row_values(1)
 sheet_dates = worksheet.col_values(2)
 row = 0
 for d in sheet_dates:
   row += 1
   if d == date:
     break
 current_row = worksheet.row_values(row)
 col = len(current_row)
 shifter = worksheet.cell(1,col).value
 return shifter

def get_all_shifters():
  gc = login()
  wks = gc.open("CHARM shift schedule 2015")
  sheets = wks.worksheets()
  worksheet = wks.get_worksheet(0)
  user_names = worksheet.row_values(1)
  return user_names[2:] # Remove 2 because the first to columns are day of the week and date respectively

if __name__ == '__main__':
  print(get_shifter())
