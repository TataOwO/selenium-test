import time
import re
import fnmatch
import json
import os

import numpy as np
import cv2

import base64 as b64

from pytesseract import pytesseract

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as EC  # noqa
from selenium.webdriver.support.wait import WebDriverWait

import undetected_chromedriver as uc

pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def list_remove_duplicate(l):
    return list(dict.fromkeys(l))

def get_schoolID_from_URL(url):
    output = url[:url.rfind("_")]
    return output[output.rfind("_")+1:]

def get_depID_from_URL(url):
    output = url[url.find("_")+1:]
    return output[:output.find("_")]

def get_schoolType_from_URL(url):
    output = url[:url.rfind("/")]
    return output[output.rfind("/")+1:]

def string_to_numString(text):
    try:
        return re.search(r'\d+', text).group()
    except:
        return text

def print_formatted_dict(d):
    print(json.dumps(d, indent=4))
    print(len(list(d.keys())))

def get_schoolID_from_name(schoolDict, name):
    for schoolID in schoolDict:
        if schoolDict[schoolID]["name"] == name: return schoolID
    return ""

def get_depID_from_name(depDict, schoolID, name):
    for depID in depDict:
        if depDict[depID]["name"] == name and depDict[depID]["school"] == schoolID: return depID
    return ""

def get_studentID_from_imgSRC(imgSRC):
    img = get_image_from_img_src(imgSRC)
    ID = image_to_text(img).strip()
    return ID

def get_image_from_img_src(inp):
    imgBytes = b64.b64decode(inp[22:])
    imgArr = np.frombuffer(imgBytes, dtype=np.uint8)
    img = cv2.imdecode(imgArr, flags=cv2.IMREAD_UNCHANGED)
    return img

def src2text(imageTable, src):
    if src is None:
        return None
    if src in imageTable:
        return imageTable[src]
    return False

def image_to_text(img):
    return pytesseract.image_to_string(img)

def eng2chr(text):
    return text.replace("p", u"正取").replace("n", u"備取").replace("o", u"離島").replace("k", u"金門").replace("m", u"馬祖").replace("w", u"澎湖").replace("u", u"原住民").replace("j", u"借取")

def get_child_elements(element):
    return element.find_elements(By.XPATH, "./*")

def get_parent_element(element):
    return element.find_element(By.XPATH, "./..")

def empty_rgba(x, y):
    arr = np.zeros((y, x, 4), dtype=np.uint8)
    output = cv2.cvtColor(arr, cv2.COLOR_RGB2RGBA)
    output = cv2.rectangle(output, (0, 0), (0, 0), (0,0,0,1), -1)
    return output

def empty_rgb(x, y):
    arr = np.zeros((y, x, 3), dtype=np.uint8)
    output = cv2.rectangle(arr, (0, 0), (0, 0), (0,0,0), -1)
    return output

def get_image_size(img):
    height, width, _ = img.shape
    return width, height

def overlay_img(background, overlay):
    output = cv2.addWeighted(background, 1, overlay, 1, 1)
    return output

def img_white2black(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_RGBA2HSV)
    mask = cv2.inRange(hsv, (255,255,255), (255,255,255))
    img[mask>0] = (0, 0, 0)
    return img

def img_trans2black(img):
    output = img.copy()
    trans_mask = output[:,:,3] == 0
    output[trans_mask] = [0, 0, 0, 255]
    ret = cv2.cvtColor(output, cv2.COLOR_BGRA2BGR)
    return ret

def empty_window(name):
    _, _2, width, height = cv2.getWindowImageRect(name)
    cv2.imshow(name, empty_rgb(width, height))

def load_json(filename):
    output = None
    with open(filename, "r") as fp:
        output = json.load(fp)
    return output

def process_student_rank(images, block):
    imgs = block.find_elements(By.TAG_NAME, "img")
    if not len(imgs): return None
    src = imgs[0].get_attribute("src")
    return src2text(images, src)

def process_student_info(block):
    imgs = block.find_elements(By.TAG_NAME, "img")
    img = None
    if len(imgs): img = imgs[0].get_attribute("src")
    ID = get_studentID_from_imgSRC(img)
    
    titles = block.find_elements(By.TAG_NAME, "a")
    title = None
    if len(titles): title = titles[0].text
    title = title.strip()
    title = title[3:]
    
    return ID, title

def check_depColumn_validation(dep):
    link = dep.find_element(By.TAG_NAME, "a")
    return not not link.text

def check_dep_on_stat(elems):
    imgElems = elems[0].find_elements(By.TAG_NAME, "img")
    if not len(imgElems): return False
    return "images/putdep1.png" in imgElems[0].get_attribute("src")

def get_depsID_from_block(elems):
    href = elems[1].find_element(By.TAG_NAME, "a").get_attribute("href")
    return get_depID_from_URL(href)

def get_rank_imgSRC(elems):
    imgElems = elems[2].find_elements(By.TAG_NAME, "img")
    if not len(imgElems): return None
    return imgElems[0].get_attribute("src")

def get_dep_rank_text(elems):
    imgElems = elems[2].find_elements(By.TAG_NAME, "img")
    if not len(imgElems): return ""
    return get_parent_element(imgElems[0]).text

def process_student_school(images, block):
    studentDict = {}
    ret = False
    table = block.find_element(By.TAG_NAME, "tbody")
    for dep in get_child_elements(table):
        if not check_depColumn_validation(dep): continue
        elems = get_child_elements(dep)
        onStat = check_dep_on_stat(elems)
        depID = get_depsID_from_block(elems)
        imgSRC = get_rank_imgSRC(elems)
        rankText = get_dep_rank_text(elems)
        ranking = src2text(images, imgSRC)
        if ranking is None:
            pass
        elif not ranking:
            ret = True
            print()
            print(imgSRC)
            break
        studentDict[depID] = {}
        studentDict[depID]["onStat"] = onStat
        studentDict[depID]["ranking"] = rankText + images[imgSRC] if imgSRC else ""
    return studentDict, ret

def merge_dicts(dict1, dict2):
    res = {}
    for each in dict1:
        if not each in dict2:
            res[each] = dict1[each]
            continue
        if type(dict1[each]) == dict and type(dict2[each]) == dict:
            res[each] = merge_dicts(dict1[each], dict2[each])
            continue
        res[each] = dict1[each]
    for each in dict2:
        if each in res:
            continue
        if not each in dict1:
            res[each] = dict2[each]
            continue
        if type(dict1[each]) == dict and type(dict2[each]) == dict:
            res[each] = merge_dicts(dict1[each], dict2[each])
            continue
        res[each] = dict2[each]
    return res

def fill_text4img(img):
    inp = ""
    while True:
        cv2.imshow("img", img)
        ret = cv2.waitKey(33)
        if ret == 8:  # backspace
            inp = inp[:-1]
            print(inp)
            continue
        if ret == 91: # [ -> go left
            print()
            cv2.destroyAllWindows()
            return -1, inp
        if ret == 93: # ] -> go right
            print()
            cv2.destroyAllWindows()
            return 1, inp
        if ret == 13: # enter
            leaveStat = True
            prev = d["url"]
            return 0, None
        if ret in range(1, 256):
            inp += chr(ret)
            print(inp)

def type2txt(typeName):
    if typeName == "cross":
        return u"普大 個人申請"
    if typeName == "tech":
        return u"科大 四技申請"
    if typeName == "vtech":
        return u"統測甄選"
    return ""

def determine_depDict(crossDict, vtechDict, depID):
    if depID in crossDict: return crossDict
    if depID in vtechDict: return vtechDict
    return None
