#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from ackermann_msgs.msg import AckermannDriveStamped
from sensor_msgs.msg import LaserScan

import drivers
i = 0
turndir = 0
walldist = 0

def run(data):
    global i
    global turndir
    global walldist
    speed = 0
    if data.ranges[540] < 0.75:
        speed = 1.5*data.ranges[540]/0.75
    else:
        speed = 1.5
    drivers.drivecenter(data, speed)
        
    """print(turndir)
    if min(data.ranges[200:880]) < 0.1:
        drivers.stop()
    elif turndir == 0:
        print('goingforth')
        drivers.drivecenter(data, 0.8)
    rightm = (sum(data.ranges[440:540]) / len(data.ranges[440:540]))
    leftm = (sum(data.ranges[540:640]) / len(data.ranges[540:640]))
    if abs(rightm - leftm) > 0.5:
        if rightm > leftm:
            print('rightturn')
            
    
        else:
            print('left turn')
            if turndir == 0:
                drivers.drivedecimal(data, 1, 1.2)
                turndir = -1
                walldist = data.ranges[756]
                
        i=i+1
        print('turning', i) 
    if turndir == -1:
        drivers.drivedecimal(data, 1, 1.2)
        if abs(data.ranges[756] - walldist) >1:
            
            turndir = 0   """
        
if __name__ == '__main__':
    try:
        rospy.init_node('driver', anonymous=True)
    	rate = rospy.Rate(100) # 20hz
        rospy.Subscriber('/scan', LaserScan, run)
    	while not rospy.is_shutdown():
			rospy.spin()


    except rospy.ROSInterruptException:
        pass
