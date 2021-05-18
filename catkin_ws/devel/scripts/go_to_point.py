#! /usr/bin/env python

# import ros stuff
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
from tf import transformations

import math
#And also define some variables: publisher, robot state, machine state, goal position and some tune parameters:

# robot state variables
position_ = Point()
yaw_ = 0
# machine state
state_ = 0
# goal
desired_position_ = Point()
desired_position_.x = -3
desired_position_.y = 7
desired_position_.z = 0
# parameters
yaw_precision_ = math.pi / 90 # +/- 2 degree allowed
dist_precision_ = 0.3

# publishers
pub = None

def main():
    global pub
    
    rospy.init_node('go_to_point')
    
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    
    sub_odom = rospy.Subscriber('/odom', Odometry, clbk_odom)
    
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        if state_ == 0:
            fix_yaw(desired_position_)
        elif state_ == 1:
            go_straight_ahead(desired_position_)
        elif state_ == 2:
            done()
            pass
        else:
            rospy.logerr('Unknown state!')
            pass
        rate.sleep()

if __name__ == '__main__':
    main()