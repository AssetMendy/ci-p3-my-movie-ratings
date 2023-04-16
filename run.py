import gspread
from oauth2client.service_account import ServiceAccountCredentials
from tabulate import tabulate

# Define the scope of the API access
SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# Define the credentials and authorize the API access
CREDS  = ServiceAccountCredentials.from_json_keyfile_name('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT  = gspread.authorize(SCOPED_CREDS)

# Open the Google Sheet
SHEET = GSPREAD_CLIENT.open('my_movie_ratings').worksheet('movies')