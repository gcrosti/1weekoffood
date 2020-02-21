

#%%
from itertools import combinations_with_replacement, islice
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
import pickle

#%%OPEN DATA
with open('meals.pickle','rb') as f:
    meals = pickle.load(f)
with open('meals_recipes.pickle','rb') as f:
    meals_recipes = pickle.load(f)
with open('recipes.pickle','rb') as f:
    recipes = pickle.load(f)
with open('all_combos.pickle','rb') as f:
    all_combos = pickle.load(f)

#%%
#print(meals)
#%% HELPER FUNCS

#REFACTORING DATA
gf_mealids = []
veg_mealids = []
timedict = {}
for meal in meals:
    aidee = meal['id']
    if meal['Gluten-free?'] == 'y':
        gf_mealids.append(aidee)
    if meal['Vegetarian?'] == 'y':
        veg_mealids.append(aidee)
    timedict[aidee] = [meal['total_active_time'],meal['max_passive_time']]


#GLUTEN-FREE FILTER
def is_gf(combo):
    for meal in set(combo):
        if meal in gf_mealids:
            return 'y'      
    return 'n'

#VEGETARIAN FILTER
def is_veg(combo):
    for meal in set(combo):
        if meal in veg_mealids:
            return 'y'
    return 'n'

print(timedict)
#%%
#TIME CALCULATION

def enter_time(combo):
    time = {}
    time['active'] = 0
    time['passive'] = 0
    for meal in set(combo):
        time['active'] += int(meals[meals['id']==meal]['total_active_time']) 
        time['passive'] = max([int(meals[meals['id']==meal]['max_passive_time']),time['passive']])
    return time

#%% ENRICH COMBOS
enriched_combos = []
for portion, combos in all_combos.items():
    for combo in combos:
        combo_dict = {}
        combo_dict['portion'] = portion
        combo_dict['combo'] = combo
        comboset = set(combo)
        if all(item in veg_mealids for item in comboset):
            combo_dict['veg'] = 'y'
            print(combo_dict)
        else:
            combo_dict['veg'] = 'n'
        if all(item in gf_mealids for item in comboset):
            combo_dict['gf'] = 'y'
        else:
            combo_dict['gf'] = 'n'
        combo_dict['total_active_time'] = sum(timedict[x][0] for x in comboset)
        combo_dict['max_passive_time'] = max(timedict[x][1] for x in comboset)
        enriched_combos.append(combo_dict)

enriched_combos[100]
#%%
len(enriched_combos)

#%%
with open('enriched_combos_l.pickle','wb') as f:
    pickle.dump(enriched_combos,f,protocol=2)

#%% TESTING
vegcombos = [(1,1,1,1),(1,1,1,2),(1,1,2,2),(1,2,3,4)]
for combo in vegcombos:
    if all(item in veg_mealids for item in set(combo)):
        print('yay')
    else:
        print('womp')

#%%
