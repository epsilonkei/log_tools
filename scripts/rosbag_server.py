#!/usr/bin/env python
# coding: UTF-8

# from log_tools.srv import *
import log_tools.srv
import rospy
import time

import subprocess

def rosbag_command_callback(rosbag_command):
    rospy.loginfo("rosbag_command_callback()")
    if rosbag_command.command == 'start':
        localtime = time.localtime()
        global filename = rosbag_command.filename + str(localtime.tm_year) + "-" + str(localtime.tm_mon) + "-" + str(localtime.tm_mday) + "-" + str(localtime.tm_hour) + "-" + str(localtime.tm_sec)
        rospy.loginfo("start recording rosbag")
        p = subprocess.Popen(["rosbag","record","-a","-O",filename])
    elif rosbag_command.command == 'stop':
        rospy.loginfo("stop recording rosbag")
        subprocess.Popen(["pkill","rosbag","-2"])
        subprocess.Popen(["pkill","record","-2"])
    else :
        rospy.loginfo("invalid command")

    return True

def rosbag_command_server():
    rospy.init_node('log_tools_rosbag_command_server')
    s = rospy.Service('rosbag_command', log_tools.srv.RosbagCommand, rosbag_command_callback)
    rospy.loginfo("Ready to record rosbag")
    rospy.spin()

rosbag_command_server()
if __name__ == "__main__":
    rosbag_command_server()

