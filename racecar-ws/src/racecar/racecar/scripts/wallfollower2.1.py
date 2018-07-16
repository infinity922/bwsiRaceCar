#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from ackermann_msgs.msg import AckermannDriveStamped
from sensor_msgs.msg import LaserScan

def drive(x,th,t):
    
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
    
    

def lidarCallback(data):
	distance = data.ranges[270]
	if(distance > 3):
		rospy.loginfo("Driving right %f" % distance)
		drive(0.2, -0.1, 10)
	else:
		rospy.loginfo("Driving left %f" % distance)
		drive(0.2, 0.1, 10)
	

if __name__ == '__main__':
    try:
        rospy.init_node('follower', anonymous=True)
    	rate = rospy.Rate(100) # 10hz
        rospy.Subscriber('/scan', LaserScan, lidarCallback)
    	while not rospy.is_shutdown():
			rospy.spin()


    except rospy.ROSInterruptException:
        pass
