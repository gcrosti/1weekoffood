from datetime import datetime
import os
import pytz
import requests
import math
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# CREATE CLIENT
scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/giuseppecrosti/Documents/1weekoffood/client_secret.json', scope)
client = gspread.authorize(creds)


def query_api(city):
    worksheet = client.open("1week of food calculator")
    return worksheet.get_worksheet(0)