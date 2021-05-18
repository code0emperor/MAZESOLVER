#! /usr/bin/env python

import rospy

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
pub = None

def clbk_laser(msg):
    regions = {
        'right':  min(min(msg.ranges[0:143]), 10),
        'frontright': min(min(msg.ranges[144:287]), 10),
        'frontront':  min(min(msg.ranges[288:431]), 10),
        'frontleft':  min(min(msg.ranges[432:575]), 10),
        'left':   min(min(msg.ranges[576:719]), 10),
    }
    
    take_action(regions)
    
def take_action(regions):
    msg = Twist()
    linear_x = 0
    angular_z = 0
    
    state_description = ''
    
    if regions['front'] > 1 and regions['frontleft'] > 1 and regions['frontright'] > 1:
        state_description = 'case 1 - nothing'
        linear_x = 0.6
        angular_z = 0
    elif regions['front'] < 1 and regions['frontleft'] > 1 and regions['frontright'] > 1:
        state_description = 'case 2 - front'
        linear_x = 0
        angular_z = 0.3
    elif regions['front'] > 1 and regions['frontleft'] > 1 and regions['frontright'] < 1:
        state_description = 'case 3 - frontright'
        linear_x = 0
        angular_z = 0.3
    elif regions['front'] > 1 and regions['frontleft'] < 1 and regions['frontright'] > 1:
        state_description = 'case 4 - frontleft'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] < 1 and regions['frontleft'] > 1 and regions['frontright'] < 1:
        state_description = 'case 5 - front and frontright'
        linear_x = 0
        angular_z = 0.3
    elif regions['front'] < 1 and regions['frontleft'] < 1 and regions['frontright'] > 1:
        state_description = 'case 6 - front and frontleft'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] > 1 and regions['frontleft'] < 1 and regions['frontright'] < 1:
        state_description = 'case 7 - frontleft and frontright'
        linear_x = 0.3
        angular_z = 0
    elif regions['front'] < 1 and regions['frontleft'] < 1 and regions['frontright'] < 1:
        state_description = 'case 8 - front and frontleft and frontright'
        linear_x = 0
        angular_z = 0.3
    
    else:
        state_description = 'unknown case'
        rospy.loginfo(regions)

    rospy.loginfo(state_description)
    msg.linear.x = linear_x
    msg.angular.z = angular_z
    pub.publish(msg)

def main():
    global pub
    
    rospy.init_node('reading_laser')
    
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    
    sub = rospy.Subscriber('/m2wr/laser/scan', LaserScan, clbk_laser)
    
    rospy.spin()

if __name__ == '__main__':
    main()
