from __future__ import division
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

# GENERATE VIABLE OUTPUTS
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
        
    sorted_combos = sorted(possible_combos, key = lambda i: i['total_active_time'])
    if sorted_combos:
        out = [sorted_combos[0],sorted_combos[int(round(len(sorted_combos)/2))],sorted_combos[-1]]
        return out
    return "no combos available :("
    


    