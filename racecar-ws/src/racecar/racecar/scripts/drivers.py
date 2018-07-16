#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from ackermann_msgs.msg import AckermannDriveStamped
from sensor_msgs.msg import LaserScan

lasterror = 0

# publishes to the robot
def drive(x, th):
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


# this calculates the steering angle based on the error given using a PD controller
# it is passed an error, a porportional gain, a derivitave gain, and a speed
def pd(error, pgain, dgain, speed):
    global lasterror    
    der = error - lasterror
    drive(speed, pgain * error + dgain * der)
    lasterror = error


# this drives the robot based on it's distance from the right wall
# it is passed the lidar data, the target distance from the right wall, and a speed
def driveright(data, distance, speed):
    error = min(data.ranges[200:540]) - distance
    pd(error, 1.5, 15, speed)


# this drives the robot based on it's distance from the left wall
# it is passed the lidar data, the target distance from the left wall, and a speed
def driveleft(data, distance, speed):
    error = min(data.ranges[540:880]) - distance
    pd(error, 1.5, 15, speed)


# this drives the robot in the middle of two walls
# it is passed the lidar data, and a speed
def drivecenter(data, speed):
    error = min(data.ranges[540:880]) - min(data.ranges[200:540])
    pd(error, 1.5, 15, speed)


# this drives the car between two walls with a decimal used as the position between the walls,
# 1 being the far left hand side of the track, 0 being the far right hand side.
# it is passed the lidar data, the decimal, and a speed
# !!! this is untested !!!
# !!! we should add a min distance from either wall, to prevent collisions !!!
def drivedecimal(data, decimal, speed):
    error = min(data.ranges[540:880])*decimal - min(data.ranges[200:540])*(1-decimal)
    pd(error, 1.5, 15, speed)


