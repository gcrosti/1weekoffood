from datetime import datetime
import os
import pytz
import requests
import math
import pickle
import random

# OPEN ENRICHED COMBOS
with open('enriched_combos_l.pickle','rb') as f:
    enriched_combos = pickle.load(f)

# OPEN OTHER DATASETS
with open('meals.pickle','rb') as f:
    meals = pickle.load(f)
with open('meals_recipes.pickle','rb') as f:
    meals_recipes = pickle.load(f)
with open('recipes.pickle','rb') as f:
    recipes = pickle.load(f)

# FORMAT INPUTS
def format_inputs(x):
    r = {}
    r['veg'] = str(x['s_veg'][0])
    r['gf'] = str(x['s_gf'][0])
    lunch_p = int(x['s_lunch_p'][:len(x['s_lunch_p'])-1])/100
    dinner_p = int(x['s_dinner_p'][:len(x['s_dinner_p'])-1])/100
    r['mouths'] = int(x['s_mouths'])*(lunch_p+dinner_p)*7
    print(r)
    return r

def output(inputs):
    f_inputs = format_inputs(inputs)
    possible_combos = []
    for row in enriched_combos:
        if f_inputs['veg'] == 'y':
            if row['veg'] != 'y':
                continue
        if f_inputs['gf'] == 'y':
            if row['gf'] != 'y':
                continue
        if row['portion'] == f_inputs['mouths']:
            possible_combos.append(row) 
    
    #sample = random.sample(possible_combos,10)
    out = possible_combos
    #out['meal_id'] = [x for x in set(sample['combo'][0])]
    #out['meal_name'] = [meals[meals['id']==x]['Meal_name'].values[0] for x in out['meal_id']]
    #out['recipes'] = [meals_recipes[meals_recipes['Meal_id']==x]['Recipe_name'].values for x in out['meal_id']]
    #out['recipe_urls'] = [meals_recipes[meals_recipes['Meal_id']==x]['recipe_urls'].values for x in out['meal_id']]
    #out['servings'] = [sample['combo'].values[0].count(x) for x in out['meal_id']]
    return out
    


    