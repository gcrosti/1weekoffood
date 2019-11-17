

from itertools import combinations_with_replacement, islice
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np


# CREATE CLIENT
scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/giuseppecrosti/Documents/1weekoffood/client_secret.json', scope)
client = gspread.authorize(creds)
worksheet_data = client.open("Data_1weekMVP")

#GLUTEN-FREE FILTER
def gf_filter(meals,gf):
    meals1 = meals
    if gf == 'y':
        meals1 = meals[meals['Gluten-free?']=='y']
    return meals1

#VEGETARIAN FILTER
def veg_filter(meals,veg):
    meals1 = meals
    if veg == 'y':
        meals1 = meals[meals['Vegetarian?']=='y'] 
    return meals1

#GENERATE MEALS
def generate_meals(inputs):
    meals = pd.DataFrame(worksheet_data.get_worksheet(6).get_all_records())
    meals1 = gf_filter(meals,inputs['s_gf'])
    meals2 = veg_filter(meals1,inputs['s_veg'])
    total_portions = int(7 * (int(inputs['s_lunch_p'][:len(inputs['s_lunch_p'])-1])/100) + 7 * (int(inputs['s_dinner_p'][:len(inputs['s_dinner_p'])-1])/100)) * int(inputs['s_mouths'])
    meal_combos = (combinations_with_replacement(meals2['id'],total_portions))
    meal_combos2 = (x for x in meal_combos if len(set(x)) > 2)
    varied_combos = {}
    min_var = 0
    for combo in meal_combos2:
        set_combo = set(combo)
        count = 0
        for meal in set_combo:
            if int(combo.count(meal)) % int(meals2[meals2['id']==meal]['max_min_portion']) > 1:
                break
            count += 1
            if count == len(set_combo):
                count = 0
                if len(varied_combos) < 10:
                    varied_combos[np.var(combo)] = combo
                    min_var = min(varied_combos.keys())
                    break
                if min_var < np.var(combo):
                    varied_combos[np.var(combo)] = combo
                    del varied_combos[min_var]
                    min_var = min(varied_combos.keys())
                

    return varied_combos.values()

