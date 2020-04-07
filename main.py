import os
import json

from selenium import webdriver
#from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from typing import List, Dict

BASE_URL = 'https://uwaterloo.ca/important-dates/important-dates/list'

ACADEMIC_YEAR = 'Sep 1, 2019 to Aug 31, 2020'
ACADEMIC_TERM = 'Spring'
TERM_NUMBER = '1205'

def scrape_dates(url: str, file_path: str):

    driver = webdriver.Chrome()
    driver.get(url)

def json_conversion(raw: str):


def main():
    result = str(scrape_dates(BASE_URL))

if __name__ == '__main__':
    main()


