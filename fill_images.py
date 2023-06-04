import time
import re
import fnmatch
import json
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

depDict = util.load_json("depDict.json")

images = util.load_json("img2txt.json")
imgKey = list(images.keys())

i = 0
inp = ""

prev = images[imgKey[0]]
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
        
        for cCount, column in enumerate(driver.find_elements(By.XPATH, "//tr[@bgcolor='#FFFFFF' or @bgcolor='#DEDEDC']")):
            blockList = util.get_child_elements(column)
            for imgElem in blockList[1].find_elements(By.TAG_NAME, "img"):
                src = imgElem.get_attribute("src")
                if not src.startswith("data:image/png;base64,") or src in imgKey: continue
                img = util.get_image_from_img_src(src)
                img = util.img_trans2black(img)
                images[src] = {"img":img, "text":""}
                imgKey.append(src)
            for imgElem in blockList[4].find_elements(By.TAG_NAME, "img"):
                src = imgElem.get_attribute("src")
                if not src.startswith("data:image/png;base64,") or src in imgKey: continue
                img = util.get_image_from_img_src(src)
                img = util.img_trans2black(img)
                images[src] = {"img":img, "text":""}
                imgKey.append(src)
        
        leaveStat = False
        while i < len(imgKey):
            if i < 0: i = 0
            key = imgKey[i]
            if type(images[key]) == str:
                i += 1
                continue
            cv2.imshow("img", images[key]["img"])
            ret = cv2.waitKey(33)
            if ret == 91: # [ -> go left
                i -= 1
                images[key]["text"] = inp
                inp = ""
                print()
                cv2.destroyAllWindows()
                continue
            if ret == 93: # ] -> go right
                i += 1
                images[key]["text"] = inp
                inp = ""
                print()
                cv2.destroyAllWindows()
                continue
            if ret == 8:  # backspace
                inp = inp[:-1]
                print(inp)
                continue
            if ret == 13: # enter
                leaveStat = True
                prev = d["url"]
                break
            if ret in range(1, 256):
                inp += chr(ret)
                print(inp)
        if leaveStat: break
except:
    print("code failed")

print(currentURL)

images["prev"] = currentURL

for key in imgKey:
    if type(images[key]) == str:
        continue
    text = util.eng2chr(images[key]["text"])
    if text == "":
        images.pop(key)
    else:
        images[key] = text

with open("img2txt.json", "w") as fp:
    json.dump(images, fp)

driver.quit()





