

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
combos.head()

#%% OPEN TABLES
meals = pd.DataFrame(worksheet_data.get_worksheet(6).get_all_records())

#%% HELPER FUNCS

#GLUTEN-FREE FILTER
def gf_filter(combo):
    ans = 'y'
    for meal in set(combo):
        if str(meals[meals['id']==meal]['Gluten-free?'])=='n':
            ans = 'n'
            break
    return ans

#VEGETARIAN FILTER
def veg_filter(combo):
    ans = 'y'
    for meal in set(combo):
        if str(meals[meals['id']==meal]['Vegetarian?']) =='n':
            ans = 'n'
            break
    return ans

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
active_time = []
passive_time = []
veg = []
gf = []
for combo in combos['combo']:
    if not combo:
        continue
    t = enter_time(combo)
    active_time.append(t['active'])
    passive_time.append(t['passive'])
    veg.append(veg_filter(combo))
    gf.append(gf_filter(combo))
#%%
active_time = []
for combo in combos['combo']:
    active_time.append(enter_time(combo)['active'])

active_time
#%%
combos['active_time'] = active_time
#combos['passive_time'] = passive_time
#combos['veg'] = veg
#combos['gf'] = gf
combos.head()


#%%
combos.to_pickle('combos_enriched.pkl')
#%%
combos_enriched_pkl = pd.read_pickle('/Users/giuseppecrosti/Documents/1weekoffood/combos_enriched.pkl')
combos_enriched_pkl.head()



#%%
combos_enriched_pkl[combos_enriched_pkl['gf']=='n'].head()

#%%
