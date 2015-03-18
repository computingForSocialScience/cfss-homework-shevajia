from flask import Flask, render_template, request, redirect, url_for
import pymysql
import pandas as pd
from igraph import *
import tempfile
import random, string

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

dbname="cped"
host="localhost"
user="root"
passwd="Thome1987"
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

app = Flask(__name__)

@app.route('/')
def make_index_resp():
    # this function just renders templates/index.html when
    # someone goes to http://127.0.0.1:5000/
    return(render_template('index.html'))

@app.route('/database/')
def make_database_resp():
    cur = db.cursor()
    sql = '''SELECT id, namePinyin, nameCHN FROM urllist'''
    cur.execute(sql)
    namelist = cur.fetchall()
    return render_template('database.html',namelist=namelist)

@app.route('/database/<id>')
def make_info_resp(id):
    cur = db.cursor()
    info_sql = '''SELECT urllist.id,
                         namePINYIN, 
                         nameCHN, 
                         url, 
                         sex, 
                         edu,  
                         birthdate,
                         deathdate,
                         party 
                  FROM urllist, infolist
             	  WHERE infolist.id = ('%s') AND urllist.id = infolist.id '''% (id)
    cur.execute(info_sql)
    info = cur.fetchall()[0]
    edu_sql = '''SELECT startdate,
                         enddate, 
                         subject_type, 
                         alma_mater
                  FROM edulist
             	  WHERE id = ('%s')'''% (id)
    cur.execute(edu_sql)
    edu = cur.fetchall()
    exp_sql = '''SELECT startyear,
                         startmonth,
                         endyear,
                         endmonth, 
                         description,
                         pro
                  FROM explist, explist_pro
             	  WHERE id = ('%s') AND explist.expId = explist_pro.expId'''% (id)
    cur.execute(exp_sql)
    exp = cur.fetchall()
    return render_template('info.html',info=info, edu=edu, exp=exp)


@app.route('/network/',methods=['GET','POST'])
def get_network():
    if request.method == 'GET':
        # This code executes when someone visits the page.
        return(render_template('getnetwork.html'))
    elif request.method == 'POST':
        #this code executes when someone fills out the form
        endyear = int(request.form['endyear'])
        startyear = int(request.form['startyear'])
        flows = read('flows_full.gml')
        flows.delete_edges(flows.es.select(year_gt=endyear))
        flows.delete_edges(flows.es.select(year_lt=startyear))
        flows.simplify(combine_edges=sum)
        layout = flows.layout_fruchterman_reingold()
        plotPng = randomword(10)
        plot(flows, "static/temp/" + plotPng + ".png", vertex_label = flows.vs['name'], vertex_size = 40, vertex_label_size =10, edge_curved = 0.2, layout = layout)
        return render_template('getnetwork.html', plotPng = plotPng)

if __name__ == '__main__':
    app.debug=True
    app.run()