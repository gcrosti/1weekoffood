

#%%
from itertools import combinations_with_replacement, islice
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
import pickle
from collections import Counter
from __future__ import division


#%%OPEN DATA
with open('meals.pickle','rb') as f:
    meals = pickle.load(f)
with open('meals_recipes.pickle','rb') as f:
    meals_recipes = pickle.load(f)
with open('recipes.pickle','rb') as f:
    recipes = pickle.load(f)
with open('all_combos.pickle','rb') as f:
    all_combos = pickle.load(f)
with open('recipes_ingredients.pickle','rb') as f:
    recipes_ingredients = pickle.load(f)


#%%
#print(meals)
#%% REFACTORING GF, VEG, TIME DATA
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

#%% ADD GF, VEG, ACTIVE TIME, PASSIVE TIME
enriched_combos = []
for portion, combos in all_combos.items():
    for combo in combos:
        combo_dict = {}
        combo_dict['portion'] = portion
        combo_dict['combo'] = combo
        comboset = set(combo)
        if all(item in veg_mealids for item in comboset):
            combo_dict['veg'] = 'y'
            #print(combo_dict)
        else:
            combo_dict['veg'] = 'n'
        if all(item in gf_mealids for item in comboset):
            combo_dict['gf'] = 'y'
        else:
            combo_dict['gf'] = 'n'
        combo_dict['total_active_time'] = sum(timedict[x][0] for x in comboset)
        combo_dict['max_passive_time'] = max(timedict[x][1] for x in comboset)
        enriched_combos.append(combo_dict)

#enriched_combos[100]
#%%
#len(enriched_combos)

#%% REFACTOR RECIPE DATA
meal_recipe_dict = {}
for meal_id in set(x['Meal_id'] for x in meals_recipes):
    meal_recipe_dict[meal_id] = []

for elem in meals_recipes:
    meal_recipe_dict[elem['Meal_id']].append(elem)

#print(meal_recipe_dict[1])

#%% CREATE MEALNAME DICT
mealnames = {}
for meal in meals:
    mealnames[meal['id']] = meal['Meal_name']

#%% ADD RECIPE DATA AND MEAL MULTIPLIER
for combo_dict in enriched_combos:
    setcombo = set(combo_dict['combo'])
    c = Counter(combo_dict['combo'])
    combo_recipes = []
    meal_multipliers = {}
    for meal_id in setcombo:
        meal_multipliers[mealnames[meal_id]] = c[meal_id]
        meal_recipes = meal_recipe_dict[meal_id]
        for r in meal_recipes:
            recipe = {}
            recipe['active_time'] = r['active_time']
            recipe['min_portion'] = r['min_portion']
            recipe['passive_time'] = r['passive_time']
            recipe['recipe_id'] = r['Recipe_id']
            recipe['meal_id'] = meal_id
            recipe['meal_name'] = r['Meal_name']
            recipe['recipe_name'] = r['Recipe_name']
            recipe['recipe_url'] = r['recipe_urls']
            recipe['multiplier'] = round(c[meal_id]/r['min_portion'],1)
            combo_recipes.append(recipe)
    combo_dict['recipes'] = combo_recipes
    combo_dict['meal_multipliers'] = meal_multipliers

#%% REFACTOR INGREDIENT DATA
recipe_ingredient_dict = {}
for recipe_id in set(x['recipe_Id'] for x in recipes_ingredients):
    recipe_ingredient_dict[recipe_id] = []

for elem in recipes_ingredients:
    recipe_ingredient_dict[elem['recipe_Id']].append(elem)

#print(recipe_ingredient_dict[1])

#%% ADD INGREDIENT DATA
for combo_dict in enriched_combos:
    setcombo = set(combo_dict['combo'])
    combo_ingredients = {}
    for recipe in combo_dict['recipes']:
        for ingredient in recipe_ingredient_dict[recipe['recipe_id']]:
            if ingredient['ingredient_id'] not in combo_ingredients.keys():
                combo_ingredients[ingredient['ingredient_id']] = {}
                combo_ingredients[ingredient['ingredient_id']]['amount'] = ingredient['amount ']*recipe['multiplier']
                combo_ingredients[ingredient['ingredient_id']]['units'] = ingredient['units']
                combo_ingredients[ingredient['ingredient_id']]['required?'] = ingredient['required?']
                combo_ingredients[ingredient['ingredient_id']]['name'] = ingredient['ingredient_name']
                combo_ingredients[ingredient['ingredient_id']]['recipe_name'] = ingredient['recipe_title']
            else:
                combo_ingredients[ingredient['ingredient_id']]['amount'] += ingredient['amount ']*recipe['multiplier']
    combo_dict['ingredients'] = combo_ingredients

#enriched_combos[32]['ingredients']

#%% PICKLE

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
