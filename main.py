import time
import re
import fnmatch
import json
import os
import sys

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

desiredType = sys.argv[1]

# load json files
schoolDict = util.load_json("schoolDict.json")
depDict = util.load_json("depDict.json")
imageTable = util.load_json("img2txt.json")
studentDict = util.load_json(f"{desiredType}.json")

prev = studentDict["prev"]
found = not prev
currentURL = ""
leaveStat = False

try:
# if True:
    for dCount, depID in enumerate(depDict):
    # for dCount, depID in enumerate(studentDict["unprocessed"]):
        d = depDict[depID]
        if d["url"] == prev: found = True
        if not found: continue
        if d["type"] != desiredType: continue
        # if d["school"] != "105": continue
        driver.get(d["url"])
        currentURL = d["url"]
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "mainContent"))
        )
        
        for cCount, column in enumerate(driver.find_elements(By.XPATH, "//tr[@bgcolor='#FFFFFF' or @bgcolor='#DEDEDC']")):
            blockList = util.get_child_elements(column)
            _, studentRank, studentInfo, studentName, studentSchool = blockList
            currentStudentRank = util.process_student_rank(imageTable, studentRank)
            if currentStudentRank == False:
                print("csr", currentStudentRank)
                if not depID in studentDict["unprocessed"]: studentDict["unprocessed"].append(depID)
                continue
            studentID, testPlace = util.process_student_info(studentInfo)
            stdDict, pStat = util.process_student_school(imageTable, studentSchool)
            if pStat:
                # print("pstat")
                if depID not in studentDict["unprocessed"]: studentDict["unprocessed"].append(depID)
                continue
            stdDict["testPlace"] = testPlace.replace(":", "").strip()
            if studentID in studentDict: stdDict = util.merge_dicts(studentDict[studentID], stdDict)
            studentDict[studentID] = stdDict
except:
    leaveStat = True
    print("code failed")

studentDict["prev"] = currentURL if leaveStat else ""

with open(f"{desiredType}.json", "w+") as fp:
    json.dump(studentDict, fp)

driver.quit()





