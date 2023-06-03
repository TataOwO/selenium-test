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

url = "https://www.com.tw/cross/check_011072_NO_1_111_0_3.html"

images = util.load_json("img2txt.json")

pos = 13

driver.get(url)
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.ID, "mainContent"))
)

column = driver.find_elements(By.XPATH, "//tr[@bgcolor='#FFFFFF' or @bgcolor='#DEDEDC']")[pos]

blockList = util.get_child_elements(column)
_, studentRank, studentInfo, studentName, studentSchool = blockList
currentStudentRank = util.process_student_rank(images, studentRank)
studentID, testPlace = util.process_student_info(studentInfo)
res = util.process_student_school(studentSchool)

print("currentStudentRank", currentStudentRank)
print("studentID", studentID)
print("testPlace", testPlace)
util.print_formatted_dict(res)
