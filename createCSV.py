import time
import re
import fnmatch
import json
import os
import sys

import numpy as np
import cv2

import function as util

desiredType = sys.argv[1]

# load json files
schoolDict = util.load_json("schoolDict.json")
depDict = util.load_json("depDict.json")
studentDict = util.load_json(f"{desiredType}.json")

csvArr = [[u"學校代碼", u"學校名稱", u"校系代碼", u"系名", u"申請管道", u"落點名次", u"學生應試號碼", u"考場名稱", u"錄取狀態", "錄取校系"]]

for stdID in studentDict:
    if stdID == "prev" or stdID == "unprocessed": continue
    stdD = studentDict[stdID]
    testPlace = stdD.pop("testPlace").replace(":", "").strip()
    stdArr = []
    oS = ""
    for depID in stdD:
        if "109042" in depID: util.print_formatted_dict(stdD)
        depD = stdD[depID]
        depName = depDict[depID]["name"]
        schoolID = depDict[depID]["school"]
        schoolName = schoolDict[schoolID]["name"]
        schoolType = depDict[depID]["type"]
        onStat = depD["onStat"]
        correRanking = depD["ranking"]
        stdID = util.string_to_numString(stdID)
        if onStat:
            oS = "{0} {1}".format(schoolName, depName)
            # print(schoolName, stdID)
        onStat = u"錄取" if onStat else u"未錄取"
        stdArr.append([schoolID, schoolName, depID, depName, schoolType, correRanking, stdID, testPlace, onStat, None])
    for each in stdArr:
        each[8] = oS
        csvArr.append(each)

# print(json.dumps(csvArr, indent=4))

for count, each in enumerate(csvArr):
    csvArr[count] = ",".join(each)

text = "\n".join(csvArr)

with open(f"{desiredType}.csv", "w+") as fp:
    fp.write(text)

# print(text)
