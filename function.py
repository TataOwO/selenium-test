import time
import re
import fnmatch
import json
import os

import numpy as np
import cv2

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as EC  # noqa
from selenium.webdriver.support.wait import WebDriverWait

import undetected_chromedriver as uc

pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def list_remove_duplicate(l):
    return list(dict.fromkeys(l))

def get_schoolID_from_URL(url):
    return url[36:39]

def get_depID_from_URL(url):
    return url[31:37]

def print_formatted_dict(d):
    print(json.dumps(d, indent=4))
    print(len(list(d.keys())))

def get_schoolID_from_name(name):
    for each in schoolDict:
        if schoolDict[each]["name"] == name: return each

def get_studentID(block):
    imgElem = block.get_element(By.TAG_NAME, "img")
    imgSRC = imgElem.get_attribute("src")
    img = get_image_from_img_src(imgSRC)
    ID = image_to_text(img)
    return ID

def get_image_from_img_src(inp):
    imgBytes = b64.b64decode(inp[22:])
    imgArr = np.frombuffer(imgBytes, dtype=np.uint8)
    img = cv2.imdecode(imgArr, flags=cv2.IMREAD_UNCHANGED)
    return img

def image_to_text(img):
    return pytesseract.image_to_string(img)

def eng2chr(text):
    return text.replace("p", u"正").replace("n", u"負").replace("o", u"離島").replace("k", u"金門").replace("m", u"馬祖").replace("w", u"澎湖")

def get_child_elements(element):
    return element.find_elements(By.XPATH, "./*")

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
    
def processStudentRank(images, block):
    imgs = block.find_elements(By.TAG_NAME, "img")
    if not len(imgs): return None
    return images[imgs[0]]
