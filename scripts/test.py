#!/usr/bin/env python2
"""Testing arm movement. 
"""

import sys
import copy 
import rospy 
import moveit_commander 
import moveit_msgs.msg
import geometry_msgs.msg

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('testing_movement', anonymous=True)

robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()

group = moveit_commander.MoveGroupCommander('arm')

display_trajectory_publisher = rospy.Publisher(
				'/move_group/display_planned_path',
				moveit_msgs.msg.DisplayTrajectory,
				queue_size=20)	

print 'Waiting for RVIZ...'
rospy.sleep(4)
print 'Starting'

print 'Reference Frame: %s' % group.get_planning_frame()
print 'Printing Robot State...'
print robot.get_current_state()

print 'Generating Plan'
pose_target = geometry_msgs.msg.Pose()
pose_target.orientation.w = 1.0
pose_target.orientation.x = 0.7 
pose_target.orientation.y = -0.05 
pose_target.orientation.z = 1.1 
group.set_pose_target(pose_target)

plan1 = group.plan()
print 'Waiting while plan 1 is being displayed'
rospy.sleep(4)

group.clear_pose_targets()
group_variable_values = group.get_current_joint_values()
print 'Current Joint Values', group_variable_values

group_variable_values[1] = 1.0
group.set_joint_value_target(group_variable_values)
plan2 = group.plan()
print 'Waiting while plan 2 is being displayed'
rospy.sleep(5)

moveit_commander.roscpp_shutdown()
