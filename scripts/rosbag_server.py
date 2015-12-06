#!/usr/bin/env python
# coding: UTF-8

# from log_tools.srv import *
import log_tools.srv
import rospy
import rospkg

import time
import subprocess
import os

def create_file_name(filename):
    localtime = time.localtime()
    return filename + str(localtime.tm_year) + "-" + str(localtime.tm_mon) + "-" + str(localtime.tm_mday) + "-" + str(localtime.tm_hour) + "-" + str(localtime.tm_sec)

def rosbag_command_callback(rosbag_command):
    rospy.loginfo("rosbag_command_callback()")
    # start recording
    if rosbag_command.command == 'start':
        global filename0
        filename0 = create_file_name(rosbag_command.filename)
        rospy.loginfo("start recording rosbag")
        p = subprocess.Popen(["rosbag","record","-a","-O",filename0])
    # stop recording and save log
    elif rosbag_command.command == 'stop':
        rospy.loginfo("stop recording rosbag")
        subprocess.Popen(["pkill","rosbag","-2"])
        subprocess.Popen(["pkill","record","-2"])
        global filename1
        if rosbag_command.filename != "":
            filename1 = create_file_name(rosbag_command.filename)
        else:
            filename1 = filename0
        # move bagfile
        if rosbag_command.path != "":
            os.system("mkdir -p " + rosbag_command.path)
            while not os.path.exists(os.path.join(rospkg.get_ros_home(),filename0) + ".bag"):
                time.sleep(0.001)
            os.system("mv " + os.path.join(rospkg.get_ros_home(),filename0) + ".bag " + os.path.join(rosbag_command.path,filename1) + ".bag")
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

