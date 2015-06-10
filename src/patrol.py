#! /usr/bin/env python

import rospy
import sys
# Brings in the SimpleActionClient
import actionlib
import topological_navigation.msg
import scitos_ptu.msg
import flir_pantilt_d46.msg
from sensor_msgs.msg import JointState

class Patrol():

    def arrived_at_node_cb(self,*vals):
        rospy.loginfo("DONE")

    def active_cb(self):
        rospy.loginfo("ACTIVE")

    def feedback_cb(self):
        rospy.loginfo("FB")

    def cb_goto(self):
        rospy.loginfo("GOTO")

    def reset_gaze(self):
        rospy.loginfo("Trying to reset gaze")
        self.ptuClient = actionlib.SimpleActionClient('SetPTUState',flir_pantilt_d46.msg.PtuGotoAction)
        self.ptuClient.wait_for_server()

        goal = flir_pantilt_d46.msg.PtuGotoGoal()
        goal.pan = 0
        goal.tilt = 0
        goal.pan_vel = 1
        goal.tilt_vel = 1
        self.ptuClient.send_goal(goal)

    def look_at_table(self):
        rospy.loginfo("Trying to look at table")
        self.ptuClient = actionlib.SimpleActionClient('SetPTUState',flir_pantilt_d46.msg.PtuGotoAction)
        self.ptuClient.wait_for_server()

        goal = flir_pantilt_d46.msg.PtuGotoGoal()
        goal.pan = 0
        goal.tilt = 15
        goal.pan_vel = 1
        goal.tilt_vel = 1
        self.ptuClient.send_goal(goal)

    def move_to_waypoint(self,target):

        self.client = actionlib.SimpleActionClient('/topological_navigation', topological_navigation.msg.GotoNodeAction)
        self.client.wait_for_server()
        rospy.loginfo("Movement Requested to " + target)

        self.navgoal = topological_navigation.msg.GotoNodeGoal()
        self.navgoal.target = target

        # Sends the goal to the action server.
        self.client.send_goal(self.navgoal)#,self.done_cb, self.active_cb, self.feedback_cb)

        # Waits for the server to finish performing the action.
        self.client.wait_for_result()

        rospy.loginfo("Observing table")
        rospy.sleep(5)

        self.next_node()

    def next_node(self):
        if not self.tour:
            rospy.loginfo("Resetting Tour")
            self.tour = list(self.tables)

        self.move_to_waypoint(self.tour.pop())


    def __init__(self) :
        rospy.init_node('aloof_patrolling', anonymous = True)

        self.tables =['WayPoint10','WayPoint12','WayPoint1','WayPoint4','WayPoint8','WayPoint6']
        self.tour = []
        self.reset_gaze()
        self.look_at_table()
        
        self.next_node()



if __name__ == '__main__':
    p = Patrol()
