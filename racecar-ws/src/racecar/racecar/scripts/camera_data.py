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
