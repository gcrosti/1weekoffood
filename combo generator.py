#%% IMPORT LIBRARIES
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from itertools import combinations_with_replacement
import numpy as np 
from collections import Counter
import pickle
import pprint

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
percentages = [0.25,0.5,0.75,1,1.25,1.5,1.75,2]
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
    #print(portion)
    meal_combos[portion] = []
    for combo in all_combos[portion]:
        if not combo:
           continue
        if toomanyleftovers(combo):
            continue
        meal_combos[portion].append(combo)
        if len(meal_combos[portion]) > 50:
            break
#%%
print(meal_combos.keys())
#%% GENERATE REMAINING COMBOS
empty_portions = []
existing_portions = meal_combos.keys()
for mouth in range(2,6):
    for amt in existing_portions:
        portion = amt*mouth
        if portion in existing_portions:
            continue
        empty_portions.append(portion)


print(len(empty_portions),empty_portions)

#%% PAIR ADDITION OF COMBOS
new_combos = {}
for pair in combinations_with_replacement(existing_portions,2):
    #print(pair)
    sumpair = sum(pair)
    if sumpair > 70:
        continue
    if sumpair in empty_portions:
        new_combos[sumpair] = [x+y for x,y in zip(meal_combos[pair[0]],meal_combos[pair[1]])]
        empty_portions.remove(sumpair)

print(len(empty_portions),new_combos.keys())

#%% TRIP ADDITION OF COMBOS
for trip in combinations_with_replacement(existing_portions,3):
    sumtrip = sum(trip)
    if sumtrip > 70:
        continue
    if sumtrip in empty_portions or float(sumtrip) in empty_portions:
        new_combos[sumtrip] = [x+y+z for x,y,z in zip(meal_combos[trip[0]],meal_combos[trip[1]],meal_combos[trip[2]])]
        empty_portions.remove(sumtrip)

print(len(empty_portions),new_combos.keys())

#%% PENTA ADDITION OF COMBOS
for penta in combinations_with_replacement(existing_portions,5):
    sumpenta = sum(penta)
    if sumpenta > 70:
        continue
    if sumpenta in empty_portions or float(sumpenta) in empty_portions:
        new_combos[sumpenta] = [x+y+z+a+b for x,y,z,a,b in zip(meal_combos[penta[0]],
        meal_combos[penta[1]],meal_combos[penta[2]],meal_combos[penta[3]],meal_combos[penta[4]])]
        empty_portions.remove(sumpenta)

print(len(empty_portions),new_combos.keys())

#%%
print(new_combos[70])
#%% MERGE DICTS
for portion, combo in new_combos.items():
    meal_combos[portion] = combo

print(meal_combos.keys())
#%% PICKLE COMBOS
with open('all_combos.pickle','wb') as f:
    pickle.dump(meal_combos,f,protocol=2)


#%% OLD CODE

for trip in combinations_with_replacement(meal_combos.keys(),3):
    sumtrip = sum(trip)
    if sum(trip) > 70:
        continue
    if sumtrip in empty_portions:
        meal_combos[sumtrip].append(meal_combos[trip[0]]+meal_combos[trip[1]]+meal_combos[trip[2]])

empty_portions_count2 = len([k for k in meal_combos.keys() if not meal_combos[k]])
print(empty_portions_count2)
#%%
print(len(meal_combos[70]))
#%%
for quart in combinations_with_replacement(meal_combos.keys(),4):
    if sum(quart) < 22:
        continue
    if sum(quart) > 70:
        continue
    print(sum(quart))

empty_portions_count2 = len([k for k in meal_combos.keys() if not meal_combos[k]])
