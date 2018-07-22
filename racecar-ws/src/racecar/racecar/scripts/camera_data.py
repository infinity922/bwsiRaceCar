#!/usr/bin/env python

import rospy
import cv2
import cv_bridge
import numpy as np
import drivers

from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Image


class Follower:
    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        self.image_sub = rospy.Subscriber('/usb_cam/image_raw', Image, self.image_callback)
    
    def image_callback(self, msg):
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding = 'bgr8')
        hsvv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0,50,50])
        upper_red = np.array([40, 255, 255])
        red = cv2.inRange(hsvv, lower_red, upper_red)
        res_red = cv2.bitwise_and(image, image, mask = red)
        blurred = cv2.GaussianBlur(red, (5,5), 0)
        thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
        red = thresh
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0]

        for c in cnts:
           M = cv2.moments(c)
           area = int(M['m00'])
           if area > 0:
               cX = int(M['m10']/M['m00'])
               cY = int(M['m01']/M['m00'])
           if area > 200:
               #cv2.drawContours(res_red, [c], -1, (0, 255, 0), 2)
               cv2.circle(res_red, (cX, cY), 7, (255, 255, 255) , -1)
               #cv2.putText(res_red, 'center', (cX-20, cY-20), cv2.FRONT_HERSEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.imshow('Image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        

if __name__ == '__main__':
    try:
        rospy.init_node('camera', anonymous=True)
    	rate = rospy.Rate(100) # 20hz
        Follower()
    	while not rospy.is_shutdown():
			rospy.spin()


    except rospy.ROSInterruptException:
        pass        
