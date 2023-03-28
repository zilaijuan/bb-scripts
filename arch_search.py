# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 08:54:38 2023

@author: zilaijuan
"""

import requests
from bs4 import BeautifulSoup
import re

import json
import sys
import os

# todo modify here
baseDir="."

def request(method, url, payload=None):
    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'PHPSESSID=drdsifj3qpqcr3rbp3ia81etnc'
    }
    payload=json.dumps(payload)
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text



url = "https://radio.kasi.re.kr/arch/getdata_mongo.php"
payload = {
  "page": "1",
  "obs_year": "",
  "exp_code": "",
  "source_name": "M87",
  "right_ascension": "",
  "declination": "",
  "polarization": [],
  "band": []
}

exp_code=input("Exper code:")
source_name=input("Target name:")
payload["exp_code"]=exp_code
payload["source_name"]=source_name

text=request("POST", url, payload)
re_pages=re.search("observation data. (\d+) pages", text)
total_pages = None
if re_pages:
    total_pages=(int) (re_pages.group(1))
if not total_pages:
    print("no result, will exit.")    
    sys.exit(0)
exper_code_list=[]    
for page in range(1,total_pages+1):
    print("page No."+str(page)+" processing...")
    payload["page"]=str(page)
    text=request("POST", url, payload)
    soup = BeautifulSoup(text,features="lxml")
    strong_list=soup.find_all("strong")
    for strong in strong_list:
        exper_code_result=re.search("Exper code: ([a-z0-9]*)", strong.text)
        if exper_code_result:
            exper_code=exper_code_result.group(1)
            exper_code_list.append(exper_code)
            print("Exper code found! "+exper_code)
print("download start....")
detail_url="https://radio.kasi.re.kr/arch/pop_data.php?id="
for exper_code in exper_code_list:
    text=request("GET", detail_url+exper_code)
    soup = BeautifulSoup(text,features="lxml")
    url_list = soup.p.text.split("wget")
    clean_url_list=[]
    for download_rul in url_list:
        clean_url=download_rul.strip()
        if clean_url.startswith("http"):
            clean_url_list.append("wget "+clean_url)
    if len(clean_url_list) >0 :
        file_path = os.path.join(baseDir,exper_code+".sh")
        with open(file_path, 'w', encoding="utf8", newline="\n") as fp:
            fp.write('\n'.join(clean_url_list))
        print("file saved. "+ file_path)



