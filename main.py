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

from dotenv import load_dotenv

load_dotenv()  # grab environment variables from .env

# initialize the browser
driver = uc.Chrome()

# load json files
schoolDict = util.load_json("schoolDict.json")
depDict = util.load_json("depDict.json")
imageTable = util.load_json("img2txt.json")

studentDict = {}

for dCount, dep in enumerate(depDict):
    d = depDict[dep]
    driver.get(d["url"])
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "mainContent"))
    )
    
    for cCount, column in enumerate(driver.find_elements(By.XPATH, "//tr[@bgcolor='#FFFFFF' or @bgcolor='#DEDEDC']")):
        blockList = util.get_child_elements(column)
        _, studentRank, studentInfo, studentName, studentSchool = blockList
        currentStudentRank = util.process_student_rank(images, studentRank)
        studentID, testPlace = util.process_student_info(studentInfo)
        stdDict = util.process_student_school(studentSchool)
        stdDict["ranking"] = imageTable[stdDict.pop("imgSRC")]




driver.quit()





