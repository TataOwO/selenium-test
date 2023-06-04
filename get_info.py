import time
import re
import fnmatch
import json
import os

import function as func

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as EC  # noqa
from selenium.webdriver.support.wait import WebDriverWait

import undetected_chromedriver as uc

MAIN_PAGE_URL = os.getenv("https://www.com.tw/cross/")

# initialize the browser
driver = uc.Chrome()

# get page information
driver.get(MAIN_PAGE_URL)
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, "university_list_row_height"))
)

# create a dictionary that contains school information
schoolDict = {}

# search for school URLs and filter them
for count, each in enumerate(driver.find_elements(By.XPATH, "//a[contains(@href, 'university_') and not(contains(@href, 'list')) and contains(@href, '.html')]")):
    href = each.get_attribute("href")
    text = each.text
    id = func.get_schoolID_from_URL(href)
    
    if not id.isnumeric or len(id) != 3: continue
    schoolDict[str(id)] = {"url":str(href), "name":str(text), "dep":{}}

# prints information
func.print_formatted_dict(schoolDict)

# department dictionary
depDict = {}

# search for department URLs and filter them
for count, school in enumerate(schoolDict):
    # access school page
    d = schoolDict[school]
    driver.get(d["url"])
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "university_dep_row_height"))
    )
    
    for each in driver.find_elements(By.XPATH, "//a[contains(@href, 'check_') and contains(@href, '_NO_') and contains(@href, '.html')]"):
        href = each.get_attribute("href")
        text = each.text
        id = func.get_depID_from_URL(href)
        
        if not id.isnumeric or len(id) != 6: continue
        depDict[str(id)] = {"url":str(href), "name":str(text), "school": str(school)}
        # schoolDict[func.get_schoolID_from_name(title)]["dep"][id] = {"url":href, "name":text}
        # we will do this later

# prints information
func.print_formatted_dict(depDict)

with open("schoolDict.json", "w") as fp:
    json.dump(schoolDict, fp)

with open("depDict.json", "w") as fp:
    json.dump(depDict, fp)

driver.quit()





