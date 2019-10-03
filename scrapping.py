from selenium import webdriver

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException

from bs4 import BeautifulSoup


driver = webdriver.Chrome()

ids = []
dates = []
job_titles = []
locations = []
companies = []
salaries = []
descriptions = []

professions = ["title%3A+data", "informatique+title%3A+développeur"]
cities = ["75", "Gironde", "Rhône", "Loire-Atlantique", "Haute-Garonne"]

for profession in professions:
    for city in cities:
        url = 'https://www.indeed.fr/jobs?q={}&l={}&sort=date'.format(profession, city)
        driver.get(url)
        page = 1

        while True:
            try:
                all_jobs = driver.find_elements_by_class_name('result')

                for job in all_jobs:
                    result_html = job.get_attribute('innerHTML')
                    soup = BeautifulSoup(result_html, 'lxml')

                    id_ = job.get_attribute('id')

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

                    if id_ not in ids:
                        ids.append(id_)
                        dates.append(date)
                        job_titles.append(title)
                        locations.append(location)
                        companies.append(company)
                        salaries.append(salary)
                        descriptions.append(job_desc)

                # Click on the "Suivant" button :
                try:
                    if page == 1:
                        driver.find_element_by_class_name('np').click()
                        page = 0
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
