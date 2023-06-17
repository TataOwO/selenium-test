import time
import re
import fnmatch
import json
import os

import numpy as np
import cv2

import function as util

# load json files
schoolDict = util.load_json("schoolDict.json")
depDict = util.load_json("depDict.json")
studentDict = util.load_json("studentDict.json")

csvArr = [[u"學校代碼", u"學校名稱", u"校系代碼", u"系名", u"落點名次", u"學生應試號碼", u"考場名稱", u"錄取狀態", "錄取校系"]]

for stdID in studentDict:
    if stdID == "prev": continue
    stdD = studentDict[stdID]
    testPlace = stdD.pop("testPlace").replace(":", "").strip()
    stdArr = []
    oS = ""
    for depID in stdD:
        depD = stdD[depID]
        depName = depDict[depID]["name"]
        schoolID = depDict[depID]["school"]
        schoolName = schoolDict[schoolID]["name"]
        if schoolID != "105": continue
        onStat = depD["onStat"]
        correRanking = depD["ranking"]
        if onStat:
            oS = "{0} {1}".format(schoolName, depName)
            print(schoolName, stdID)
        onStat = u"錄取" if onStat else u"未錄取"
        stdArr.append([schoolID, schoolName, depID, depName, correRanking, stdID, testPlace, onStat, None])
    for each in stdArr:
        each[8] = oS
        csvArr.append(each)

# print(json.dumps(csvArr, indent=4))

for count, each in enumerate(csvArr):
    csvArr[count] = ",".join(each)

text = "\n".join(csvArr)

with open("111.csv", "w") as fp:
    fp.write(text)

# print(text)
