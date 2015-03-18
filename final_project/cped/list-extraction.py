import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re
import sys
import csv

#Get the last page number.
req = requests.get('http://cped.nccu.edu.tw/view-resume')
src = req.text
soup = BeautifulSoup(src)
row = soup.select('li > a')
last_page_url = row[9]['href']
last_page_number = int(last_page_url.split("=")[-1])
print "There are totally " + str(last_page_number) + " pages of actors in the database."

def get_cadres(url):
    '''Get cadre names and links from the url.'''
    req = requests.get(url)
    src = req.text
    soup = BeautifulSoup(src)
    rows = soup.select('tbody > tr')
    cadres = []
    for row in rows:
        rowData = [cell.text for cell in row.select('td')]
        name_CHN = rowData[0].encode('utf-8')
        name_ENG = rowData[1].encode('utf-8')
        cadre_relative_url = row.select('a')[0]['href']
        cadre_full_url = 'http://cped.nccu.edu.tw' + cadre_relative_url
        cadres.append((name_ENG.strip(), name_CHN.strip(), cadre_full_url))
    return cadres

print "Starting to extract the name list."
#Get all cadres
cadre_info = []
for i in range(last_page_number + 1): #The page numbers starts with 0.
    print "Page " + str(i) +" extracted."
    page_url = 'http://cped.nccu.edu.tw/view-resume?page=' + str(i)
    page_cadre_info =  get_cadres(page_url)
    cadre_info = cadre_info + page_cadre_info
print "Extraction completed."

cadre_num = len(cadre_info)
print "There are " + str(cadre_num) + " resumes in the database."

outfile = open('cadre_list.csv', 'wb')
from collections import OrderedDict
ordered_fieldnames = OrderedDict([('Name_Pinyin',None),('Name_CHN',None),('URL', None)])
header = csv.DictWriter(outfile, fieldnames=ordered_fieldnames)
header.writeheader()
wr = csv.writer(outfile)
wr.writerows(cadre_info)
outfile.close()
print "Cadre_list saved."
