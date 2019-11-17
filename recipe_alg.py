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

#%%
print([0]*4)
#%% OPEN WORKSHEETS
worksheet = client.open("1week of food calculator")
worksheet_data = client.open("Data_1weekMVP")
#%% STORE INPUTS
inputs = worksheet.get_worksheet(0)

mouths = int(inputs.cell(6,4).value)
lunch_p = float(int(inputs.cell(7,4).value[:len(inputs.cell(7,4).value)-1])/100)
dinner_p = float(int(inputs.cell(8,4).value[:len(inputs.cell(8,4).value)-1])/100)
time = int(inputs.cell(9,4).value)
veg = inputs.cell(10,4).value
gf = inputs.cell(11,4).value

#%% CREATE TABLES
meals = pd.DataFrame(worksheet_data.get_worksheet(6).get_all_records())
meals_recipes = pd.DataFrame(worksheet_data.get_worksheet(4).get_all_records())
recipes = pd.DataFrame(worksheet_data.get_worksheet(0).get_all_records())


#%% FILTER 1: GF
meals1 = meals
if gf == 'y':
    meals1 = meals[meals['Gluten-free?']=='y']

#%% FILTER 2: VEGETARIAN
meals2 = meals1
if veg == 'y':
    meals2 = meals1[meals1['Vegetarian?']=='y'] 

#%%
meals2
#%% GENERATE MEAL COMBOS BASED ON PORTION CALCULATIONS
total_portions = 7 * (lunch_p+dinner_p) * mouths
meal_combos = list(combinations_with_replacement(meals2['id'],int(total_portions)))

print(total_portions)

#%% FILTER FOR LEFTOVERS AND VARIABILITY
meal_combos2 = []
for combo in meal_combos:
    if len(set(combo)) < 3:
        continue
    set_combo = set(combo)
    count = 0
    for meal in set_combo:
        if int(combo.count(meal)) % int(meals2[meals2['id']==meal]['max_min_portion']) > 1:
            break
        count += 1
        if count == len(set_combo):
            meal_combos2.append(combo)
            count = 0

print(len(meal_combos),len(meal_combos2))
#%%
meal_combos_df = pd.DataFrame()
#%%
meal_combos_df['combos'] = meal_combos2
#%%
def extract_active_time(l):
    total = 0
    for meal in l:
        total += int(meals2[meals2['id'] == meal]['total_active_time'])
    return total
#%%
meal_combos_df['total_active_time'] = [extract_active_time(set(x)) for x in meal_combos_df['combos']]

#%%
meal_combos_df['var'] = [np.var(x) for x in meal_combos_df['combos']]

#%%
out = meal_combos_df.sort_values(by='var',ascending=False).head(10)
#%%
output_raw = worksheet.get_worksheet(1)
cells_combos = output_raw.range('A1:A10')
cells_time = output_raw.range('B1:B10')

#%%
i = 0
for combo in out['combos']:
    cells_combos[i].value = str(combo)
    i +=1 

i = 0
for time in out['total_active_time']:
    cells_time[i].value = time
    i += 1

output_raw.update_cells(cells_combos)
output_raw.update_cells(cells_time)
#%%
