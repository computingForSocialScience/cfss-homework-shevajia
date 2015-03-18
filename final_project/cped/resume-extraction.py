import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re
import sys
import csv
import urllib
import os

folder = os.getcwd()
folderpath = folder + '/portraits' 
if not os.path.exists(folderpath): os.makedirs(folderpath)

def get_cadre_info(url):
    req = requests.get(url)
    src = req.text
    soup = BeautifulSoup(src)
    cadre_info = {}
    row = soup.select('h1.title')[0]
    cadre_info['name_CHN'] = row.text
    id_row = soup.select('div.pane-content')[0].div
    id = id_row['id'].split('-')[-1]
    cadre_info['id'] = id
    if len(soup.select('img')) < 2:
        row_correction = 1
    else: 
        pic_row = soup.select('img')[1]
        pic_url = pic_row['src']
        folder = os.getcwd()
        urllib.urlretrieve(pic_url, folder + '/portraits/' + id +'.jpg')
        row_correction = 0
    rows = soup.select('tr > td')
    rowData = [cell.text for cell in rows]
    cadre_info['name_PINYIN'] = rowData[1 - row_correction].strip()
    cadre_info['sex'] = rowData[2 - row_correction].strip()
    cadre_info['ethnicity'] = rowData[4 - row_correction].strip()
    cadre_info['edu'] = rowData[5 - row_correction].strip()
    cadre_info['studying_abroad'] = rowData[6 - row_correction].strip()
    cadre_info['studying_abroad_country'] = rowData[7 - row_correction].strip()
    cadre_info['birthdate'] = rowData[8 - row_correction].strip()
    cadre_info['deathdate'] = rowData[9 - row_correction].strip()
    cadre_info['ancestral_hometown'] = rowData[10 - row_correction].strip()
    cadre_info['professional_title'] = rowData[11 - row_correction].strip()
    cadre_info['date_of_starting_to_work'] = rowData[12 - row_correction].strip()
    cadre_info['birthplace'] = rowData[13 - row_correction].strip()
    cadre_info['party'] = rowData[14 - row_correction].strip()
    cadre_info['date_of_joining_the_party'] = rowData[15 - row_correction].strip()
    cadre_info['CYL'] = rowData[16 - row_correction].strip()
    cadre_info['special_relationship'] = rowData[17 - row_correction].strip()
    cadre_info['notes'] = rowData[18 - row_correction].strip().replace('\n', '')
    
    cadre_edu = []
    current_positions = []
    past_positions = []
    exp_rows = soup.select('tbody > tr')
    for exp_row in exp_rows:
        exp_rowData = [cell.text for cell in exp_row.select('td')]
        if len(exp_rowData) == 4:
            start_date = exp_rowData[0].strip().encode('utf-8')
            end_date = exp_rowData[1].strip().encode('utf-8')
            subject_type = exp_rowData[2].strip().encode('utf-8')
            alma_mater = exp_rowData[3].strip().encode('utf-8')
            cadre_edu.append((id.encode('utf-8'), cadre_info['name_CHN'].encode('utf-8'),start_date, end_date, subject_type, alma_mater))
        elif len(exp_rowData) == 2:
            start_date = exp_rowData[0].strip().encode('utf-8')
            position = exp_rowData[1].strip().encode('utf-8')
            current_positions.append((id.encode('utf-8'), cadre_info['name_CHN'].encode('utf-8'),start_date,'now', position))
        elif len(exp_rowData) == 3:
            start_date = exp_rowData[0].strip().encode('utf-8')
            end_date = exp_rowData[1].strip().encode('utf-8')
            position = exp_rowData[2].strip().encode('utf-8')
            past_positions.append((id.encode('utf-8'), cadre_info['name_CHN'].encode('utf-8'),start_date, end_date, position))
    
    pages = soup.find(title= u'到最後一頁') #potential problem
    if pages == None:
        pass
    else:
        last_page = int(pages['href'].split("=")[-1])
        for i in range(1, (last_page + 1)):
            additional_page_url = url + '?page=' + str(i)
            req = requests.get(additional_page_url)
            src = req.text
            soup = BeautifulSoup(src)
            exp_rows = soup.select('tbody > tr')
            for exp_row in exp_rows:
                exp_rowData = [cell.text for cell in exp_row.select('td')]
                if len(exp_rowData) == 4:
                    start_date = exp_rowData[0].strip()
                    end_date = exp_rowData[1].strip()
                    subject_type = exp_rowData[2].strip()
                    alma_mater = exp_rowData[3].strip()
                    cadre_edu.append((start_date, end_date, subject_type, alma_mater))
                elif len(exp_rowData) == 2:
                    start_date = exp_rowData[0].strip()
                    position = exp_rowData[1].strip()
                    current_positions.append((start_date, position))
                elif len(exp_rowData) == 3:
                    start_date = exp_rowData[0].strip()
                    end_date = exp_rowData[1].strip()
                    position = exp_rowData[2].strip()
                    past_positions.append((start_date, end_date, position))
    
    cadre_data = [cadre_info, cadre_edu, current_positions, past_positions] 
    return cadre_data


from collections import OrderedDict

f_cadre_list = open('cadre_list.csv', 'r')
f_cadre_info_list = open('cadre_info_list.csv', 'w')
f_cadre_edu_list = open('cadre_edu_list.csv', 'wb')
wr_edu = csv.writer(f_cadre_edu_list)
f_cadre_exp_list = open('cadre_exp_list.csv', 'wb')
wr_exp = csv.writer(f_cadre_exp_list)

cadre_list = csv.reader(f_cadre_list)
cadre_list_header = cadre_list.next()
url_list = []
for row in cadre_list:
    url = row[2]
    url_list.append(url)
num = len (url_list)

f_cadre_info_list.write(u'id,name_CHN,name_PINYIN,sex,ethnicity,edu,studying_abroad,studying_abroad_country,birthdate,deathdate,ancestral hometown,professional title,date of starting to work,birthplace,party,date of joining the party,CYL,special relationships,notes\n')

ordered_fieldnames_edu = OrderedDict([('id',None),('name_CHN',None),('start date', None),('end date', None),('subject type', None),('alma mater', None)])
header_edu = csv.DictWriter(f_cadre_edu_list, fieldnames=ordered_fieldnames_edu)
header_edu.writeheader()

ordered_fieldnames_exp = OrderedDict([('id',None),('name_CHN',None),('start date', None),('end date', None),('position', None)])
header_exp = csv.DictWriter(f_cadre_exp_list, fieldnames=ordered_fieldnames_exp)
header_exp.writeheader()

print 'Starting to extract resumes.'
i = 0
j = 0
for url in url_list[:10]:
    cadre_data = get_cadre_info(url)
    cadre_info = cadre_data[0]
    cadre_edu = cadre_data[1]
    cadre_current_positions = cadre_data[2]
    cadre_past_positions = cadre_data[3]
    
    f_cadre_info_list.write(cadre_info['id'] + ',')
    f_cadre_info_list.write(cadre_info['name_CHN'].encode('utf8') + ',')
    f_cadre_info_list.write(cadre_info['name_PINYIN'].encode('utf8') + ',')
    f_cadre_info_list.write(cadre_info['sex'].encode('utf8') + ',')
    f_cadre_info_list.write(cadre_info['ethnicity'].encode('utf8') + ',')
    f_cadre_info_list.write(cadre_info['edu'].encode('utf8') + ',')
    f_cadre_info_list.write(cadre_info['studying_abroad'].encode('utf8') + ',')
    f_cadre_info_list.write(cadre_info['studying_abroad_country'].encode('utf8') + ',')
    f_cadre_info_list.write(cadre_info['birthdate'].encode('utf8') + ',')
    f_cadre_info_list.write(cadre_info['deathdate'].encode('utf8') + ',')
    f_cadre_info_list.write(cadre_info['ancestral_hometown'].encode('utf8') + ',')
    f_cadre_info_list.write(cadre_info['professional_title'].encode('utf8') + ',')
    f_cadre_info_list.write(cadre_info['date_of_starting_to_work'].encode('utf8') + ',')
    f_cadre_info_list.write(cadre_info['birthplace'].encode('utf8') + ',')
    f_cadre_info_list.write(cadre_info['party'].encode('utf8') + ',')
    f_cadre_info_list.write(cadre_info['date_of_joining_the_party'].encode('utf8') + ',')
    f_cadre_info_list.write(cadre_info['CYL'].encode('utf8') + ',')
    f_cadre_info_list.write(cadre_info['special_relationship'].encode('utf8') + ',')
    f_cadre_info_list.write(cadre_info['notes'].encode('utf8') + '\n')
    
    wr_edu.writerows(cadre_edu)
    
    wr_exp.writerows(cadre_past_positions)
    wr_exp.writerows(cadre_current_positions)
    
    i = i + 1
    percent = float(i) /num
    print 'Row ' + str(i) + ' extracted.'
    if percent > 0.001 and j == 0:
        print '0.1 percent extracted.'
        j = 0.001
    elif percent > 0.01 and j == 0.001:
        print '1 percent extracted.'
        j = 0.01

print 'Extraction completed.'