import pandas as pd

from selenium import webdriver

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException

from bs4 import BeautifulSoup

from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client.indeed_db
job_offers_collec = db.job_offers

try:
    salary_df = pd.read_csv('salary_indeed.csv')
except FileNotFoundError:
    salary_df = pd.DataFrame(columns=['_id', 'Title', 'Company', 'Location',
                                      'Salary', 'Description', 'Date',
                                      'Job_Search', 'Department_Search'])

driver = webdriver.Chrome()

professions = ["title%3A+data", "informatique+title%3A+développeur"]
# 75 = Paris ; Gironde = Bordeaux ; Rhône = Lyon
# Loire-Atlantique = Nantes ; Haute-Garonne = Toulouse
# 75 à la place de Paris car ce dernier donne Montreuil par ex.
departments = ["75", "Gironde", "Rhône", "Loire-Atlantique", "Haute-Garonne"]

for profession in professions:
    for dpt in departments:
        url = 'https://www.indeed.fr/jobs?q={}&l={}&sort=date'.format(profession, dpt)
        driver.get(url)
        driver.implicitly_wait(4)

        first_page = True
        never_seen = True

        while never_seen:
            try:
                all_jobs = driver.find_elements_by_class_name('result')

                for job in all_jobs:
                    result_html = job.get_attribute('innerHTML')
                    soup = BeautifulSoup(result_html, 'lxml')

                    id_ = job.get_attribute('id')
                    if id_ in salary_df._id:
                        never_seen = False
                        break

                    date = soup.find(class_="date")
                    if date is not None:
                        date = date.text

                    location = soup.find(class_="location")
                    if location is not None:
                        location = location.text

                    company = soup.find(class_="company")
                    if company is not None:
                        company = company.text

                    salary = soup.find(class_="salary")
                    if salary is not None:
                        salary = salary.text

                    sum_div = job.find_element_by_class_name("summary")
                    sum_div.click()
                    driver.implicitly_wait(4)

                    job_desc = driver.find_element_by_id('vjs-desc').text
                    title = driver.find_element_by_id('vjs-jobtitle').text

                    if salary_df[(salary_df["Title"] == title)
                                 & (salary_df["Company"] == company)
                                 & (salary_df["Location"] == location)
                                 & (salary_df["Description"] == job_desc)].empty:
                        if profession == 'title%3A+data':
                            job_search = "Data"
                        else:
                            job_search = "Développeur"

                        job_offer = {'_id': id_,
                                     'Title': title,
                                     'Company': company,
                                     'Location': location,
                                     'Salary': salary,
                                     'Description': job_desc,
                                     'Date': date,
                                     'Job_Search': job_search,
                                     'Department_Search': dpt}

                        # Insert into the pandas DataFrame
                        salary_df = salary_df.append(job_offer,
                                                     ignore_index=True)
                        # Insert into the MongoDB database
                        job_offers_collec.insert_one(job_offer)
                    else:
                        continue

                # Click on the "Suivant" button :
                try:
                    if first_page:
                        driver.find_element_by_class_name('np').click()
                        first_page = False
                    else:
                        try:
                            driver.find_elements_by_class_name('np')[1].click()
                        except IndexError:
                            # Last page, no "Suivant" button
                            break
                except NoSuchElementException:
                    break

            except ElementClickInterceptedException:
                # If there is a popup, close it :
                close_popup_button = driver.find_element_by_class_name('popover-x-button-close')
                close_popup_button.click()
                driver.implicitly_wait(4)

salary_df.to_csv('salary_indeed.csv', index=False)
