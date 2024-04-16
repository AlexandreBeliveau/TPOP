import cv2
import os
import numpy as np

cwd = os.getcwd()+'/Projet_2/images_calibration/laserD'
images = os.listdir(cwd)

for name in images:
    im = cv2.imread(cwd + '/' + name)
    # cv2.imshow('image laser', im)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    filtered = cv2.morphologyEx(binary, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    contours, hierarchy = cv2.findContours(filtered, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 50:
            cv2.drawContours(im, [contour], 0, (0, 255, 0), 2)
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.circle(im, (cX, cY), 5, (0, 0, 255), -1)
    

    cv2.imshow('filtered image', im)
    cv2.waitKey(0)

