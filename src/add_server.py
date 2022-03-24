#! /usr/bin/env python

import rospy

import actionlib

import addition_actionlib.msg

class add(object):
    _feedback = addition_actionlib.msg.addFeedback()
    _result = addition_actionlib.msg.addResult()

    def __init__(self,name):
        self.action_name = name
        self.action_server = actionlib.SimpleActionServer(self.action_name, addition_actionlib.msg.addAction, 
                                                          execute_cb = self.server_callback, auto_start = False)
        self.action_server.start()

    def server_callback(self, goal):
        r = rospy.Rate(1)
        success = True

        self._feedback.sum = 0

        rospy.loginfo("%s: Adding the numbers recieved")

        for i in range(len(goal.number)):
            if self.action_server.is_preempt_requested():
                rospy.loginfo("%s Preempted" % self.action_name)
                self.action_server.set_preempted()
                success = False
                break

            self._feedback.sum = goal.number[0] + goal.number[1]

            self.action_server.publish_feedback(self._feedback)

            r.sleep()

        if success:
            self._result.sum = self._feedback.sum
            rospy.loginfo('%s: Succeeded' % self.action_name)
            self.action_server.set_succeeded(self._result)

if __name__ == "__main__":
    rospy.init_node("whocares")
    server = add(rospy.get_name())
    rospy.spin()