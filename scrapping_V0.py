#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 15:05:50 2019

@author: Ivan
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd 

#dataframe=pd.DataFrame(columns=['id','Title','Location','Company','Salary','Sponsored','Description'])
Id_ = []
Title = []
Location = []
Company = []
Salary = []
Sponsored = []
Job_desc= []

browser = webdriver.Chrome()

for i in range(0,1000,10):

    browser.get('https://www.indeed.fr/emplois?q=data+scientist&l=Paris&start='+str(i))
    browser.implicitly_wait(4)

    all_jobs=browser.find_elements_by_class_name('result')

    for job in all_jobs:
        result_html=job.get_attribute('innerHTML')
        soup=BeautifulSoup(result_html,'html.parser')
        
        id_= job.get_attribute('id')

        try:
            title=soup.find("a",class_="jobtitle").text.replace('\n','')
        except:
            title='None'

        try:
            location=soup.find(class_="location").text
        except:
            location='None'

        try:
            company=soup.find(class_="company").text.replace("\n","").strip()
        except:
            company='None'

        try:
            salary=soup.find(class_="salary").text.replace("\n","").strip()
        except:
            salary="None"

        try:
            sponsored=soup.find(class_="sponsoredGray").text
            sponsored="Sponsored"
        except:
            sponsored='Not Sponsored'

        sum_div=job.find_element_by_class_name("summary")
        try:
            sum_div.click()
            browser.implicitly_wait(4)
        except:
            close_button=browser.find_element_by_class_name('popover-x-button-close')
            close_button.click()
            browser.implicitly_wait(4)
            sum_div.click()
            browser.implicitly_wait(4)
            
        job_desc=browser.find_element_by_id('vjs-desc').text
        
        if id_ not in Id_:
            Id_.append(id_)
            Title.append(title)
            Location.append(location)
            Company.append(company)
            Salary.append(salary)
            Sponsored.append(sponsored)
            Job_desc.append(job_desc)
            
#pour lyon
browser = webdriver.Chrome()
for i in range(0,50,10):

    browser.get('https://www.indeed.fr/emplois?q=data+scientist&l=lyon&start='+str(i))
    browser.implicitly_wait(4)

    all_jobs=browser.find_elements_by_class_name('result')

    for job in all_jobs:
        result_html=job.get_attribute('innerHTML')
        soup=BeautifulSoup(result_html,'html.parser')
        
        id_= job.get_attribute('id')

        try:
            title=soup.find("a",class_="jobtitle").text.replace('\n','')
        except:
            title='None'

        try:
            location=soup.find(class_="location").text
        except:
            location='None'

        try:
            company=soup.find(class_="company").text.replace("\n","").strip()
        except:
            company='None'

        try:
            salary=soup.find(class_="salary").text.replace("\n","").strip()
        except:
            salary="None"

        try:
            sponsored=soup.find(class_="sponsoredGray").text
            sponsored="Sponsored"
        except:
            sponsored='Not Sponsored'

        sum_div=job.find_element_by_class_name("summary")
        try:
            sum_div.click()
            browser.implicitly_wait(4)
        except:
            close_button=browser.find_element_by_class_name('popover-x-button-close')
            close_button.click()
            browser.implicitly_wait(4)
            sum_div.click()
            browser.implicitly_wait(4)
            
        job_desc=browser.find_element_by_id('vjs-desc').text
        
        if id_ not in Id_:
            Id_.append(id_)
            Title.append(title)
            Location.append(location)
            Company.append(company)
            Salary.append(salary)
            Sponsored.append(sponsored)
            Job_desc.append(job_desc)
            
#pour lille            
for i in range(0,40,10):

    browser.get('https://www.indeed.fr/emplois?q=data+scientist&l=lille&start='+str(i))
    browser.implicitly_wait(4)

    all_jobs=browser.find_elements_by_class_name('result')

    for job in all_jobs:
        result_html=job.get_attribute('innerHTML')
        soup=BeautifulSoup(result_html,'html.parser')
        
        id_= job.get_attribute('id')

        try:
            title=soup.find("a",class_="jobtitle").text.replace('\n','')
        except:
            title='None'

        try:
            location=soup.find(class_="location").text
        except:
            location='None'

        try:
            company=soup.find(class_="company").text.replace("\n","").strip()
        except:
            company='None'

        try:
            salary=soup.find(class_="salary").text.replace("\n","").strip()
        except:
            salary="None"

        try:
            sponsored=soup.find(class_="sponsoredGray").text
            sponsored="Sponsored"
        except:
            sponsored='Not Sponsored'

        sum_div=job.find_element_by_class_name("summary")
        try:
            sum_div.click()
            browser.implicitly_wait(4)
        except:
            close_button=browser.find_element_by_class_name('popover-x-button-close')
            close_button.click()
            browser.implicitly_wait(4)
            sum_div.click()
            browser.implicitly_wait(4)
            
        job_desc=browser.find_element_by_id('vjs-desc').text
        
        if id_ not in Id_:
            Id_.append(id_)
            Title.append(title)
            Location.append(location)
            Company.append(company)
            Salary.append(salary)
            Sponsored.append(sponsored)
            Job_desc.append(job_desc)
            
#pour bordeaux

for i in range(0,40,10):

    browser.get('https://www.indeed.fr/emplois?q=data+scientist&l=bordeaux&start='+str(i))
    browser.implicitly_wait(4)

    all_jobs=browser.find_elements_by_class_name('result')

    for job in all_jobs:
        result_html=job.get_attribute('innerHTML')
        soup=BeautifulSoup(result_html,'html.parser')
        
        id_= job.get_attribute('id')

        try:
            title=soup.find("a",class_="jobtitle").text.replace('\n','')
        except:
            title='None'

        try:
            location=soup.find(class_="location").text
        except:
            location='None'

        try:
            company=soup.find(class_="company").text.replace("\n","").strip()
        except:
            company='None'

        try:
            salary=soup.find(class_="salary").text.replace("\n","").strip()
        except:
            salary="None"

        try:
            sponsored=soup.find(class_="sponsoredGray").text
            sponsored="Sponsored"
        except:
            sponsored='Not Sponsored'

        sum_div=job.find_element_by_class_name("summary")
        try:
            sum_div.click()
            browser.implicitly_wait(4)
        except:
            close_button=browser.find_element_by_class_name('popover-x-button-close')
            close_button.click()
            browser.implicitly_wait(4)
            sum_div.click()
            browser.implicitly_wait(4)
            
        job_desc=browser.find_element_by_id('vjs-desc').text
        
        if id_ not in Id_:
            Id_.append(id_)
            Title.append(title)
            Location.append(location)
            Company.append(company)
            Salary.append(salary)
            Sponsored.append(sponsored)
            Job_desc.append(job_desc)            
            
            
df = pd.DataFrame(list(zip(Id_, Title, Location, Company, Salary, Sponsored, Job_desc)),columns=['id','Title','Location','Company','Salary','Sponsored','Description'])

df.to_csv("offers_Data_scientist", index = False)

#CSV to SQL

from selenium import webdriver
import sqlalchemy
engine = sqlalchemy.create_engine('mysql+pymysql://root:__######___@localhost/Data_scientists')
import mysql.connector

mydb = mysql.connector.MySQLConnection(
    host='localhost',
    user='root',
    password='#######'
)

mycursor = mydb.cursor()

#mycursor.execute("CREATE DATABASE Data_scientists")

mydb = mysql.connector.MySQLConnection(
  host="localhost",
  user="root",
  passwd="#######",
  database="Data_scientists"
)

cursor = mydb.cursor()

query = 'CREATE TABLE offers(Id text(255), Title text(255), Location text(255), Company text(255), Salary text(255), Sponsored text(255), Description text(255))'
 

cursor.execute(query)

#df.to_sql(name='Data_scientists', con=engine, index=False, if_exists='append')

sql_select_Query = "SELECT * FROM Data_scientists.offers;"
cursor = mydb.cursor()
cursor.execute(sql_select_Query)
records = cursor.fetchall()

records