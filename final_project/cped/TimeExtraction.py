import unicodecsv as csv

f_exp = open("cadre_exp_list.csv")
exp = csv.reader(f_exp)

exps = []
for row in exp:
    id,name_CHN, start_date, end_date, job_description = row
    exps.append((id, name_CHN, start_date, end_date, job_description))

start_date = [row[2] for row in exps[1:]]

start_years = []
start_months = []
for row in start_date:
    row_split = row.split('/')
    if len(row_split) == 2:
        start_year = row_split[0].strip()
        start_month = row_split[1].strip()
    else:
        start_year = row_split[0].strip()
        start_month = ""
    start_years.append(start_year)
    start_months.append(start_month)

end_date = [row[3] for row in exps[1:]]
end_years = []
end_months = []
for row in end_date:
    row_split = row.split('/')
    if len(row_split) == 2:
        end_year = row_split[0].strip()
        end_month = row_split[1].strip()
    else:
        end_year = row_split[0].strip()
        end_month = ""
    end_years.append(end_year)
    end_months.append(end_month)

from io import open

outfile = open('cadre_exp_list_1.1.csv', 'w', encoding = 'utf8')
outfile.write(u'id,name_CHN,start date,start year,start month,end date,end year,end month,description\n')
num_rows = len(exps) - 1
for i in range(num_rows):
    line = exps[i+1][0] + u',' + exps[i+1][1] + u',' + exps[i+1][2] + u','+ start_years[i] +u',' + start_months[i] + u','+ exps[i+1][3] + u','+ end_years[i] + u',' + end_months[i] + u',"' + exps[i+1][4] + u'"\n'
    outfile.write(line) 
outfile.close() 


Exps = []
num_rows = len(exps) - 1
for i in range(num_rows):
    row = (exps[i+1][0], exps[i+1][1], exps[i+1][2], start_years[i], start_months[i], exps[i+1][3], end_years[i], end_months[i], exps[i+1][4])
    Exps.append(row)

import json
# dump into a file
f = open('Exps.json','wb')
json.dump(Exps,f)
f.close()