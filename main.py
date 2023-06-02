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

load_dotenv()  # take environment variables from .env.

# initialize the browser
driver = uc.Chrome()

depDict = None

with open("depDict.json", "r") as fp:
    depDict = json.load(fp)

images = None

with open("img2txt.json", "r") as fp:
    images = json.load(fp)

schoolDict = None

with open("schoolDict.json", "r") as fp:
    schoolDict = json.load(fp)

depDict = None

with open("depDict.json", "r") as fp:
    depDict = json.load(fp)

studentDict = {}

for dCount, dep in enumerate(depDict):
    d = depDict[dep]
    driver.get(d["url"])
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "mainContent"))
    )
    
    for cCount, column in enumerate(driver.find_elements(By.XPATH, "//tr[@bgcolor='#FFFFFF' or @bgcolor='#DEDEDC']")):
        blockList = util.get_child_elements(column)
        _, ranking, studentInfo, studentName, studentSchool = blockList
        currentStudentRank = util.processStudentRank(images, ranking)
        

driver.quit()





