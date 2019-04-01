import gspread
import matches
import argparse

from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

#parse for the search entry
parser = argparse.ArgumentParser(description='Input a search entry')
parser.add_argument('searchEntry', nargs='?', help='search for name of value')
args = parser.parse_args()

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Sector Taxonomy")

# Select the references worksheet of the CRANE sheets
worksheet = sheet.worksheet("References")

# find cell, which columns to search in?
#searchEntry = args[0]
searchEntry = "Extreme Efficiency in IT/Data Centers"
matches.returnMatches(worksheet, searchEntry)



