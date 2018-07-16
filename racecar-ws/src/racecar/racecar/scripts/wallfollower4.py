#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from ackermann_msgs.msg import AckermannDriveStamped
from sensor_msgs.msg import LaserScan

def drive(x,th,t):
    
    pubb = rospy.Publisher('/vesc/ackermann_cmd_mux/output', AckermannDriveStamped, queue_size=1)
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

	dist_right = data.ranges[270]
        ahead = data.ranges[540]
        dist_left = data.ranges[810]
        if dist_right > dist_left:
            distance = 3-dist_left
	else:
            distance = dist_right

        if(ahead > 8):
            speed = 2.8        
        elif(ahead > 2):
            speed = 2.6
        elif(ahead > 2):
            speed = 1.0
        elif(ahead > 1):
            speed = 0.4
        elif(ahead > 0.1):
            speed = 0.2
        else:
            speed = 0.1

	if(distance > 1.5):
		rospy.loginfo("Driving right %f" % distance)
                if(distance > 2.4):
		    drive(speed, -1.0, 10)
                elif(distance > 2.3):
                    drive(speed, -0.9, 10)
                elif(distance > 2.1):
                    drive(speed, -0.7, 10)
                elif(distance > 1.9):
                    drive(speed, -0.4, 10)
                elif(distance > 1.7):
                    drive(speed, -0.2, 10)
                else:
                    drive(speed, -0.05, 10)
	else:
		rospy.loginfo("Driving left %f" % distance)
                if(distance < 0.1):
		    drive(-speed, 0.8, 10)
                elif(distance < 0.7):
                    drive(speed, 0.9, 10)
                elif(distance < 0.9):
                    drive(speed, 0.6, 10)
                elif(distance < 1.1):
                    drive(speed, 0.4, 10)
                elif(distance < 1.3):
                    drive(speed, 0.2, 10)
                else:
                    drive(speed, 0.05, 10)

                
	

if __name__ == '__main__':
    try:
        rospy.init_node('follower', anonymous=True)
    	rate = rospy.Rate(100) # 10hz
        rospy.Subscriber('/scan', LaserScan, lidarCallback)
    	while not rospy.is_shutdown():
			rospy.spin()


    except rospy.ROSInterruptException:
        pass
