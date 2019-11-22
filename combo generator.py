#%% IMPORT LIBRARIES
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from itertools import combinations_with_replacement
import numpy as np

#%% CREATE CLIENT
scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/giuseppecrosti/Documents/1weekoffood/client_secret.json', scope)
client = gspread.authorize(creds)

#%% OPEN WORKSHEETS
worksheet = client.open("1week of food calculator")
worksheet_data = client.open("Data_1weekMVP")

#%% CREATE TABLES
meals = pd.DataFrame(worksheet_data.get_worksheet(6).get_all_records())
meals_recipes = pd.DataFrame(worksheet_data.get_worksheet(4).get_all_records())
recipes = pd.DataFrame(worksheet_data.get_worksheet(0).get_all_records())

#%% GENERATE ALL MEAL COMBOS
percentages = [0.25,0.5,0.75,1,1.25,1.5,1.75,2]
mouths = [1,2,3,4,5]
all_combos = {}
for percentage in percentages:
    for mouth in mouths:
        portion = 7*percentage*mouth
        all_combos[portion] = combinations_with_replacement(meals['id'],int(portion))

#%% GENERATE FILTER FOR LEFTOVERS
def checkforleftovers(combo):
    set_combo = set(combo)
    count = 0
    for meal in set_combo:
        if int(combo.count(meal)) % int(meals[meals['id']==meal]['max_min_portion']) > 1:
            break
        count += 1
        if count == len(set_combo):
            return True
    return False

#%% GENERATE COMBOS DF
meal_combos_df = pd.DataFrame(columns=('portion','combo'))
for portion in all_combos:
    print(portion)
    len_set = 0
    for combo in all_combos[portion]:
        if not combo:
            continue
        if not checkforleftovers(combo):
            continue
        if len(set(combo)) <= len_set:
            continue
        meal_combos_df = meal_combos_df.append({'portion':portion,'combo':combo},ignore_index=True)
        len_set = min([3,len(set(combo))])
        if len(meal_combos_df[meal_combos_df['portion']==portion]['portion']) == 1000:
            break

meal_combos_df.head()
#%% PICKLE COMBOS
meal_combos_df.to_pickle('all_combos.pkl')
#%%
 
def extract_active_time(l):
    total = 0
    for meal in l:
        total += int(meals[meals['id'] == meal]['total_active_time'])
    return total
