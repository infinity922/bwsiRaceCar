#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from ackermann_msgs.msg import AckermannDriveStamped
from sensor_msgs.msg import LaserScan

desired = .5
lasterror = 0


def drive(x, th, t):
    pubb = rospy.Publisher('/ackermann_cmd_mux/input/default', AckermannDriveStamped, queue_size=1)
    msg = AckermannDriveStamped();
    msg.header.stamp = rospy.Time.now();
    msg.header.frame_id = "base_link";

    msg.drive.speed = x;
    msg.drive.acceleration = 0;
    msg.drive.jerk = 0;
    msg.drive.steering_angle = th;
    msg.drive.steering_angle_velocity = 0;
    pubb.publish(msg)


# max 450* min 0*
def lidardatafind(data):
    
    return min(data.ranges[200:550])


def finderror(distance, data):
    
    return min(data.ranges[1350:1600] - distance

def  deroferror(error):

    global lasterror
    der = lasterror-error
    lasterror = error
    
    return der


def run(data):
    if data.ranges[600] < 1:
        # drive(1.2, 1, 10)
    else:
        drive(5, (finderror(lidardatafind(data), data))*1.5+(-15)*(deroferror(finderror(lidardatafind(data), data))), 10)


if __name__ == '__main__':
    try:
        rospy.init_node('follower', anonymous=True)
    	rate = rospy.Rate(100) # 20hz
        rospy.Subscriber('/scan', LaserScan, run)
    	while not rospy.is_shutdown():
			rospy.spin()


    except rospy.ROSInterruptException:
        pass
