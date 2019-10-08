
######################################## Import les bibliotheques ######################################## 

import pandas as pd
import numpy as np 
import string
import re

df = pd.read_csv('partial_scraping.csv')


######################################## Traitement des donnees ########################################

# Lower letters

def lower_data(dataset):
    dataset['Description'] = dataset['Description'].str.lower()
    dataset['Title'] = dataset['Title'].str.lower()
    dataset['Company'] = dataset['Company'].str.lower()
    return dataset

df = lower_data(df)

def split_salary(row):
    salary = row["Salary"]
    if salary != 'None':
        if "-" in salary:
            split = salary.split("-")
            salary_min = split[0]
            salary_max = split[1]
        else:
            salary_min = salary
            salary_max = salary

        row["salary_min"] = salary_min.replace("€","").replace("par mois","").replace("par semaine","").replace("par an","").replace("\xa0","")
        row["salary_max"] = salary_max.replace("€","").replace("par mois","").replace("par semaine","").replace("par an","").replace("\xa0","")

        if "mois" in row["Salary"]:
            row["salary_min"] = int(row["salary_min"])*12
            row["salary_max"] = int(row["salary_max"])*12

        if "semaine" in row["Salary"]:
            row["salary_min"] = int(row["salary_min"])*52
            row["salary_max"] = int(row["salary_max"])*52
    else:
        regex_salary = re.findall('\d+ \d+[€]|\d+k€|\d+[.]\d+k€|\d+[.]\d+K€|\d+K€|\d+ \d+[.]\d+[€]|\d+[,]\d+[.]\d+[€]|\d+[,]\d+[€]|\d+€|\d+ \d+[,]\d+[€]', row['Description'])
        if regex_salary != []:
            row['Salary'] = list(regex_salary)
            if len(regex_salary) > 1 :
                if 'k' in regex_salary[0] or 'k' in regex_salary[1] or 'K' in regex_salary[0] or 'K' in regex_salary[1]:
                    row['salary_min'] = int(regex_salary[0].replace("k", "").replace("€","").replace("\xa0","").replace(" ","").replace(",00","")) * 1000
                    row['salary_max'] = int(regex_salary[1].replace("k", "").replace("€","").replace("\xa0","").replace(" ","").replace(",00","")) * 1000
                else:
                    regex_salary_min = int(regex_salary[0].replace("€","").replace("\xa0","").replace(" ","").replace(",00",""))
                    regex_salary_max = int(regex_salary[1].replace("€","").replace("\xa0","").replace(" ","").replace(",00",""))
                    if regex_salary_min < 140 and regex_salary_max < 140:
                        # Taux horaire
                        row['salary_min'] = regex_salary_min * 35 * 52
                        row['salary_max'] = regex_salary_max * 35 * 52
                    elif regex_salary_min < 2000 and regex_salary_min > 500 and regex_salary_max < 2000 and regex_salary_max > 500:
                        # Taux mensuel
                        row['salary_min'] = regex_salary_min * 12 
                        row['salary_max'] = regex_salary_max * 12
                    elif regex_salary_min < 500 and regex_salary_min > 140 and regex_salary_max < 500 and regex_salary_max > 140:
                        # Taux journalier
                        row['salary_min'] = regex_salary_min * 5 * 52 
                        row['salary_max'] = regex_salary_max * 5 * 52
                    else:
                        # Taux annuel
                        row['salary_min'] = regex_salary_min  
                        row['salary_max'] = regex_salary_max 
                        
            
            else:
                if 'k' in regex_salary[0] or 'K' in regex_salary[0]:
                    regex_salary = int(regex_salary[0].replace("k", "").replace("€","").replace("\xa0","").replace(" ","").replace(",00",".")) * 1000
                    row['salary_min'] = regex_salary
                    row['salary_max'] = regex_salary
                else:
                    regex_salary = int(regex_salary[0].replace("€","").replace("\xa0","").replace(" ","").replace(",00",""))
                    if regex_salary < 140 :
                        row['salary_min'] = regex_salary * 35 * 52 
                        row['salary_max'] = regex_salary * 35 * 52
                    elif regex_salary < 2000 and regex_salary > 500 :
                        row['salary_min'] = regex_salary * 12
                        row['salary_max'] = regex_salary * 12
                    elif regex_salary > 140 and regex_salary < 500:
                        row['salary_min'] = regex_salary * 5 * 52
                        row['salary_max'] = regex_salary * 5 * 52

        else:
            row['Salary'] = 'None'
            row['salary_min'] = 0
            row['salary_max'] = 0
        
    return row

    df = df.apply(split_salary, axis=1)

def add_contracts(dataset):
    dataset['Contrat'] = ''
    for i in range(len(dataset['Title'])):
        keyword = re.findall('cdi|cdd|free-lance|free lance|freelance|independant|stage|internship|alternance|apprenticeship', dataset['Title'][i])
        if keyword == []:
            keyword = re.findall('cdi|cdd|free-lance|free lance|freelance|independant|stage|internship|alternance|apprenticeship', dataset['Description'][i])
            if keyword == []:
                 dataset['Contrat'][i] = 'None'

        if dataset['Contrat'][i] != 'None':
            if 'cdi' in keyword:
                dataset['Contrat'][i] = 'CDI'
            elif 'cdd' in keyword:
                dataset['Contrat'][i] = 'CDD'
            elif 'free lance' in keyword or 'freelance' in keyword or 'free-lance' in keyword:
                dataset['Contrat'][i] = 'Free Lance'
            elif 'stage' in keyword or 'internship' in keyword:
                dataset['Contrat'][i] = 'Stage'
            elif 'alternance' in keyword or 'apprenticeship' in keyword:
                dataset['Contrat'][i] = 'Alternance'
            elif 'cdi' in keyword and len(keyword) > 1:
                dataset['Contrat'][i] = 'CDI'

    return dataset

add_contracts(df)

def add_statut(dataset):
    dataset['Statut'] = ''
    for i in range(len(dataset['Title'])):
        statut_word = re.findall('junior|senior|confirmé|débutant|experimenté|expérience significative', dataset['Title'][i])
        if statut_word == []:
            statut_word = re.findall('junior|senior|confirmé|débutant|experimenté|expérience significative', dataset['Description'][i])
            if statut_word == []:
                dataset['Statut'][i] = 'None'
        if dataset['Statut'][i] != 'None':
            if 'junior' in statut_word or df['Contrat'][i] == 'Stage':
                dataset['Statut'][i] = 'Junior'
            elif 'senior' in statut_word:
                dataset['Statut'][i] = 'Senior'
            elif 'confirmé' in statut_word or 'experimenté' in statut_word or 'expérience significative' in statut_word:
                dataset['Statut'][i] = 'Confirmé'
            else : 
                if statut_word[0] == 'junior' or df['Contrat'][i] == 'Stage':
                    dataset['Statut'][i] = 'Junior'
                elif statut_word[0] == 'senior':
                    dataset['Statut'][i] = 'Senior'
                elif statut_word[0] == 'confirmé' or statut_word[0] == 'experimenté' or statut_word[0] == 'expérience significative':
                    dataset['Statut'][i] = 'Confirmé'

    return dataset

add_statut(df)

def competences(dataset):
    dataset['python'] = 0
    dataset['Machine Learning'] = 0
    dataset['Java'] = 0
    for i in range(len(dataset['Description'])):
        key_word = re.findall('python|java|machine learning', dataset['Description'][i])
        if 'python' in key_word:
            dataset['python'][i] = 1
        elif 'java' in key_word:
            dataset['Java'][i] = 1
        elif 'machine learning' in key_word:
            dataset['Machine Learning'][i] = 1 
    return dataset
    
competences(df)