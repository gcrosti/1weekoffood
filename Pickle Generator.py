#%% IMPORT LIBRARIES
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pickle

#%% CREATE CLIENT
scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/giuseppecrosti/weekoffood/1weekoffood/client_secret.json', scope)
client = gspread.authorize(creds)

#%% OPEN WORKSHEET
worksheet_data = client.open("Data_1weekMVP")
#%% OPEN SHEETS
meals = worksheet_data.get_worksheet(6).get_all_records()
meals_recipes = worksheet_data.get_worksheet(4).get_all_records()
recipes = worksheet_data.get_worksheet(0).get_all_records()
recipes_ingredients = worksheet_data.get_worksheet(2).get_all_records()

#%% PICKLE

with open('meals.pickle','wb') as f:
    pickle.dump(meals,f,protocol=2)

with open('meals_recipes.pickle','wb') as f:
    pickle.dump(meals_recipes,f,protocol=2)

with open('recipes.pickle','wb') as f:
    pickle.dump(recipes,f,protocol=2)

with open('recipes_ingredients.pickle','wb') as f:
    pickle.dump(recipes_ingredients,f,protocol=2)
#%%
