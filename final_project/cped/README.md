# Notes on How to Replicate My Final Project

## Part 1: Web scraping

In this step, I web-scraped all CVs in the Chinese Political Elites Database (http://cped.nccu.edy.tw/) and saved them as csvs. By executing list-extraction.py, every elite's name and the url to his/her CV will be saved in cadre_list.csv. It takes approximately 40 mins. Then, resume-extraction.py will visit every url and extract all useful information which appears on that webpage. All biographical information is saved in cadre_info_list.csv. All educational experience is saved in cadre_edu_list.csv. All work experience is saved in cadre_exp_list.csv. The whole process takes approximately 4 hrs.

## Part 2: Province recognition

timeExtraction.py will first parse the starting date and ending date of every job experience and separate year and month. New information is saved in cadre_exp_list_1.1.csv as well as Exps.json. ParsingJobDesription_Pro.py will parse the description of each job experience and determine the provincial unit of that particular entry. Relevant information is saved in pro.csv.

## Part 3: Network extraction
Pro_Network_Extraction.py will extract inter-provincial networks from the csv saved in the previous step. (I used only a subset of the full data, i.e. CVs after 1980). Network data is saved in flows_en.csv.

## Part 4：Build a database
First, manually create a database called "cped" in MySQL. Then, build_database.py will create tables inside cped and save my data in it. 

## Part 5: Web presentation
Running app.py will enable a web presentation of the database. The website can also show the networks extracted. 


 