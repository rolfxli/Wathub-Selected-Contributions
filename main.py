import os
import json
import requests
import pprint

from bs4 import BeautifulSoup
from typing import List, Dict

BASE_URL = 'https://uwaterloo.ca/important-dates/important-dates/list'
DIRECT_URL = 'https://uwaterloo.ca/important-dates/important-dates/list?date=Today&=All&page='

ALL_DATES_BASE_URL = 'https://uwaterloo.ca/important-dates/important-dates/list?academic_term=All&academic_year='
ACADEMIC_YEAR_VALUE='214'
ALL_DATES_PAGE='&audience=All&combine=&date=Any&type=All&=All&page='
ALL_DATES='&audience=All&combine=&date=Any&type=All&=All'

def writeOut(normalString: str, year: int):
    file_name = "important_dates_" + str(year) + ".txt"
    f = open(file_name, "w")
    f.write(normalString)
    f.close()

    #json_file_name = "important_dates_" + str(year) + ".json"
    #fs = open(file_name, "r")
    #data = fs.read()
    #jsonString = json.loads(data)
    #jf = open(json_file_name, "w")
    #json.dump(jsonString, jf)
    #jf.close()


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
    jsonString = "["
    item_count = 0
    
    for page in range(count):
        final_url = ""
        if (page == 0):
            final_url = firstUrl
        else:
            final_url = url + str(page)

        page = requests.get(final_url)
        soup = BeautifulSoup(page.content, "html.parser")
        evens = soup.find_all(class_="even")
        odds = soup.find_all(class_="odd")

        for even in evens:
            hrefs = even.find_all('a')
            title = even.find(class_="views-field views-field-title-1").text.strip()
            title = str(title).replace("\n"," ").replace("\r"," ").replace("\\n", " ").replace('"', "")

            titleHref = redirectionUrl + str(hrefs[0].get('href'))
            titleHref = str(titleHref).replace("\n"," ").replace("\r"," ").replace("\\n", " ").replace('"', "")

            description = even.find(class_="views-field views-field-field-uw-imp-dates-description").text.strip()
            description = str(description).replace("\n"," ").replace("\r"," ").replace("\\n", " ").replace('"', "")

            term = even.find(class_="views-field views-field-name-2").text.strip()
            term = str(term).replace("\n"," ").replace("\r"," ").replace("\\n", " ").replace('"', "")

            dates = even.find(class_="views-field views-field-field-uw-imp-dates-date active").text.strip()
            dates = str(dates).replace("\n"," ").replace("\r"," ").replace("\\n", " ").replace('"', "")

            important_date = "{\"Title\": \"" + title + "\", \"TitleRef\": \"" + titleHref + "\", \"Description\": \"" + description + "\", \"Term\": \"" + term + "\", \"Dates\": \"" + dates + "\"}"
            important_date = str(important_date)
            important_dates.append(important_date)
            jsonString += important_date
            jsonString += ","
            item_count += 1

        for odd in odds:
            hrefs = odd.find_all('a')
            title = odd.find(class_="views-field views-field-title-1").text.strip()
            title = str(title).replace("\n"," ").replace("\r"," ").replace("\\n", " ").replace('"', "")

            titleHref = redirectionUrl + str(hrefs[0].get('href'))
            titleHref = str(titleHref).replace("\n"," ").replace("\r"," ").replace("\\n", " ").replace('"', "")

            description = odd.find(class_="views-field views-field-field-uw-imp-dates-description").text.strip()
            description = str(description).replace("\n"," ").replace("\r"," ").replace("\\n", " ").replace('"', "")

            term = odd.find(class_="views-field views-field-name-2").text.strip()
            term = str(term).replace("\n"," ").replace("\r"," ").replace("\\n", " ").replace('"', "")

            dates = odd.find(class_="views-field views-field-field-uw-imp-dates-date active").text.strip()
            dates = str(dates).replace("\n"," ").replace("\r"," ").replace("\\n", " ").replace('"', "")

            important_date = "{\"Title\": \"" + title + "\", \"TitleRef\": \"" + titleHref + "\", \"Description\": \"" + description + "\", \"Term\": \"" + term + "\", \"Dates\": \"" + dates + "\"}"
            important_date = str(important_date)
            important_dates.append(important_date)
            jsonString += important_date
            jsonString += ","
            item_count += 1

    jsonString = jsonString[:-1]
    jsonString += "]"

    writeOut(jsonString, year)

    print(important_dates)
    print('\n')
    print(item_count)

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
        pageCount += 1
    
    load_pages(condensedUrl, pageCount, year)

def main():
    get_total_pages(ACADEMIC_YEAR_VALUE)

if __name__ == '__main__':
    main()

