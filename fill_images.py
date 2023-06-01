import time
import re
import fnmatch
import json

import function as func

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as EC  # noqa
from selenium.webdriver.support.wait import WebDriverWait

import undetected_chromedriver as uc

MAIN_PAGE_URL = "https://www.com.tw/cross/university_list111.html"

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
for count, each in enumerate(driver.find_elements(By.XPATH, "/a[contains(@href, 'university') and not(contains(@href, 'list')) and contains(@href, '.html')]]")):
    # if len(list(schoolDict.keys())) == 4: break
    
    href = each.get_attribute("href")
    text = each.text
    id = func.get_schoolID_from_URL(href)
    
    if not id.isnumeric or len(id) != 3: continue
    schoolDict[id] = {"url":href, "name":text, "dep":{}}

# schoolDict.pop("004")
# prints information
# func.print_formatted_dict(schoolDict)

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
        depDict[id] = {"url":href, "name":text, "school": school}
        # schoolDict[func.get_schoolID_from_name(title)]["dep"][id] = {"url":href, "name":text}
        # we will do this later

# prints information
func.print_formatted_dict(depDict)

stdDict = {}

images = {}
imgKey = []

for dep in depDict:
    d = depDict[school]
    driver.get(d["url"])
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "mainContent"))
    )
    
    # for column in driver.find_elements(By.XPATH, "//tr[@bgcolor='#FFFFFF' or @bgcolor='#DEDEDC']"):
    table = driver.find_element(By.XPATH, "//table[@style='overflow:hidden' and @cellpadding='0' and @cellspacing='0']")
    for imgElem in table.find_elements(By.TAG_NAME, "img"):
        src = imgElem.get_attribute("src")
        if not src.startswith("data:image/png;base64,"): continue
        images[src] = {"img":func.get_image_from_img_src(src), "text":""}
        imgKey.append(src)

i = 0
inp = ""

while i < len(imgKey):
    key = imgKey[i]
    cv2.imshow("img", images[key])
    ret = cv2.waitKey(33)
    if ret

driver.quit()





