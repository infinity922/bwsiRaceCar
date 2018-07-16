#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from ackermann_msgs.msg import AckermannDriveStamped
from sensor_msgs.msg import LaserScan

desired = 2
lasterror = 0


def drive(x, th, t):
    pubb = rospy.Publisher('/ackermann_cmd_mux/input/teleop', AckermannDriveStamped, queue_size=1)
    msg = AckermannDriveStamped();
    msg.header.stamp = rospy.Time.now();
    msg.header.frame_id = "base_link";

    msg.drive.speed = x;
    msg.drive.acceleration = 1;
    msg.drive.jerk = 1;
    msg.drive.steering_angle = th;
    msg.drive.steering_angle_velocity = 1;
    pubb.publish(msg)


# max 450* min 0*
def lidardatafind(data):

    return min(data.ranges[0:451])


def finderror(distance):
    return desired - distance


def deroferror(error):
    der = lasterror-error
    nonlocal.lasterror = error
    return der


def run(data):
    drive(0.3, (finderror(lidardatafind(data)))+(deroferror(finderror(lidardatafind(data)))), 10)


if __name__ == '__main__':
    try:
        rospy.init_node('follower', anonymous=True)
    	rate = rospy.Rate(100) # 10hz
        rospy.Subscriber('/scan', LaserScan, run)
    	while not rospy.is_shutdown():
			rospy.spin()


    except rospy.ROSInterruptException:
        pass
