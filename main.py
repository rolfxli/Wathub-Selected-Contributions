import os
import json
import requests

from bs4 import BeautifulSoup
from typing import List, Dict

BASE_URL = 'https://uwaterloo.ca/important-dates/important-dates/list'
DIRECT_URL = 'https://uwaterloo.ca/important-dates/important-dates/list?date=Today&=All&page='

ALL_DATES_BASE_URL = 'https://uwaterloo.ca/important-dates/important-dates/list?academic_term=All&academic_year='
ACADEMIC_YEAR_VALUE='214'
ALL_DATES_PAGE='&audience=All&combine=&date=Any&type=All&=All&page='
ALL_DATES='&audience=All&combine=&date=Any&type=All&=All'

def load_pages(url: str, count: int, year: int):
    #year_2018_2019 = 188
    #year_2019_2020 = 214
    #year_2020_2021 = 229
    baseUrl = ALL_DATES_BASE_URL
    academicYear = year
    baseEndUrl = ALL_DATES
    firstUrl = baseUrl + academicYear + baseEndUrl
    redirectionUrl = "https://uwaterloo.ca"

    important_dates = []
    #print(count)
    for page in range(count):
        final_url = ""
        if (page == 0):
            final_url = firstUrl
        else:
            final_url = url + str(page)
        #print(final_url)

        page = requests.get(final_url)
        soup = BeautifulSoup(page.content, "html.parser")
        #events = soup.find_all('tbody')
        #print(events)
        evens = soup.find_all(class_="even")
        #print (evens[0])
        count = 0
        for even in evens:
            hrefs = even.find_all('a')
            title = even.find(class_="views-field views-field-title-1").text.strip()
            titleHref = redirectionUrl + str(hrefs[0].get('href'))
            description = even.find(class_="views-field views-field-field-uw-imp-dates-description").text.strip()
            term = even.find(class_="views-field views-field-name-2").text.strip()
            dates = even.find(class_="views-field views-field-field-uw-imp-dates-date active").text.strip()

            important_date = "{\"Title\": \"" + str(title) + "\", \"TitleRef\": \"" + str(titleHref) + "\", \"Description\": \"" + str(description) + "\", \"Term\": \"" + str(term) + "\", \"Dates\": \"" + str(dates) + "\"}" 
            important_dates.append(important_date)
            count += 1
        #print(count)
    
    print(important_dates)

def get_total_pages(year: str):
    # Create the query url
    baseUrl = ALL_DATES_BASE_URL
    academicYear = year
    endUrl = ALL_DATES_PAGE
    baseEndUrl = ALL_DATES
    allUrl = baseUrl + academicYear + baseEndUrl
    condensedUrl = baseUrl + academicYear + endUrl
    url = baseUrl + academicYear + endUrl + "0"


    pageCount = 1
    page = requests.get(url)

    # Ensure that the status of the page is 200-299 to indicate success
    status = page.status_code
    realStatus = int(status / 100)
    if (realStatus != 2):
        return

    # Instantiate BeautifulSoup
    soup = BeautifulSoup(page.content, "html.parser")

    foundPages = soup.find_all(class_="pager-item")
    for result in foundPages:
        #print(result)
        pageCount += 1
    
    print('\n')
    load_pages(condensedUrl, pageCount, year)

#def json_conversion(raw: str):


def main():
    get_total_pages(ACADEMIC_YEAR_VALUE)

if __name__ == '__main__':
    main()


