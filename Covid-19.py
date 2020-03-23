import datetime
import json
import requests
import argparse
import logging
from bs4 import BeautifulSoup
from tabulate import tabulate
import pandas as pd

FORMAT = '[%(asctime)-15s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG, filename='bot.log', filemode='a')

URL = 'https://www.mohfw.gov.in/'
SHORT_HEADERS = ['Sno', 'State','In','Fr','Cd','Dt']
FILE_NAME = 'corona_india_data.json'
extract_contents = lambda row: [x.text.replace('\n', '') for x in row]


def save(x):
    with open(FILE_NAME, 'w') as f:
        json.dump(x, f)


def load():
    res = {}
    with open(FILE_NAME, 'w+') as f:
        res = json.load(f)
    return res
    


interested_states = ["Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu & Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttarakhand","Uttar Pradesh","West Bengal","Andaman and Nicobar Islands","Chandigarh","The Government of NCT of Delhi","Dadra and Nagar Haveli","Daman and Diu","Lakshadweep","Puducherry"]

current_time = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
info = []

try:
    response = requests.get(URL).content
    soup = BeautifulSoup(response, 'html.parser')
    header = extract_contents(soup.tr.find_all('th'))
    print("__")
    stats = []
    all_rows = soup.find_all('tr')
    for row in all_rows:
        stat = extract_contents(row.find_all('td'))
        #print(stat)
        if stat:
            if len(stat) == 5:
                # last row
                stat = ['', *stat]
                stats.append(stat)
            elif any([s.lower() in stat[1].lower() for s in interested_states]):
                stats.append(stat)
    cur_data = {x[1]: {current_time: x[2:]} for x in stats}
except Exception as e:
  print(e)
col = ["S_No"   ,"NameofState"  ,"Total_Confirmed_cases_(Indian_National)","Total_Confirmed_cases_(Foreign_National)","Cured_Discharged/Migrated",  "Death"]
df = pd.DataFrame(stats,columns=col)
df = df[:-1]
df.drop(["S_No"],inplace=True,axis=1)
df[["Total_Confirmed_cases_(Indian_National)","Total_Confirmed_cases_(Foreign_National)","Cured_Discharged/Migrated",   "Death"]] = df[["Total_Confirmed_cases_(Indian_National)","Total_Confirmed_cases_(Foreign_National)","Cured_Discharged/Migrated",   "Death"]].apply(pd.to_numeric)
df.to_csv("data.csv",index=False)