import csv
import pandas as pd
import goslate
import cPickle

f_exp = open("Word_Exp_Pro_NonM_CCP_after1980.csv")
exp = csv.reader(f_exp)
exp_header = exp.next()


exps = []
for row in exp:
    id,start_year,start_month,end_year,end_month,province1,province2 = row
    if start_year == "":
        start_year_int = 0
    else:
        start_year_int = int(start_year)
    if start_month == "":
        start_month_int = 6
    else:
        start_month_int = int(start_month)
    if end_year == "now":
        end_year_int = 9999
    else:
        end_year_int = int(end_year)
    if end_month == "":
        end_month_int = 0
    else:
        end_month_int = int(end_month)
    if province1 == '\xe9\x87\x8d\xe6\x85\xb6\xe5\xb8\x82\xef\xbc\x88\xe6\xaa\xa2\xe6\x9f\xa5\xef\xbc\x89': #重慶市的問題
        province1 = '\xe9\x87\x8d\xe6\x85\xb6\xe5\xb8\x82'
    exps.append((id,start_year_int,start_month_int,end_year_int,end_month_int,province1,province2))

exps_pro = []
for exp in exps:
    if exp[-2]:
        exps_pro.append(exp)
    else:
        pass

id = 0
end_year = 0
pro = ""
flows = []
for exp in exps_pro:
    if exp[-1] == "":
        if exp[0] == id:
            if abs(exp[1] - end_year) <= 1:
                if exp[5] != pro:
                    flow = (pro, exp[5],id, exp[1], exp[2])
                    pro = exp[5]
                    end_year = exp[3]
                    flows.append(flow)
                else:
                    end_year = max(exp[3], end_year)
            else: 
                if exp[5] != pro:
                    pro = exp[5]
                    end_year = exp[3]
                else: 
                    end_year = max(exp[3],end_year)

        else:
            id = exp[0]
            end_year = exp[3]
            pro = exp[5]
    else:
        year = (exp[3] + exp[1])/2
        flows.append((exp[-1], exp[-2], exp[0], year, 6))
        if exp[0] == id:
            if abs(exp[1] - end_year) <= 1:
                if exp[-1] != pro:
                    flow = (pro, exp[-1], id, exp[1], exp[2])
                    pro = exp[5]
                    end_year = exp [3]
                    flows.append(flow)
                else:
                    end_year = exp[3]
                    pro = exp[5]
            else: 
                pro = exp[5]
                end_year = exp[3]
        else:
            id = exp[0]
            end_year = exp[3]
            pro = exp[5]

import json
f = open('Pro_Network.json','wb')
json.dump(flows,f)
f.close()

f = open('rev_dict_pro.pkl','r')
rev_dict_pro = cPickle.load(f)
f.close()

gs = goslate.Goslate()
flows_en = []
i = 0
for flow in flows:
    print i
    if flow[0] == '陝西省':
        sender = 'Shaanxi'
    else:
        sender = gs.translate(rev_dict_pro[flow[0]], "en").split()[0]
        if sender == 'Inner':
            sender = 'Inner Mongolia'
    if flow[1] == '陝西省':
        receiver = 'Shaanxi'
    else:
        receiver = gs.translate(rev_dict_pro[flow[1]], "en").split()[0]
        if receiver == 'Inner':
            receiver = 'Inner Mongolia' 
    flows_en.append((sender, receiver, flow[2], flow[3], flow[4]))
    i = i + 1

flows_df_en = pd.DataFrame(flows_en, columns = ["sender", "receiver", "elite id", "year", "month"])
flows_df_en.to_csv("flows_en.csv", index = False)