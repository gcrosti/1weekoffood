#%%
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

#%%
# use creds to create a client to interact with the Google Drive API
scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/giuseppecrosti/Documents/1weekoffood/client_secret.json', scope)
client = gspread.authorize(creds)

#%%
# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
worksheet = client.open("Data_1weekMVP")

#%%
ingredients_recipes = worksheet.get_worksheet(2).get_all_records()

#%%
meals_additional_ingredients = worksheet.get_worksheet(6).get_all_records()

#%%
r_ingredients = [row['ingredient_name'] for row in ingredients_recipes]
#%%
m_ingredients = [row['ingredient_name'] for row in meals_additional_ingredients]


#%%
tot_ingredients = r_ingredients + m_ingredients
#%%
set_ingredients = list(set(tot_ingredients))

#%%
ingredients_wks = worksheet.get_worksheet(1)

#%%
cell_listA = ingredients_wks.range('A2:A{}'.format(1+len(set_ingredients)))
cell_listB = ingredients_wks.range('B2:B{}'.format(1+len(set_ingredients)))
#%%

for i in range(len(set_ingredients)):
    cell_listA[i].value = set_ingredients[i]
    cell_listB[i].value = i+1
#%%
ingredients_wks.update_cells(cell_listA)
ingredients_wks.update_cells(cell_listB)
#%%
