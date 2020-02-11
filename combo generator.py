#%% IMPORT LIBRARIES
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from itertools import combinations_with_replacement
import numpy as np 
from collections import Counter

#%% CREATE CLIENT
scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/giuseppecrosti/weekoffood/1weekoffood/client_secret.json', scope)
client = gspread.authorize(creds)

#%% OPEN WORKSHEETS
worksheet = client.open("1week of food calculator")
worksheet_data = client.open("Data_1weekMVP")

#%% CREATE TABLES
meals = worksheet_data.get_worksheet(6).get_all_records()
meals_recipes = worksheet_data.get_worksheet(4).get_all_records()
recipes = worksheet_data.get_worksheet(0).get_all_records()


#%% GENERATE ALL MEAL COMBO ITERATORS
percentages = [0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3]
all_combos = {}
for percentage in percentages:
    portion = 7*percentage
    all_combos[portion] = combinations_with_replacement([x['id'] for x in meals],int(portion))

#%%
all_combos
#%%GENERATE DICS OF ID-MAXMINPORTIONS
portiondict = {}
for meal in meals:
    portiondict[meal['id']] = meal['max_min_portion']

#%% GENERATE FILTER FOR LEFTOVERS
def toomanyleftovers(combo):
    set_combo = set(combo)
    if len(set_combo) > 4:
        return True
    c = Counter(combo)
    for meal in set_combo:
        left = abs(int(c[meal]) - int(portiondict[meal]))
        if left > 1:
            return True       
    return False
#%% GENERATE COMBOS
meal_combos = {}
for portion in all_combos:
    print(portion)
    meal_combos[portion] = []
    for combo in all_combos[portion]:
        if not combo:
           continue
        if toomanyleftovers(combo):
            continue
        meal_combos[portion].append(combo)
        if len(meal_combos[portion]) > 20:
            break

#%%
meal_combos
#%% PICKLE COMBOS
#meal_combos_df.to_pickle('all_combos.pkl')
#%%

#%% CREATE ARRAYS
columns = []
dts = []
for k in meals[0].keys():
    dts.append((k,type(meals[0][k])))
    columns.append(tuple([meal[k] for meal in meals]))
#print(dts)
meals_arr = np.array(columns,dtype=dts)