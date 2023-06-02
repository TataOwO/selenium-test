import cv2
import numpy as np

empty = np.zeros((500, 500, 3), dtype=np.uint8)

while True:
    cv2.imshow("img", empty)
    ret = cv2.waitKey(33)
    if ret != -1:
        print(ret)


