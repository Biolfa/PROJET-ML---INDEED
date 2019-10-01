from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import pandas as pd 
import requests 
from pymongo import MongoClient

# Liste des jobs et villes

jobs = ['data+scientist', 'developpeur+full+stack']
towns = ['Besancon', 'Toulouse', 'Nantes', 'Bordeaux']

def scrapping_links(position, city):

    links = []
    browser = webdriver.Chrome()
    for job in position:
        for town in city:
            url = 'https://www.indeed.fr/emplois?q=title%3A+{}&l={}&radius=5&sort=date'.format(job, town)
            browser.get(url)
            number = 0
            while True:
                try:
                    title = browser.find_elements_by_class_name('jobtitle')
                    [links.append(x.get_attribute('href')) for x in title]
                    if number == 1 :
                        browser.find_elements_by_class_name('np')[1].click()
                    else:
                        browser.find_element_by_class_name('np').click()
                        number = 1
                except NoSuchElementException:
                    number = 0
                    break
                except IndexError:
                    break
                except ElementClickInterceptedException:
                    close_button=browser.find_element_by_class_name('popover-x-button-close')
                    close_button.click()


def scrapping_jobs(url):
    client = MongoClient()
    db = client.indeed_db
    job_offers = db.job_offers

    for link in url:
        open_url = requests.get(link)
        soup = BeautifulSoup(open_url.content, 'lxml')
        job_offer={
            "id_indeed": ObjectId(id_),
            "Title": title,
            "Location": location,
            "Date": date,
            "Company": company,
            "Salary": salary,
            "Job_desc": job_desc
        }
        
