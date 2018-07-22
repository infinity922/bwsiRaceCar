#!/usr/bin/env python

import rospy
import cv2
import cv_bridge
import numpy as np
import drivers

from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Image

im = cv2.imread("red shapes.jpg")
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 10, 255, 0)
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#cnts = cnts[0] if imutils.is_cv2() else cnts[1]
print("Length of contours list is: ", len(contours))


# loop over the contours


i = 0
for c in contours:
# compute the center of the contour
    M = cv2.moments(c)
    area = int(M["m00"])
    if (area > 0):	
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
# draw the contour and center of the shape on the image
    if (area > 1000):
        cv2.drawContours(im, [c], -1, (0, 255, 0), 2)
        cv2.circle(im, (cX, cY), 7, (0, 255, 255), -1)
        text = "center" + str(i) + " area: " + str(area)
	cv2.putText(im, text, (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    i = i + 1

cv2.imshow('contours', im)
cv2.waitKey(0)
cv2.destroyAllWindows()
