#! /usr/bin/env python

from __future__ import print_function
import rospy
import sys

import actionlib

import addition_actionlib.msg

def add_client():
    client = actionlib.SimpleActionClient('whocares', addition_actionlib.msg.addAction)
    client.wait_for_server()

    goal = addition_actionlib.msg.addGoal(number = [0,1])
    print("goal published %i %i" % (goal.number[0], goal.number[1]))

    client.send_goal(goal)
    client.wait_for_result()

    return client.get_result()

if __name__ == '__main__':
    try:
        rospy.init_node('noonecares')
        result = add_client()   
        print("Result",result)

    except rospy.ROSInterruptException:
        print("program interupted before completion", file = sys.stderr)