import gspread
import matches
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Sector Taxonomy")

# Select the references worksheet of the CRANE sheets
worksheet = sheet.worksheet("References")

# find cell, which columns to search in?
found = worksheet.findall("Extreme Efficiency in IT/Data Centers")
matches.returnMatches(worksheet, found)



