import time
import re
import fnmatch
import json
import numpy as np
import cv2
import sys

import function as util

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as EC  # noqa
from selenium.webdriver.support.wait import WebDriverWait

import undetected_chromedriver as uc

# initialize the browser
driver = uc.Chrome()

desiredType = sys.argv[1]

depDict = util.load_json("depDict.json")

studentDict = util.load_json(f"{desiredType}.json")

imageTable = util.load_json("img2txt.json")
imgKey = list(imageTable.keys())

print(studentDict["unprocessed"])

i = 0
inp = ""

prev = imageTable[imgKey[0]]
found = not prev
currentURL = ""
leaveStat = False

try:
# if True:
    for dCount, dep in enumerate(studentDict["unprocessed"]):
        d = depDict[dep]
        if d["url"] == prev: found = True
        if not found: continue
        driver.get(d["url"])
        currentURL = d["url"]
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "mainContent"))
        )
        
        for cCount, column in enumerate(driver.find_elements(By.XPATH, "//tr[@bgcolor='#FFFFFF' or @bgcolor='#DEDEDC']")):
            blockList = util.get_child_elements(column)
            for imgElem in blockList[1].find_elements(By.TAG_NAME, "img"):
                src = imgElem.get_attribute("src")
                if not src.startswith("data:image/png;base64,") or src in imgKey: continue
                img = util.get_image_from_img_src(src)
                img = util.img_trans2black(img)
                imageTable[src] = {"img":img, "text":""}
                imgKey.append(src)
            for imgElem in blockList[4].find_elements(By.TAG_NAME, "img"):
                src = imgElem.get_attribute("src")
                if not src.startswith("data:image/png;base64,") or src in imgKey: continue
                img = util.get_image_from_img_src(src)
                img = util.img_trans2black(img)
                imageTable[src] = {"img":img, "text":""}
                imgKey.append(src)
        
        while i < len(imgKey):
            if i < 0: i = 0
            key = imgKey[i]
            if type(imageTable[key]) == str:
                i += 1
                continue
            img = imageTable[key]["img"]
            ret = util.fill_text4img(img)
            if ret[1] == None:
                leaveStat = True
                break
            i += ret[0]
            imageTable[key]["text"] = ret[1]
        if leaveStat: break
except:
    leaveStat = True
    print("code failed")

print(currentURL)

imageTable["prev"] = currentURL if leaveStat else ""

for key in imgKey:
    if type(imageTable[key]) == str:
        continue
    text = util.eng2chr(imageTable[key]["text"])
    if text == "":
        imageTable.pop(key)
    else:
        imageTable[key] = text

with open("img2txt.json", "w") as fp:
    json.dump(imageTable, fp)

driver.quit()





