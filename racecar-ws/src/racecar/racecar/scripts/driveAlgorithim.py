#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from ackermann_msgs.msg import AckermannDriveStamped
from sensor_msgs.msg import LaserScan

import drivers


def run(data):
   drivers.drivecenter(data, 0.8)

if __name__ == '__main__':
    try:
        rospy.init_node('driver', anonymous=True)
    	rate = rospy.Rate(100) # 20hz
        rospy.Subscriber('/scan', LaserScan, run)
    	while not rospy.is_shutdown():
			rospy.spin()


    except rospy.ROSInterruptException:
        pass
