import pymysql
import csv
import goslate
import cPickle
import json
dbname="cped"
host="localhost"
user="root"
passwd="Thome1987"
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

cur = db.cursor()
sql_create_urllist ='''CREATE TABLE IF NOT EXISTS urllist 
                    (id INTEGER,
                    namePINYIN VARCHAR(256), 
                    nameCHN VARCHAR(256), 
                    url VARCHAR(256),
                    PRIMARY KEY (id));'''
sql_create_infolist ='''CREATE TABLE IF NOT EXISTS infolist 
                         (id INTEGER, 
                         sex VARCHAR(128), 
                         ethnicity VARCHAR(256),
                         edu VARCHAR(256), 
                         studying_abroad VARCHAR(256),
                         studying_abroad_country VARCHAR(256),
                         birthdate VARCHAR(256),
                         deathdate VARCHAR(256),
                         ancestral_hometown VARCHAR(256),
                         professional_title VARCHAR(256),
                         date_of_starting_to_work VARCHAR(256),
                         birthplace VARCHAR(256),
                         party VARCHAR(256),
                         date_of_joining_the_party VARCHAR(256),
                         CYL VARCHAR(256),
                         special_relationships VARCHAR(256),
                         notes VARCHAR(1024),
                         PRIMARY KEY (id));'''
sql_create_edulist = '''CREATE TABLE IF NOT EXISTS edulist 
                        (id INTEGER, 
                        eduOrder INTEGER,
                        startdate VARCHAR(256),
                        enddate VARCHAR(256),
                        subject_type VARCHAR(256),
                        alma_mater VARCHAR(1024));'''
sql_create_explist = '''CREATE TABLE IF NOT EXISTS explist
                        (expID INTEGER PRIMARY KEY AUTO_INCREMENT,
                        id INTEGER,
                        expOrder INTEGER,
                        startyear VARCHAR(128),
                        startmonth VARCHAR(128),
                        endyear VARCHAR(128),
                        endmonth VARCHAR(128),
                        description VARCHAR(1024)
                        );'''
sql_create_explist_pro = '''CREATE TABLE IF NOT EXISTS explist_pro
                        (expID INTEGER PRIMARY KEY AUTO_INCREMENT,
                        pro VARCHAR(128)
                        );'''
cur.execute(sql_create_urllist)
cur.execute(sql_create_infolist)
cur.execute(sql_create_edulist)
cur.execute(sql_create_explist)
cur.execute(sql_create_explist_pro)

f_cadre_list = open('cadre_list.csv', 'r')
cadre_list = csv.reader(f_cadre_list)
cadre_list_header = cadre_list.next()
url_list = []
for row in cadre_list:
    url = row[2]
    id = int(url.split('/')[-1])
    namePINYIN = row[0]
    nameCHN = row[1]
    url_list.append((id, namePINYIN, nameCHN, url))

sql_insert_urllist = '''INSERT INTO urllist 
                     (id, namePINYIN, nameCHN, url)
                     VALUES
                     (%s, %s, %s, %s)'''
cur.executemany(sql_insert_urllist, url_list)
db.commit()


from io import open
f_info_list = open('cadre_info_list.csv', 'r', encoding = 'utf8')

info = []

i = 0
for item in f_info_list:
    if i == 0:
        i = i + 1
    else:
        row = item.split(u',')
        id =  int(row[0])
        if row[3] == u'男':
            sex = 'M'
        elif row[3] == u'女':
            sex = 'F'
        else:
            sex= ''
        if row[4] == u'漢族':
            ethnicity = 'Han'
        elif row[4]:
            ethnicity = 'Other'
        else: 
            ethnicity = ''
        if row[5] == u'大學本科':
            edu = "Bachelor's Degree"
        elif row[5] == u'大學專科':
            edu = "Associate Degree"
        elif row[5] == u'研究生':
            edu = "Postgraduate" 
        elif row[5] == u'中學以下':
            edu = "Middle School or Below"
        else:
            edu = row[5]
        studying_abroad = row[6]
        studying_abroad_country = row[7]
        birthdate = row[8]
        deathdate = row[9]
        ancestral_hometown = row[10]
        professional_title = row[11]
        date_of_starting_to_work = row[12]
        birthplace = row[13]
        if row[14] == u'中國共產黨':
            party = 'CCP'
        elif row[14] == u'非中國共產黨':
            party = 'Non-CCP'
        else:
            party = ""
        date_of_joining_the_party = row[15]
        if row[16] == u'是':
            CYL = 'Yes'
        elif row[16] == u'否':
            CYL = 'No'
        else:
            CYL = ''
        special_relationships = row[17]
        notes = row[18]
        info.append((id, sex, ethnicity, edu, studying_abroad, studying_abroad_country, birthdate, deathdate, ancestral_hometown, professional_title, date_of_starting_to_work, birthplace, party, date_of_joining_the_party, CYL, special_relationships, notes))
        i = i + 1

sql_insert_infolist = '''INSERT INTO infolist 
                     (id, sex, ethnicity, edu, studying_abroad, studying_abroad_country, birthdate, deathdate, ancestral_hometown, professional_title, date_of_starting_to_work, birthplace, party, date_of_joining_the_party, CYL, special_relationships, notes)
                     VALUES
                     (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
cur.executemany(sql_insert_infolist, info)
db.commit()

f_info_list = open('cadre_edu_list.csv', 'r', encoding = 'utf8')

edu = []
id = 0
order = 0
i = 0
for row in f_info_list:
    if i == 0:
        i = i + 1
    else:
        items = row.split(u',')
        if int(items[0]) == id:
            order = order + 1
            startdate = items[2]
            enddate = items[3]
            subject_type = items[4]
            alma_mater = items[5]
        else:
            id = int(items[0])
            order = 1
            startdate = items[2]
            enddate = items[3]
            subject_type = items[4]
            alma_mater = items[5]
        edu.append((id, order, startdate, enddate, subject_type, alma_mater))
        i = i + 1

sql_insert_edulist = '''INSERT INTO edulist 
                     (id, eduOrder, startdate, enddate, subject_type, alma_mater)
                     VALUES
                     (%s, %s, %s, %s, %s, %s)'''
cur.executemany(sql_insert_edulist, edu)
db.commit()

f = open('Exps.pkl','rb')
exps = cPickle.load(f)
f.close()

exp_list = []
id= 0
order = 0
for exp in exps:
    if int(exp[0]) == id:
        order = order + 1
    else:
        id = int(exp[0])
        order = 1
    exp_list.append((id, order, exp[3], exp[4], exp[6], exp[7], exp[8]))

sql_insert_explist = '''INSERT INTO explist 
                     (id, expOrder, startyear, startmonth, endyear, endmonth, description)
                     VALUES
                     (%s, %s, %s, %s, %s, %s, %s)'''
cur.executemany(sql_insert_explist, exp_list)
db.commit()

f = open('pros.json', 'r')
pros = json.load(f)
f.close()

pro = []
for row in pros:
    if row:
        pro.append(row[0])
    else:
        pro.append(u"")

sql_insert_explist_pro = '''INSERT INTO explist_pro 
                     (pro)
                     VALUES
                     (%s)'''
cur.executemany(sql_insert_explist_pro, pro)
db.commit()