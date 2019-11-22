

#%%
from itertools import combinations_with_replacement, islice
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np

#%%
# CREATE CLIENT
scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/giuseppecrosti/Documents/1weekoffood/client_secret.json', scope)
client = gspread.authorize(creds)
worksheet_data = client.open("Data_1weekMVP")

#%% OPEN PICKLED COMBOS
combos = pd.read_pickle('/Users/giuseppecrosti/Documents/1weekoffood/all_combos.pkl')

#%% OPEN TABLES
meals = pd.DataFrame(worksheet_data.get_worksheet(6).get_all_records())

#%% HELPER FUNCS

#GLUTEN-FREE FILTER
def gf_filter(combo):
    ans = 'y'
    for meal in set(combo):
        if meals[meals['id']==meal]['Gluten-free?']=='n':
            ans = 'n'
            break
    return ans

#VEGETARIAN FILTER
def veg_filter(combo):
    ans = 'y'
    for meal in set(combo):
        if meals[meals['id']==meal]['Vegetarian?']=='n':
            ans = 'n'
            break
    return ans

#TIME CALCULATION
def enter_time(combo):
    time = {}
    time['active'] = 0
    time['passive'] = 0
    for meal in set(combo):
        time['active'] += meals[meals['id']==meal]['total_active_time'] 
        #time['passive'] = max([meals[meals['id']==meal]['max_passive_time'],time['passive']])
    return time

#%% ENRICH COMBOS
combos['active_time'] = [enter_time(x)['active'] for x in combos['combo']]
#combos['passive_time'] = [enter_time(x)['passive'] for x in combos['combo']]
combos['veg'] = [veg_filter(x) for x in combos['combo']]
combos['gf'] = [gf_filter(x) for x in combos['combo']]




#%%
