#!/usr/bin/env python
# coding: UTF-8

# from log_tools.srv import *
import log_tools.srv
import rospy

import subprocess

def rosbag_command_callback(rosbag_command):
    print "rosbag_command_callback()"
    if rosbag_command.command == 'start':
        print "start recording rosbag"
        p = subprocess.Popen(["rosbag","record","-a"])
    elif rosbag_command.command == 'stop':
        print "stop recording rosbag"
        subprocess.Popen(["pkill","rosbag","-2"])
        subprocess.Popen(["pkill","record","-2"])
    else :
        print "invalid command"

    return True

def rosbag_command_server():
    rospy.init_node('log_tools_rosbag_command_server')
    s = rospy.Service('rosbag_command', log_tools.srv.RosbagCommand, rosbag_command_callback)
    print "Ready to record rosbag"
    rospy.spin()

rosbag_command_server()
if __name__ == "__main__":
    rosbag_command_server()

