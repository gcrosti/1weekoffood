#IMPORT LIBRARIES
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from itertools import combinations_with_replacement
import numpy as np

#IMPORT FUNCTIONS
import Helper_funcs


#CREATE CLIENT
scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/giuseppecrosti/Documents/1weekoffood/client_secret.json', scope)
client = gspread.authorize(creds)

#OPEN WORKSHEETS
worksheet = client.open("1week of food calculator")
worksheet_data = client.open("Data_1weekMVP")

#STORE INPUTS
inputs = worksheet.get_worksheet(0)

mouths = int(inputs.cell(6,4).value)
lunch_p = float(int(inputs.cell(7,4).value[:len(inputs.cell(7,4).value)-1])/100)
dinner_p = float(int(inputs.cell(8,4).value[:len(inputs.cell(8,4).value)-1])/100)
time = int(inputs.cell(9,4).value)
veg = inputs.cell(10,4).value
gf = inputs.cell(11,4).value


#CREATE TABLES
meals = pd.DataFrame(worksheet_data.get_worksheet(7).get_all_records())
meals_recipes = pd.DataFrame(worksheet_data.get_worksheet(5).get_all_records())
recipes = pd.DataFrame(worksheet_data.get_worksheet(0).get_all_records())

