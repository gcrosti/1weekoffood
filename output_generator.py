from datetime import datetime
import os
import pytz
import requests
import math
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# CREATE CLIENT
scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/giuseppecrosti/Documents/1weekoffood/client_secret.json', scope)
client = gspread.authorize(creds)
worksheet_data = client.open("Data_1weekMVP")


# OPEN ENRICHED COMBOS
enriched_combos = pd.read_pickle('/Users/giuseppecrosti/Documents/1weekoffood/combos_enriched.pkl')

# OPEN OTHER DATASETS
meals = pd.DataFrame(worksheet_data.get_worksheet(6).get_all_records())
meals_recipes = pd.DataFrame(worksheet_data.get_worksheet(4).get_all_records())
recipes = pd.DataFrame(worksheet_data.get_worksheet(0).get_all_records())

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
    possible_combos = enriched_combos[enriched_combos['veg']==f_inputs['veg']][enriched_combos['gf']==f_inputs['gf']][enriched_combos['portion']==f_inputs['mouths']]
    out = pd.DataFrame()
    sample = possible_combos.sample() 
    out['meal_id'] = [x for x in set(sample['combo'].values[0])]
    out['meal_name'] = [meals[meals['id']==x]['Meal_name'].values[0] for x in out['meal_id']]
    out['recipes'] = [meals_recipes[meals_recipes['Meal_id']==x]['Recipe_name'].values for x in out['meal_id']]
    out['recipe_urls'] = [meals_recipes[meals_recipes['Meal_id']==x]['recipe_urls'].values for x in out['meal_id']]
    out['servings'] = [sample['combo'].values[0].count(x) for x in out['meal_id']]
    return out
    


    