import base64 as b64
import json
from pytesseract import pytesseract
import numpy as np
import cv2

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

def get_studentID(column):
    b = column.get_element(By.XPATH, "//td[@width='28%']")
    imgElem = b.get_element(By.TAG_NAME, "img")
    imgSRC = imgElem.get_attribute("src")
    img = get_image_from_img_src(imgSRC)
    ID = image_to_text(img)
    return ID

def get_image_from_img_src(inp):
    imgBytes = b64.b64decode(inp[22:])
    imgArr = np.frombuffer(imgBytes, dtype=np.uint8)
    img = cv2.imdecode(imgArr, flags=cv2.IMREAD_COLOR)
    return img

def image_to_text(img):
    return pytesseract.image_to_string(img)
