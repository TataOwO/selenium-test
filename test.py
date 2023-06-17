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

imageTable = util.load_json("img2txt.json")

# initialize the browser
driver = uc.Chrome()

url = "https://www.com.tw/cross/check_001042_NO_0_111_0_3.html"

driver.get(url)
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.ID, "mainContent"))
)

column = driver.find_elements(By.XPATH, "//tr[@bgcolor='#FFFFFF' or @bgcolor='#DEDEDC']")[0]

blockList = util.get_child_elements(column)
_, studentRank, studentInfo, studentName, studentSchool = blockList

deps = studentSchool.find_elements(By.TAG_NAME, "tbody")[0]

depElems = util.get_child_elements(util.get_child_elements(deps)[1])

test = depElems[2].get_attribute("test")

print(test)

