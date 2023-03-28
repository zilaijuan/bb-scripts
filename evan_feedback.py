# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 10:35:38 2023

@author: zilaijuan
"""

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import json
import sys
import os

# todo modify here
baseDir="."

def request(method, url, payload=None):
    headers = {
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54',
      'Cookie': 'PHPSESSID=drdsifj3qpqcr3rbp3ia81etnc'
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text

url="https://radio.kasi.re.kr/feedback_get_list.php"

payload={'exp_code': '111',
'title': '',
'page': '1'}

exp_code=input("Exper code:")
title=input("title:")
payload["exp_code"]=exp_code
payload["title"]=title

total_pages=0

text = request("POST",url,payload)
soup = BeautifulSoup(text,features="lxml")
pages_link=soup.nav.find_all("a")
if len(pages_link)>0:
    last_button=pages_link[-1]['href']
    match = re.search("(\d+)",last_button)
    if match:
        total_pages=int(match.group(1))
else:
    match = re.search("(\d+) recordes found!",text)
    if int(match.group(1))>0:
        total_pages=1
    else:
        print("no data found! will exit.")
        sys.exit(0)
data=[]
for page in range(1,total_pages+1):
    payload['page']=page
    text = request("POST",url,payload)
    soup = BeautifulSoup(text,features="lxml")
    table_body = soup.tbody

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')

        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values

filename=exp_code+"_"+title+".xlsx"
file_path = os.path.join(baseDir,filename)
df = pd.DataFrame(data)
writer = pd.ExcelWriter(file_path)
df.columns=["Exp_code","Title","PI","Obs.Time","Correlated","Distributed"]
df.to_excel(writer, index=False)
writer.save()