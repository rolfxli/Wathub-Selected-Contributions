import os
import json
import requests

#from selenium import webdriver
#from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from typing import List, Dict

BASE_URL = 'https://uwaterloo.ca/important-dates/important-dates/list'
DIRECT_URL = 'https://uwaterloo.ca/important-dates/important-dates/list?date=Today&=All&page='

ALL_DATES_BASE_URL = 'https://uwaterloo.ca/important-dates/important-dates/list?academic_term=All&academic_year='
ACADEMIC_YEAR_VALUE='214'
ALL_DATES_PAGE='&audience=All&combine=&date=Any&type=All&=All&page='

ACADEMIC_YEAR = 'Sep 1, 2019 to Aug 31, 2020'
ACADEMIC_TERM = 'Spring'
TERM_NUMBER = '1205'

def load_pages(url: str, file_path: str):
    year_2018_2019 = 188
    year_2019_2020 = 214
    year_2020_2021 = 229

    #driver = webdriver.Chrome()
    #driver.get(url)

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

def get_total_pages(year: str):
    baseUrl = ALL_DATES_BASE_URL
    academicYear = year
    endUrl = ALL_DATES_PAGE
    url = baseUrl + academicYear + endUrl + "0"

    page = requests.get(url)
    #print(page.status_code)
    soup = BeautifulSoup(page.content, "html.parser")

    soup.find_all(class_="pager")



#def json_conversion(raw: str):


def main():
    get_total_pages(ACADEMIC_YEAR_VALUE)



if __name__ == '__main__':
    main()


