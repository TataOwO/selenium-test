import time
import re
import fnmatch
import json
import os

import numpy as np
import cv2

import function as util

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as EC  # noqa
from selenium.webdriver.support.wait import WebDriverWait

import undetected_chromedriver as uc

# initialize the browser
driver = uc.Chrome()

# load json files
schoolDict = util.load_json("schoolDict.json")
depDict = util.load_json("depDict.json")
imageTable = util.load_json("img2txt.json")
studentDict = util.load_json("studentDict.json")

prev = studentDict["prev"]
found = False
currentURL = ""

try:
    for dCount, dep in enumerate(depDict):
        d = depDict[dep]
        if d["url"] == prev: found = True
        if not found: continue
        driver.get(d["url"])
        currentURL = d["url"]
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "mainContent"))
        )
        
        depDict[dep]["student"] = {}
        
        for cCount, column in enumerate(driver.find_elements(By.XPATH, "//tr[@bgcolor='#FFFFFF' or @bgcolor='#DEDEDC']")):
            blockList = util.get_child_elements(column)
            _, studentRank, studentInfo, studentName, studentSchool = blockList
            currentStudentRank = util.process_student_rank(imageTable, studentRank)
            studentID, testPlace = util.process_student_info(studentInfo)
            stdDict = util.process_student_school(imageTable, studentSchool)
            stdDict["testPlace"] = testPlace.replace(":", "").strip()
            if studentID in studentDict: stdDict = util.merge_dicts(studentDict[studentID], stdDict)
            studentDict[studentID] = stdDict
            
            depDict[dep]["student"][studentID] = currentStudentRank
except:
    print("code failed")

studentDict["prev"] = currentURL

with open("depDict.json", "w") as fp:
    json.dump(depDict, fp)

with open("studentDict.json", "w") as fp:
    json.dump(studentDict, fp)

driver.quit()





