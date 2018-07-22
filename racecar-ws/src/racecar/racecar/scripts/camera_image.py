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
	self.isOpen = False
    
    def image_callback(self, msg):
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding = 'bgr8')
        cX = 0
	if(not self.isOpen):
		self.isOpen = True
                
                hsvv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                # define range of color in HSV
                lower = np.array([10,50,170])
                upper = np.array([25,255,255])

                # define range of red color in HSV
                #lower = np.array([0,50,50])
                #upper = np.array([40,255,255])

                # define range of green color in HSV
                #lower = np.array([40,50,50])
                #upper = np.array([100,255,255])

                # define range of blue color in HSV
                #lower = np.array([100,50,50])
                #upper = np.array([150,255,255])

                # define range of yellow color in HSV
                #lower = np.array([50,50,50])
                #upper = np.array([60,100,100])


                # Filter the HSV image to get only one color
                filt = cv2.inRange(hsvv, lower, upper)
                # Superimpose the original and filter mask by Bitwise-AND mask and original image
                res_red = cv2.bitwise_and(image,image, mask= filt)

                blurred = cv2.GaussianBlur(filt, (5, 5), 0)
                thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
#                thresh2 = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
#                thresh3 = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

                # find contours in the thresholded image
                im2,contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                print("Length of contours list is: ", len(contours))


                # loop over the contours
                i = 0
                a = np.array([]) #create an array to hold area values
                for c in contours:
	        # compute the area and center of each contour
  	            M = cv2.moments(c)
                    area = int(M["m00"])
                    a = np.append(a,area)
#                    if (area > 0):	
#                        cX = int(M["m10"] / M["m00"])
#	                cY = int(M["m01"] / M["m00"])

#	         draw each contour and center of the shape on the image
#                    if (1):
#	                cv2.drawContours(res_red, [c], -1, (0, 255, 0), 2)
#	                cv2.circle(res_red, (cX, cY), 7, (0, 255, 255), -1)
#                       text = "center" + str(i) + " area: " + str(area)
#	                cv2.putText(res_red, text, (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                    i = i + 1

                if len(a) != 0: 
			print("Biggest area is ", np.amax(a))
			print("corresponds to contour no: ", np.argmax(a))
			cX = 0
			cc = np.argmax(a)
			M = cv2.moments(contours[cc])
			area = int(M["m00"])

			if (area > 0):	
			    cX = int(M["m10"] / M["m00"])
			    cY = int(M["m01"] / M["m00"])
			else:
				cX = 0
				cY = 0

			cv2.drawContours(res_red, contours[cc], -1, (0, 255, 0), 2)
			cv2.circle(res_red, (cX, cY), 7, (0, 255, 255), -1)
			text = "center" + str(cc) + " area: " + str(area)
			cv2.putText(res_red, text, (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
		else:
			cX = 320
			cY = 50

#		cv2.imshow('original', image)
		#cv2.imshow('contours', res_red)
		#cv2.waitKey(0)
		cv2.destroyAllWindows()
		
		self.isOpen = False
		print(cX)
        error = (float(cX)-320)/320
        drivers.pd(error, -2, -10, 1)
	print error
        

if __name__ == '__main__':
    try:
        rospy.init_node('camera', anonymous=True)
    	rate = rospy.Rate(100) # 20hz
        f = Follower()
    	while not rospy.is_shutdown():
			rospy.spin()


    except rospy.ROSInterruptException:
        pass        
