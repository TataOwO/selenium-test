import time
import re
import fnmatch
import json
import os

import function as util

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as EC  # noqa
from selenium.webdriver.support.wait import WebDriverWait

import undetected_chromedriver as uc

MAIN_PAGE_URL = [
    "https://www.com.tw/cross/university_list111.html",
    "https://www.com.tw/vtech/university_list111.html",
    "https://www.com.tw/cross/tech_university_list111.html"
]

# initialize the browser
driver = uc.Chrome()

# create a dictionary that contains school information
schoolDict = {}

for url in MAIN_PAGE_URL:
    # get page information
    driver.get(url)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "university_list_row_height"))
    )

    # search for school URLs and filter them
    for count, each in enumerate(driver.find_elements(By.XPATH, "//a[contains(@href, 'university_') and not(contains(@href, 'list')) and contains(@href, '.html')]")):
        href = each.get_attribute("href")
        text = each.text
        id = util.get_schoolID_from_URL(href)
        schoolType = util.get_schoolType_from_URL(href) if len(id) == 3 else "tech"
        
        if not id.isnumeric: continue
        schoolDict[id] = {"url":href, "name":text, "type":schoolType}

# prints information
util.print_formatted_dict(schoolDict)

# department dictionary
depDict = {}

# search for department URLs and filter them
for count, school in enumerate(schoolDict):
    # access school page
    # if school != "105": continue
    d = schoolDict[school]
    driver.get(d["url"])
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "university_dep_row_height"))
    )
    
    for each in driver.find_elements(By.XPATH, "//a[contains(@href, 'check_') and contains(@href, '_NO_') and contains(@href, '.html')]"):
        href = each.get_attribute("href")
        text = each.text
        id = util.get_depID_from_URL(href)
        
        if not id.isnumeric or id in depDict: continue
        depDict[id] = {"url":href, "name":text, "school": school, "type":d["type"]}
        # schoolDict[util.get_schoolID_from_name(title)]["dep"][id] = {"url":href, "name":text}
        # we will do this later

# prints information
util.print_formatted_dict(depDict)

with open("schoolDict.json", "w") as fp:
    json.dump(schoolDict, fp)

with open("depDict.json", "w") as fp:
    json.dump(depDict, fp)

driver.quit()



