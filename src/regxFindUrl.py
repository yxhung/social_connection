__author__ = 'yxhung'

import requests
from bs4 import BeautifulSoup
import os
import shutil
import re


os.chdir('../../whoscall/openCid')

global dump

def download_file(url):
    global dump
    file = requests.get(url, stream=True)
    dump = file.raw

def save_file(fn):
    global dump
    with open(fn, 'wb') as location:
        shutil.copyfileobj(dump, location)
    del dump

# 1. download the database from OpenCellId
url = 'http://opencellid.org/downloads/?apiKey=db112c9c-0b36-4573-85d6-cfff827bbf35'
html = requests.get(url).text
soup = BeautifulSoup(html)
all_links = soup.findAll('a', href=True)
for link in all_links:
    if re.search('cell_towers', link['href']) :
        print(link['href'])
        url = 'http://opencellid.org'+link['href']
        download_file(url)
        fn = link['href'].split('=')[2]
        save_file(fn)

