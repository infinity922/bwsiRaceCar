#!/usr/bin/env python

import rospy
import cv2
import cv_bridge
import numpy as np
from std_msgs.msg import String
from ackermann_msgs.msg import AckermannDriveStamped
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Image

#####-----
#!/usr/bin/env python
# BEGIN ALL
# import rospy
# from sensor_msgs.msg import Image
# import cv2, cv_bridge

# class Follower:
#  def __init__(self):
#    self.bridge = cv_bridge.CvBridge()
#    cv2.namedWindow("window", 1)
#    self.image_sub = rospy.Subscriber('camera/rgb/image_raw', 
#                                      Image, self.image_callback)
#  def image_callback(self, msg):
#    image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
#    cv2.imshow("window", image)
#    cv2.waitKey(3)

# rospy.init_node('follower')
# follower = Follower()
# rospy.spin()
# END ALL
#####-----
def drive(x,th,t):
    
    pubb = rospy.Publisher('/vesc/ackermann_cmd_mux/output', AckermannDriveStamped, queue_size=10)
    msg = AckermannDriveStamped();
    msg.header.stamp = rospy.Time.now();
    msg.header.frame_id = "base_link";

    msg.drive.speed = x;
    msg.drive.acceleration = 1;
    msg.drive.jerk = 1;
    msg.drive.steering_angle = th;
    msg.drive.steering_angle_velocity = 1;
    pubb.publish(msg)

def lidarCallback(data):
	distance = data.ranges[540]
	if(distance > 6):
		rospy.loginfo("Driving forward %f" % distance)
		drive(1, 0, 10)
	else:
		rospy.loginfo("Driving backward %f" % distance)
		drive(-1, 0, 10)

class Follower:

  def __init__(self):
    self.bridge = cv_bridge.CvBridge()
    cv2.namedWindow("window", 1)
    self.image_sub = rospy.Subscriber('/camera/zed/rgb/image_rect_color',Image, self.image_callback)

  def image_callback(self, msg):
    image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
 #   cv2.imshow("window", image)

    hsvv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # define range of red color in HSV
    lower_red = np.array([0,50,50])
    upper_red = np.array([40,255,255])

    # Threshold the HSV image to get only yellow colors
    red = cv2.inRange(hsvv, lower_red, upper_red)

    # Superimpose the original and filter mask by Bitwise-AND mask and original image
    res_red = cv2.bitwise_and(image,image, mask= red)

    blurred = cv2.GaussianBlur(red, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
    red = thresh

# find contours in the thresholded image
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
#cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    cnts = cnts[0]

# loop over the contours
    for c in cnts:
	# compute the center of the contour
	M = cv2.moments(c)
        area = int(M["m00"])
        if (area > 0):	
            cX = int(M["m10"] / M["m00"])
	    cY = int(M["m01"] / M["m00"])
        
	# draw the contour and center of the shape on the image
        if (area > 200):
	    cv2.drawContours(res_red, [c], -1, (0, 255, 0), 2)
	    cv2.circle(res_red, (cX, cY), 7, (255, 255, 255), -1)
	    cv2.putText(res_red, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


#    cv2.imshow('mask',red)
    cv2.imshow('red filter',res_red)

    cv2.waitKey(3)
	

if __name__ == '__main__':
    try:
        rospy.init_node('follower', anonymous=True)
    	rate = rospy.Rate(100) # 10hz
        rospy.Subscriber('/scan', LaserScan, lidarCallback)
        Follower()
    	while not rospy.is_shutdown():
			rospy.spin()


    except rospy.ROSInterruptException:
        pass
