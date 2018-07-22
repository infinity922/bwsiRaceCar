#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from ackermann_msgs.msg import AckermannDriveStamped
from sensor_msgs.msg import LaserScan

# 0 to 1080 field of view is 240


import drivers
#I don't know many of these parameters yet

#returns ranges so that we know when to start turning. When the range is small, all of the lidar that is in those data ranges has passed the wall so we can can start to turn. May need to work on what the values should be
RightRange = max(data.ranges[540:560]) - min(data.ranges[540:560]) #right centre
LeftRange = max(data.ranges[520:540]) - min(data.ranges[520:540) #left centre

now = 0
now_set = False

#just need to mesure the wheelbase for this one. The equation requires it to be divided in two
WheelBase = 
WheelBase = WheelBase/2

def run(data):

    if abs(data.ranges[180] - data.ranges[900]) > 0.9: #left side and right side  
#basically if the difference is bigger than 0.9, positive or negitive
    	print('turn')
    	if data.ranges[leftcentre] > data.ranges[rightcentre]: #left center and right centre
        	print('left')
        	leftturn()
    	elif data.ranges[leftcentre] < data.ranges[rightcentre]: #left center and right centre
        	print('right')
        	rightturn()
    else:
        #go back to drive algorithum



def left_turn(data):
	global now
	global now_set
    speed = 0.8
    drivers.drivedecimal(data, 1, 0.8)
    turn_angle = WheelBase/(data.ranges[540] - min(data.ranges[leftside])
	if now_set == False:
	    now = data.ranges[540] 
		now_set = True
    if data.ranges[540] <= now + 0.5:
        drive(speed, turn_angle)
	else:
		now_set = False
   

def right_turn(data):
	global now
	global now_set
    speed = 0.8
    drivers.drivedecimal(data, 0, speed)
    turn_angle = WheelBase/(data.ranges[540] - min(data.ranges[rightside])
    now = data.ranges[540]      #is now mutable? Have to make it imutabke for the code to work. needs to be value at the current time
    if data.ranges[540] <= now + 0.5:  
        drive(speed, -turn_angle)
	else:
    	now_set = False

if __name__ == '__main__':
    try:
        rospy.init_node('driver', anonymous=True)
    	rate = rospy.Rate(100) # 20hz
        rospy.Subscriber('/scan', LaserScan, run)
    	while not rospy.is_shutdown():
			rospy.spin()


    except rospy.ROSInterruptException:
pass
