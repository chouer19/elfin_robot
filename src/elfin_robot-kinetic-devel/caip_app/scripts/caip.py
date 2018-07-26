#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Monday July 09 11:36:59 2018

@author: Chong Xue

 Software License Agreement (BSD License)

 Copyright (c) 2018, CAIP Co., Ltd.
 All rights reserved.

 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions
 are met:

  * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
  * Redistributions in binary form must reproduce the above
    copyright notice, this list of conditions and the following
    disclaimer in the documentation and/or other materials provided
    with the distribution.
  * Neither the name of the copyright holders nor the names of its
    contributors may be used to endorse or promote products derived
    from this software without specific prior written permission.

 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 POSSIBILITY OF SUCH DAMAGE.
 
"""
# author: Chong Xue

from __future__ import division
import rospy
import math
import tf
import moveit_commander
from std_msgs.msg import Bool, String, Int64
from std_srvs.srv import SetBool, SetBoolRequest, SetBoolResponse
from elfin_robot_msgs.srv import SetString, SetStringRequest, SetStringResponse
from elfin_robot_msgs.srv import SetInt16, SetInt16Request
import wx
from sensor_msgs.msg import JointState
from actionlib import SimpleActionClient
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from control_msgs.msg import JointTrajectoryControllerState
from geometry_msgs.msg import PoseStamped, PoseArray, Pose
from trajectory_msgs.msg import trajectory_msgs
import threading
import dynamic_reconfigure.client
from dynamic_reconfigure.srv import Reconfigure, ReconfigureRequest
from dynamic_reconfigure.msg import DoubleParameter, Config
import time
import sys

def testcaip(num, num2, num3, num4, num5, num6):
    #print(num)
    caip = CaipElfin()
    #print(caip.JointState)
    caip.listen()
    print('start')
    for i in range(0,10):
        #print('come in function "call_ref_coordinate()"')
        time.sleep(0.4)
        #caip.want_end_coordinate()
        #print(caip.EndCoordinate)
        caip.want_stop()
        
        name=['elfin_joint1', 'elfin_joint2', 'elfin_joint3',
              'elfin_joint4', 'elfin_joint5', 'elfin_joint6']
        pos = [i*5 / 180 * math.pi] * 6
        #print(num)
        if num == 0:
            caip.do_joints_goal(name,pos)
        elif num == 1:
            caip.do_cart_goal(0.10 + i * 0.05, 0.10 + i * 0.06, 0.7 - 0.06 * i, 0,0,0,1 )
        elif num == 2:
            caip.set_cart_path()
            caip.do_cart_path()
        elif num == 3:
            caip.want_joint(num2)
            caip.want_joint(num3)
        elif num == 4:
            caip.want_home()
        elif num == 5:
            caip.want_cart(num2)
        elif num == 6:
            caip.do_joint_cmd(num2)

    caip.want_stop()
    print('end')
    pass

class CaipElfin():

    def __init__(self):
        # The current status of the joints.
        self.JointState = JointTrajectoryControllerState()

        # The servo power's status of the robot.
        self.ServoPowerState = Bool()

        # The fault power's status of the robot.
        self.PowerFaultState = Bool()

        # The reference coordinate in the calculations of the elfin_basic_api node
        self.RefCoordinate = String()

        # The end coordinate in the calculations of the elfin_basic_api node
        self.EndCoordinate = String()

        #The value of the dynamic parameters of elfin_basic_api, e.g. velocity scaling.
        self.DynamicArgs = Config()

        # get the reference coordinate name of elfin_basic_api from the response of this service.
        self.call_ref_coordinate = rospy.ServiceProxy('elfin_basic_api/get_reference_link', SetBool)
        self.call_ref_coordinate_req = SetBoolRequest()

        # get the end coordinate name of elfin_basic_api from the response of this service.
        self.call_end_coordinate = rospy.ServiceProxy('elfin_basic_api/get_end_link', SetBool)
        self.call_end_coordinate_req = SetBoolRequest()

        self.JointsPub = rospy.Publisher('elfin_basic_api/joint_goal', JointState, queue_size=1)
        self.JointsGoal = JointState()

        self.CartGoalPub = rospy.Publisher('elfin_basic_api/cart_goal', PoseStamped, queue_size=1)
        self.CartPos = PoseStamped()

        self.CartPathPub = rospy.Publisher('elfin_basic_api/cart_path_goal', PoseArray, queue_size=1)
        self.CartPath = PoseArray()
        self.CartPath.header.stamp=rospy.get_rostime()
        self.CartPath.header.frame_id='elfin_base_link'

        self.JointCmdPub = rospy.Publisher('elfin_teleop_joint_cmd_no_limit', Int64 , queue_size=1)
        self.JointCmd = Int64()

        self.action_client = SimpleActionClient('elfin_module_controller/follow_joint_trajectory',
                                              FollowJointTrajectoryAction)
        self.action_goal = FollowJointTrajectoryGoal()
        #self.goal_list = JointTrajectoryPoint()
        self.goal_list = []

    
        self.call_teleop_stop=rospy.ServiceProxy('elfin_basic_api/stop_teleop', SetBool)
        self.call_teleop_stop_req=SetBoolRequest()


        self.call_teleop_joint=rospy.ServiceProxy('elfin_basic_api/joint_teleop',SetInt16)
        self.call_teleop_joint_req=SetInt16Request()


        self.call_teleop_cart=rospy.ServiceProxy('elfin_basic_api/cart_teleop', SetInt16)
        self.call_teleop_cart_req=SetInt16Request()

 
        self.call_move_homing=rospy.ServiceProxy('elfin_basic_api/home_teleop', SetBool)
        self.call_move_homing_req=SetBoolRequest()

        pass

    def want_joint(self,data):
        self.call_teleop_joint_req.data = data
        resp=self.call_teleop_joint.call(self.call_teleop_joint_req)
        print(resp)

    def want_home(self):
        print('homehomehome')
        self.call_move_homing_req.data = True
        resp=self.call_move_homing.call(self.call_move_homing_req)
        print(resp)

    def want_cart(self, data):
        self.call_teleop_cart_req.data =data
        resp=self.call_teleop_cart.call(self.call_teleop_cart_req)
        print(resp)

    def want_stop(self):
        self.call_teleop_stop_req.data=True
        resp=self.call_teleop_stop.call(self.call_teleop_stop_req)
        print(resp)

    def set_joint_cmd(self, data=None):
        if data is not None:
            self.JointCmd.data = data
        else:
            self.JointCmd.data = 0

    def do_joint_cmd(self, data=None):
        if data is not None:
            cmd = Int64()
            cmd.data = data
            self.JointCmdPub.publish(cmd)
        else:
            self.JointCmdPub.publish(self.JointCmd)
        pass

    def set_cart_path(self):
        ps=Pose()
        ps.position.x=0.264
        ps.position.y=0.125
        ps.position.z=1.143
        ps.orientation.x=0
        ps.orientation.y=0
        ps.orientation.z=0
        ps.orientation.w=1

        ps1=Pose()
        ps1.position.x=0.324
        ps1.position.y=0.245
        ps1.position.z=1.143
        ps1.orientation.x=0
        ps1.orientation.y=0
        ps1.orientation.z=0
        ps1.orientation.w=1

        ps2=Pose()
        ps2.position.x=0.504
        ps2.position.y=0.330
        ps2.position.z=1.143
        ps2.orientation.x=0
        ps2.orientation.y=0
        ps2.orientation.z=0
        ps2.orientation.w=1

        ps3=Pose()
        ps3.position.x=0.505
        ps3.position.y=0.225
        ps3.position.z=1.143
        ps3.orientation.x=0
        ps3.orientation.y=0
        ps3.orientation.z=0
        ps3.orientation.w=1

        self.CartPath.poses.append(ps)
        self.CartPath.poses.append(ps1)
        self.CartPath.poses.append(ps2)
        #self.CartPath.poses.append(ps3)
        #self.CartPath.poses.append(ps1)
        pass

    def do_cart_path(self,path=None):
        if path is not None:
            self.CartPathPub.publish(path)
        else:
            self.CartPathPub.publish(self.CartPath)

    def set_cart_pos(self,x,y,z,ox,oy,oz,ow):
        self.CartPos.header.stamp=rospy.get_rostime()
        self.CartPos.header.frame_id='elfin_base_link'
        self.CartPos.pose.position.x=x
        self.CartPos.pose.position.y=y
        self.CartPos.pose.position.z=z
        self.CartPos.pose.orientation.x=ox
        self.CartPos.pose.orientation.y=oy
        self.CartPos.pose.orientation.z=oz
        self.CartPos.pose.orientation.w=ow
        pass

    def set_action_goal(self, name = None, goal_list = None):
        if name is not None and goal_list is not None:
            self.action_goal.trajectory.joint_names = name
            self.action_goal.trajectory.points = goal_list
        else:
            point_goal=JointTrajectoryPoint()
            point_goal.positions=[0.4, -0.5]
            point_goal.velocities=[0, 0]
            point_goal.accelerations=[0, 0]
            point_goal.time_from_start=rospy.Time(secs=2, nsecs=0)
            self.action_goal.trajectory.points.append(point_goal)

        self.action_goal.trajectory.header.stamp.secs=0
        self.action_goal.trajectory.header.stamp.nsecs=0
        pass

    def do_action_goal(self, action_goal = None):
        self.action_client.wait_for_server()
        if action_goal is None:
            self.action_client.send_goal(self.action_goal)
            self.action_goal.trajectory.points=[]
        else:
            self.action_client.send_goal(self.action_goal)

        pass

    def do_cart_goal(self,x=None, y=None, z=None, ox=None, oy=None, oz=None, ow=None):
        if x is None or y is None or z is None or ox is None or oy is None or oz is None or ow is None:
             pass
        else:
            self.set_cart_pos(x,y,z,ox,oy,oz,ow)
        self.CartGoalPub.publish(self.CartPos)
        pass

    def set_joints_goal(self, name=None, pos=None):
        if name is None:
            name=['elfin_joint1', 'elfin_joint2', 'elfin_joint3',
                 'elfin_joint4', 'elfin_joint5', 'elfin_joint6']
        if pos is not None:
            name=['elfin_joint1', 'elfin_joint2', 'elfin_joint3',
                 'elfin_joint4', 'elfin_joint5', 'elfin_joint6']
            name = name[:len(pos)]
        else:
            pos = [0.4, 0.4, 0.4, 0.4, 0.4, 0.4]
        self.JointsGoal.name = name
        self.JointsGoal.position = pos
        self.JointsGoal.header.stamp=rospy.get_rostime()

    def do_joints_goal(self, name=None, pos=None):
        if name is not None and pos is not None:
            self.set_joints_goal(name, pos)
        elif pos is not None:
            name=['elfin_joint1', 'elfin_joint2', 'elfin_joint3',
                 'elfin_joint4', 'elfin_joint5', 'elfin_joint6']
            name = name[:len(pos)]
            self.set_joints_goal(name, pos)
        self.JointsPub.publish(self.JointsGoal)

    def want_end_coordinate(self):
        self.call_end_coordinate_req.data = True
        resp = self.call_end_coordinate.call(self.call_end_coordinate_req)
        if resp.success:
            self._end_coordinate(resp)
        #print(resp)

    def want_ref_coordinate(self):
        self.call_ref_coordinate_req.data = True
        resp = self.call_ref_coordinate.call(self.call_ref_coordinate_req)
        if resp.success:
            self._ref_coordinate(resp)
        #print(resp)

    def _joints_state(self, data):
         self.JointState = data
         #print(self.JointState)

    def get_joints_state(self):
         return self.JointState

    def _servo_power_state(self, data):
         self.ServoPowerState = data.data
         #print(data.data)

    def get_servo_power_state(self):
         return self.ServoPowerState

    def _power_fault_state(self,data):
        self.PowerFaultState = data.data
        #print(self.PowerFaultState)

    def get_power_fault_state(self):
        return self.PowerFaultState

    def _ref_coordinate(self,data):
        if hasattr(data, 'message'):
            self.RefCoordinate = data.message
        else:
            self.RefCoordinate = data.data
        #print(self.RefCoordinate)

    def get_ref_coordinate(self):
        return self.RefCoordinate

    def _end_coordinate(self,data):
        if hasattr(data, 'message'):
            self.EndCoordinate = data.message
        else:
            self.EndCoordinate = data.data
        #print(self.EndCoordinate)

    def get_end_coordinate(self):
        return self.EndCoordinate

    def _dynamic_args(self,data):
        self.DynamicArgs = data
        #print(self.DynamicArgs)
        
    def get_dynamic_args(self,data):
        return self.DynamicArgs
        
    def listen(self):
        rospy.Subscriber('elfin_arm_controller/state', JointTrajectoryControllerState, self._joints_state)
        rospy.Subscriber('elfin_ros_control/elfin/enable_state', Bool, self._servo_power_state)
        rospy.Subscriber('elfin_ros_control/elfin/fault_state', Bool, self._power_fault_state)
        rospy.Subscriber('elfin_basic_api/reference_link_name', String, self._ref_coordinate)
        rospy.Subscriber('elfin_basic_api/end_link_name', String, self._end_coordinate)
        rospy.Subscriber('elfin_basic_api/parameter_updates', Config, self._dynamic_args)
        pass

class MyFrame(wx.Frame):  
  
    def __init__(self,parent,id):  
        the_size=(700, 570)
        wx.Frame.__init__(self,parent,id,'Elfin Control Panel',pos=(250,100)) 
        self.panel=wx.Panel(self)
        font=self.panel.GetFont()
        font.SetPixelSize((12, 24))
        self.panel.SetFont(font)
        
        self.listener = tf.TransformListener()
        
        self.robot=moveit_commander.RobotCommander()
        self.scene=moveit_commander.PlanningSceneInterface()
        self.group=moveit_commander.MoveGroupCommander('elfin_arm')

        self.controller_ns='elfin_arm_controller/'
        self.elfin_driver_ns='elfin_ros_control/elfin/'
        
        self.elfin_basic_api_ns='elfin_basic_api/'
        
        self.joint_names=rospy.get_param(self.controller_ns+'joints', [])
        
        self.ref_link_name=self.group.get_planning_frame()
        self.end_link_name=self.group.get_end_effector_link()
        
        self.ref_link_lock=threading.Lock()
        self.end_link_lock=threading.Lock()
                
        self.js_display=[0]*6 # joint_states
        self.jm_button=[0]*6 # joints_minus
        self.jp_button=[0]*6 # joints_plus
        self.js_label=[0]*6 # joint_states
                      
        self.ps_display=[0]*6 # pcs_states
        self.pm_button=[0]*6 # pcs_minus
        self.pp_button=[0]*6 # pcs_plus
        self.ps_label=[0]*6 # pcs_states
                      
        self.display_init()
        self.key=[]
                                
        btn_height=390
        btn_lengths=[]
                
        self.power_on_btn=wx.Button(self.panel, label=' Servo On ', name='Servo On',
                                    pos=(20, btn_height))
        btn_lengths.append(self.power_on_btn.GetSize()[0])
        btn_total_length=btn_lengths[0]
        
        self.power_off_btn=wx.Button(self.panel, label=' Servo Off ', name='Servo Off')
        btn_lengths.append(self.power_off_btn.GetSize()[0])
        btn_total_length+=btn_lengths[1]
        
        self.reset_btn=wx.Button(self.panel, label=' Clear Fault ', name='Clear Fault')
        btn_lengths.append(self.reset_btn.GetSize()[0])
        btn_total_length+=btn_lengths[2]

        self.home_btn=wx.Button(self.panel, label='Home', name='home_btn')
        btn_lengths.append(self.home_btn.GetSize()[0])
        btn_total_length+=btn_lengths[3]
        
        self.stop_btn=wx.Button(self.panel, label='Stop', name='Stop')
        btn_lengths.append(self.stop_btn.GetSize()[0])
        btn_total_length+=btn_lengths[4]
        
        btn_interstice=(550-btn_total_length)/4
        btn_pos_tmp=btn_lengths[0]+btn_interstice+20
        self.power_off_btn.SetPosition((btn_pos_tmp, btn_height))
        
        btn_pos_tmp+=btn_lengths[1]+btn_interstice
        self.reset_btn.SetPosition((btn_pos_tmp, btn_height))
        
        btn_pos_tmp+=btn_lengths[2]+btn_interstice
        self.home_btn.SetPosition((btn_pos_tmp, btn_height))
        
        btn_pos_tmp+=btn_lengths[3]+btn_interstice
        self.stop_btn.SetPosition((btn_pos_tmp, btn_height))
        
        self.servo_state_label=wx.StaticText(self.panel, label='Servo state:',
                                              pos=(590, btn_height-10))
        self.servo_state_show=wx.TextCtrl(self.panel, style=(wx.TE_CENTER |wx.TE_READONLY),
                                    value='', pos=(600, btn_height+10))
        self.servo_state=bool()
        
        self.fault_state_label=wx.StaticText(self.panel, label='Fault state:',
                                              pos=(590, btn_height+60))
        self.fault_state_show=wx.TextCtrl(self.panel, style=(wx.TE_CENTER |wx.TE_READONLY),
                                    value='', pos=(600, btn_height+80))
        self.fault_state=bool()
        
        self.reply_show_label=wx.StaticText(self.panel, label='Result:',
                                           pos=(20, btn_height+120))
        self.reply_show=wx.TextCtrl(self.panel, style=(wx.TE_CENTER |wx.TE_READONLY),
                                    value='', size=(670, 30), pos=(20, btn_height+140))
        
        link_textctrl_length=(btn_pos_tmp-40)/2
        
        self.ref_links_show_label=wx.StaticText(self.panel, label='Ref. link:',
                                                    pos=(20, btn_height+60))
        
        self.ref_link_show=wx.TextCtrl(self.panel, style=(wx.TE_READONLY),
                                           value=self.ref_link_name, size=(link_textctrl_length, 30),
                                           pos=(20, btn_height+80))
        
        self.end_link_show_label=wx.StaticText(self.panel, label='End link:',
                                               pos=(link_textctrl_length+30, btn_height+60))
        
        self.end_link_show=wx.TextCtrl(self.panel, style=(wx.TE_READONLY),
                                       value=self.end_link_name, size=(link_textctrl_length, 30),
                                       pos=(link_textctrl_length+30, btn_height+80))
        
        self.set_links_btn=wx.Button(self.panel, label='Set links', name='Set links')
        self.set_links_btn.SetPosition((btn_pos_tmp, btn_height+75))
        
        # the variables about velocity scaling
        velocity_scaling_init=rospy.get_param(self.elfin_basic_api_ns+'velocity_scaling',
                                              default=0.4)
        default_velocity_scaling=str(round(velocity_scaling_init, 2)) 

        self.velocity_setting_label=wx.StaticText(self.panel, label='Velocity Scaling',
                                                  pos=(20, btn_height-70))
        self.velocity_setting=wx.Slider(self.panel, value=int(velocity_scaling_init*100),
                                        minValue=1, maxValue=100,
                                        style = wx.SL_HORIZONTAL,
                                        size=(500, 30),
                                        pos=(45, btn_height-50))
        self.velocity_setting_txt_lower=wx.StaticText(self.panel, label='1%',
                                                    pos=(20, btn_height-45))
        self.velocity_setting_txt_upper=wx.StaticText(self.panel, label='100%',
                                                    pos=(550, btn_height-45))
        self.velocity_setting_show=wx.TextCtrl(self.panel, 
                                               style=(wx.TE_CENTER|wx.TE_READONLY), 
                                                value=default_velocity_scaling,
                                                pos=(600, btn_height-55))
        self.velocity_setting.Bind(wx.EVT_SLIDER, self.velocity_setting_cb)
        self.teleop_api_dynamic_reconfig_client=dynamic_reconfigure.client.Client(self.elfin_basic_api_ns,
                                                                                  config_callback=self.basic_api_reconfigure_cb)
        
        self.dlg=wx.Dialog(self.panel, title='messag')
        self.dlg.Bind(wx.EVT_CLOSE, self.closewindow)
        self.dlg_panel=wx.Panel(self.dlg)
        self.dlg_label=wx.StaticText(self.dlg_panel, label='hello', pos=(15, 15))
        
        self.set_links_dlg=wx.Dialog(self.panel, title='Set links', size=(400, 100))
        self.set_links_dlg_panel=wx.Panel(self.set_links_dlg)
        
        self.sld_ref_link_show=wx.TextCtrl(self.set_links_dlg_panel, style=wx.TE_PROCESS_ENTER,
                                           value='', pos=(20, 20), size=(link_textctrl_length, 30))
        self.sld_end_link_show=wx.TextCtrl(self.set_links_dlg_panel, style=wx.TE_PROCESS_ENTER,
                                           value='', pos=(20, 70), size=(link_textctrl_length, 30))
        
        self.sld_set_ref_link_btn=wx.Button(self.set_links_dlg_panel, label='Update ref. link',
                                            name='Update ref. link')
        self.sld_set_ref_link_btn.SetPosition((link_textctrl_length+30, 15))
        self.sld_set_end_link_btn=wx.Button(self.set_links_dlg_panel, label='Update end link',
                                            name='Update end link')
        self.sld_set_end_link_btn.SetPosition((link_textctrl_length+30, 65))
        
        self.set_links_dlg.SetSize((link_textctrl_length+self.sld_set_ref_link_btn.GetSize()[0]+50, 120))
        
                        
        self.call_teleop_joint=rospy.ServiceProxy(self.elfin_basic_api_ns+'joint_teleop', 
                                                  SetInt16)
        self.call_teleop_joint_req=SetInt16Request()
        
        self.call_teleop_cart=rospy.ServiceProxy(self.elfin_basic_api_ns+'cart_teleop', 
                                                 SetInt16)
        self.call_teleop_cart_req=SetInt16Request()
        
        self.call_teleop_stop=rospy.ServiceProxy(self.elfin_basic_api_ns+'stop_teleop', 
                                                 SetBool)
        self.call_teleop_stop_req=SetBoolRequest()
        
        self.call_stop=rospy.ServiceProxy(self.elfin_basic_api_ns+'stop_teleop', 
                                          SetBool)
        self.call_stop_req=SetBoolRequest()
        self.call_stop_req.data=True
        self.stop_btn.Bind(wx.EVT_BUTTON, 
                           lambda evt, cl=self.call_stop,
                           rq=self.call_stop_req :
                           self.call_set_bool_common(evt, cl, rq))
            
        self.call_reset=rospy.ServiceProxy(self.elfin_driver_ns+'clear_fault', SetBool)
        self.call_reset_req=SetBoolRequest()
        self.call_reset_req.data=True
        self.reset_btn.Bind(wx.EVT_BUTTON, 
                           lambda evt, cl=self.call_reset,
                           rq=self.call_reset_req :
                           self.call_set_bool_common(evt, cl, rq))
                
        self.call_power_on=rospy.ServiceProxy(self.elfin_driver_ns+'enable_robot', SetBool)
        self.call_power_on_req=SetBoolRequest()
        self.call_power_on_req.data=True
        self.power_on_btn.Bind(wx.EVT_BUTTON, 
                               lambda evt, cl=self.call_power_on,
                               rq=self.call_power_on_req :
                               self.call_set_bool_common(evt, cl, rq))
        
        self.call_power_off=rospy.ServiceProxy(self.elfin_driver_ns+'disable_robot', SetBool)
        self.call_power_off_req=SetBoolRequest()
        self.call_power_off_req.data=True
        self.power_off_btn.Bind(wx.EVT_BUTTON, 
                               lambda evt, cl=self.call_power_off,
                               rq=self.call_power_off_req :
                               self.call_set_bool_common(evt, cl, rq))
                
        self.call_move_homing=rospy.ServiceProxy(self.elfin_basic_api_ns+'home_teleop', 
                                                 SetBool)
        self.call_move_homing_req=SetBoolRequest()
        self.call_move_homing_req.data=True
        self.home_btn.Bind(wx.EVT_LEFT_DOWN, 
                           lambda evt, cl=self.call_move_homing,
                           rq=self.call_move_homing_req :
                           self.call_set_bool_common(evt, cl, rq))
        self.home_btn.Bind(wx.EVT_LEFT_UP,
                           lambda evt, mark=100:
                           self.release_button(evt, mark) )
            
        self.call_set_ref_link=rospy.ServiceProxy(self.elfin_basic_api_ns+'set_reference_link', SetString)
        self.call_set_end_link=rospy.ServiceProxy(self.elfin_basic_api_ns+'set_end_link', SetString)
        self.set_links_btn.Bind(wx.EVT_BUTTON, self.show_set_links_dialog)
        
        self.sld_set_ref_link_btn.Bind(wx.EVT_BUTTON, self.update_ref_link)
        self.sld_set_end_link_btn.Bind(wx.EVT_BUTTON, self.update_end_link)
        
        self.sld_ref_link_show.Bind(wx.EVT_TEXT_ENTER, self.update_ref_link)
        self.sld_end_link_show.Bind(wx.EVT_TEXT_ENTER, self.update_end_link)
            
        self.action_client=SimpleActionClient(self.controller_ns+'follow_joint_trajectory',
                                              FollowJointTrajectoryAction)
        self.action_goal=FollowJointTrajectoryGoal()
        self.action_goal.trajectory.joint_names=self.joint_names
        
        self.SetMinSize(the_size)
        self.SetMaxSize(the_size)
        
    def display_init(self):
        js_pos=[20, 20]
        js_btn_length=[70, 70, 61, 80]
        js_distances=[10, 20, 10, 26]
        dis_h=50
        for i in xrange(len(self.js_display)):
            self.jp_button[i]=wx.Button(self.panel,
                                        label='J'+str(i+1)+' +', 
                                        pos=(js_pos[0],
                                             js_pos[1]+(5-i)*dis_h),
                                        size=(70,40))
            dis_tmp=js_btn_length[0]+js_distances[0]
                                        
            self.jp_button[i].Bind(wx.EVT_LEFT_DOWN, 
                                   lambda evt, mark=i+1 : self.teleop_joints(evt, mark) )
            self.jp_button[i].Bind(wx.EVT_LEFT_UP,
                                   lambda evt, mark=i+1 : self.release_button(evt, mark) )
            
            self.jm_button[i]=wx.Button(self.panel,
                                        label='J'+str(i+1)+' -', 
                                        pos=(js_pos[0]+dis_tmp,
                                             js_pos[1]+(5-i)*dis_h),
                                        size=(70,40))
            dis_tmp+=js_btn_length[1]+js_distances[1]
                                        
            self.jm_button[i].Bind(wx.EVT_LEFT_DOWN, 
                                   lambda evt, mark=-1*(i+1) : self.teleop_joints(evt, mark) )
            self.jm_button[i].Bind(wx.EVT_LEFT_UP,
                                   lambda evt, mark=-1*(i+1) : self.release_button(evt, mark) )
            
            pos_js_label=(js_pos[0]+dis_tmp, js_pos[1]+(5-i)*dis_h)
            self.js_label[i]=wx.StaticText(self.panel,
                                           label='J'+str(i+1)+'/deg:',
                                           pos=pos_js_label)
            self.js_label[i].SetPosition((pos_js_label[0], pos_js_label[1]+abs(40-self.js_label[i].GetSize()[1])/2))
            dis_tmp+=js_btn_length[2]+js_distances[2]

            pos_js_display=(js_pos[0]+dis_tmp, js_pos[1]+(5-i)*dis_h)
            self.js_display[i]=wx.TextCtrl(self.panel, 
                                           style=(wx.TE_CENTER |wx.TE_READONLY),
                                           value=' 0000.00 ', 
                                           pos=pos_js_display)
            self.js_display[i].SetPosition((pos_js_display[0], pos_js_display[1]+abs(40-self.js_display[i].GetSize()[1])/2))
            dis_tmp+=js_btn_length[3]+js_distances[3]

        ps_pos=[js_pos[0]+dis_tmp, 20]
        ps_btn_length=[70, 70, 53, 80]
        ps_distances=[10, 20, 10, 20]
        pcs_btn_label=['X', 'Y', 'Z', 'Rx', 'Ry', 'Rz']
        pcs_label=['X', 'Y', 'Z', 'R', 'P', 'Y']
        unit_label=['/mm:', '/mm:', '/mm:', '/deg:', '/deg:', '/deg:']
        for i in xrange(len(self.ps_display)):
            self.pp_button[i]=wx.Button(self.panel,
                                        label=pcs_btn_label[i]+' +', 
                                        pos=(ps_pos[0],
                                             ps_pos[1]+(5-i)*dis_h),
                                        size=(70,40))
            dis_tmp=ps_btn_length[0]+ps_distances[0]
                                        
            self.pp_button[i].Bind(wx.EVT_LEFT_DOWN, 
                                   lambda evt, mark=i+1 : self.teleop_pcs(evt, mark) )
            self.pp_button[i].Bind(wx.EVT_LEFT_UP,
                                   lambda evt, mark=i+1 : self.release_button(evt, mark) )
            
            self.pm_button[i]=wx.Button(self.panel,
                                        label=pcs_btn_label[i]+' -', 
                                        pos=(ps_pos[0]+dis_tmp,
                                             ps_pos[1]+(5-i)*dis_h),
                                        size=(70,40))
            dis_tmp+=ps_btn_length[1]+ps_distances[1]
                                        
            self.pm_button[i].Bind(wx.EVT_LEFT_DOWN, 
                                   lambda evt, mark=-1*(i+1) : self.teleop_pcs(evt, mark) )
            self.pm_button[i].Bind(wx.EVT_LEFT_UP,
                                   lambda evt, mark=-1*(i+1) : self.release_button(evt, mark) )
            
            pos_ps_label=(ps_pos[0]+dis_tmp, ps_pos[1]+(5-i)*dis_h)
            self.ps_label[i]=wx.StaticText(self.panel, 
                                           label=pcs_label[i]+unit_label[i],
                                           pos=pos_ps_label)
            self.ps_label[i].SetPosition((pos_ps_label[0], pos_ps_label[1]+abs(40-self.ps_label[i].GetSize()[1])/2))
            dis_tmp+=ps_btn_length[2]+ps_distances[2]
            
            pos_ps_display=(ps_pos[0]+dis_tmp, ps_pos[1]+(5-i)*dis_h)
            self.ps_display[i]=wx.TextCtrl(self.panel, 
                                           style=(wx.TE_CENTER |wx.TE_READONLY),
                                           value='', 
                                           pos=pos_ps_display)
            self.ps_display[i].SetPosition((pos_ps_display[0], pos_ps_display[1]+abs(40-self.ps_display[i].GetSize()[1])/2))
            dis_tmp+=ps_btn_length[3]+ps_distances[3]
    
    def velocity_setting_cb(self, event):
        current_velocity_scaling=self.velocity_setting.GetValue()*0.01
        self.teleop_api_dynamic_reconfig_client.update_configuration({'velocity_scaling': current_velocity_scaling})
        wx.CallAfter(self.update_velocity_scaling_show, current_velocity_scaling)
    
    def basic_api_reconfigure_cb(self, config):
        if self.velocity_setting_show.GetValue()!=config.velocity_scaling:
            self.velocity_setting.SetValue(int(config.velocity_scaling*100))
            wx.CallAfter(self.update_velocity_scaling_show, config.velocity_scaling)        
    
    def action_stop(self):
        self.action_client.wait_for_server()
        self.action_goal.trajectory.header.stamp.secs=0
        self.action_goal.trajectory.header.stamp.nsecs=0
        self.action_goal.trajectory.points=[]
        self.action_client.send_goal(self.action_goal)
    
    def teleop_joints(self,event,mark):       
        self.call_teleop_joint_req.data=mark
        resp=self.call_teleop_joint.call(self.call_teleop_joint_req)
        wx.CallAfter(self.update_reply_show, resp)
        event.Skip()
        
    def teleop_pcs(self,event,mark): 
        self.call_teleop_cart_req.data=mark            
        resp=self.call_teleop_cart.call(self.call_teleop_cart_req)
        wx.CallAfter(self.update_reply_show, resp)
        event.Skip()    
    
    def release_button(self, event, mark):
        self.call_teleop_stop_req.data=True
        resp=self.call_teleop_stop.call(self.call_teleop_stop_req)
        wx.CallAfter(self.update_reply_show, resp)
        event.Skip()
    
    def call_set_bool_common(self, event, client, request):
        btn=event.GetEventObject()
        check_list=['Servo On', 'Servo Off', 'Clear Fault']
        if btn.GetName() in check_list:
            self.show_message_dialog(btn.GetName(), client, request)
        else:
            try:
                resp=client.call(request)
                wx.CallAfter(self.update_reply_show, resp)
            except rospy.ServiceException, e:
                resp=SetBoolResponse()
                resp.success=False
                resp.message='no such service in simulation'
                wx.CallAfter(self.update_reply_show, resp)
        event.Skip()
    
    def thread_bg(self, client, request):
        wx.CallAfter(self.show_dialog)
        self.action_stop()
        rospy.sleep(1)
        try:
            resp=client.call(request)
            wx.CallAfter(self.update_reply_show, resp)
        except rospy.ServiceException, e:
            resp=SetBoolResponse()
            resp.success=False
            resp.message='no such service in simulation'
            wx.CallAfter(self.update_reply_show, resp)
        wx.CallAfter(self.destroy_dialog)
    
    def show_message_dialog(self, message, cl, rq):
        msg='executing ['+message+']'
        self.dlg_label.SetLabel(msg)
        lable_size=[]
        lable_size.append(self.dlg_label.GetSize()[0])
        lable_size.append(self.dlg_label.GetSize()[1])
        self.dlg.SetSize((lable_size[0]+30, lable_size[1]+30))
        t=threading.Thread(target=self.thread_bg, args=(cl, rq,))
        t.start()
        
    def show_dialog(self):
        self.dlg.SetPosition((self.GetPosition()[0]+250,
                              self.GetPosition()[1]+250))
        self.dlg.ShowModal()
        
    def destroy_dialog(self):
        self.dlg.EndModal(0)
        
    def closewindow(self,event):
        pass
    
    def show_set_links_dialog(self, evt):
        self.sld_ref_link_show.SetValue(self.ref_link_name)
        self.sld_end_link_show.SetValue(self.end_link_name)
        self.set_links_dlg.SetPosition((self.GetPosition()[0]+150,
                                        self.GetPosition()[1]+250))
        self.set_links_dlg.ShowModal()
    
    def update_ref_link(self, evt):
        request=SetStringRequest()
        request.data=self.sld_ref_link_show.GetValue()
        
        resp=self.call_set_ref_link.call(request)
        wx.CallAfter(self.update_reply_show, resp)
    
    def update_end_link(self, evt):
        request=SetStringRequest()
        request.data=self.sld_end_link_show.GetValue()
        
        resp=self.call_set_end_link.call(request)
        wx.CallAfter(self.update_reply_show, resp)
    
    def updateDisplay(self, msg):      
        for i in xrange(len(self.js_display)):
            self.js_display[i].SetValue(msg[i])
        
        for i in xrange(len(self.ps_display)):
            self.ps_display[i].SetValue(msg[i+6])
            
        if self.ref_link_lock.acquire():
            ref_link=self.ref_link_name
            self.ref_link_lock.release()
        
        if self.end_link_lock.acquire():
            end_link=self.end_link_name
            self.end_link_lock.release()
        
        self.ref_link_show.SetValue(ref_link)
        self.end_link_show.SetValue(end_link)
    
    def update_reply_show(self,msg):
        if msg.success:
            self.reply_show.SetBackgroundColour(wx.Colour(200, 225, 200))
        else:
            self.reply_show.SetBackgroundColour(wx.Colour(225, 200, 200))
        self.reply_show.SetValue(msg.message)
            
    def update_servo_state(self, msg):
        if msg.data:
            self.servo_state_show.SetBackgroundColour(wx.Colour(200, 225, 200))
            self.servo_state_show.SetValue('Enabled')
        else:
            self.servo_state_show.SetBackgroundColour(wx.Colour(225, 200, 200))
            self.servo_state_show.SetValue('Disabled')
    
    def update_fault_state(self, msg):
        if msg.data:
            self.fault_state_show.SetBackgroundColour(wx.Colour(225, 200, 200))
            self.fault_state_show.SetValue('Warning')
        else:
            self.fault_state_show.SetBackgroundColour(wx.Colour(200, 225, 200))
            self.fault_state_show.SetValue('No Fault')
        
    def update_velocity_scaling_show(self, msg):
        self.velocity_setting_show.SetValue(str(round(msg, 2)))
    
    
    def s_call_back(self, data):
        while not rospy.is_shutdown():
            try:
                self.listener.waitForTransform(self.group.get_planning_frame(),
                                               self.group.get_end_effector_link(),
                                               rospy.Time(0), rospy.Duration(100))
                (xyz,qua) = self.listener.lookupTransform(self.group.get_planning_frame(), 
                                                        self.group.get_end_effector_link(), 
                                                        rospy.Time(0))
                break
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                continue
        rpy=tf.transformations.euler_from_quaternion(qua)
        
        for i in xrange(len(data.position)):
            self.key.append(str(round(data.position[i]*180/math.pi, 2)))
            
        self.key.append(str(round(xyz[0]*1000, 2)))
        self.key.append(str(round(xyz[1]*1000, 2)))
        self.key.append(str(round(xyz[2]*1000, 2)))
        
        self.key.append(str(round(rpy[0]*180/math.pi, 2)))
        self.key.append(str(round(rpy[1]*180/math.pi, 2)))
        self.key.append(str(round(rpy[2]*180/math.pi, 2)))
        
        wx.CallAfter(self.updateDisplay, self.key)
        self.key=[]
    
    def monitor_status(self, evt):
        self.key=[]
        
        current_joint_values=self.group.get_current_joint_values()
        for i in xrange(len(current_joint_values)):
            self.key.append(str(round(current_joint_values[i]*180/math.pi, 2)))
        
        if self.ref_link_lock.acquire():
            ref_link=self.ref_link_name
            self.ref_link_lock.release()
        
        if self.end_link_lock.acquire():
            end_link=self.end_link_name
            self.end_link_lock.release()
        
        while not rospy.is_shutdown():
            try:
                self.listener.waitForTransform(ref_link, end_link, rospy.Time(0), rospy.Duration(100))
                (xyz,qua) = self.listener.lookupTransform(ref_link, end_link, rospy.Time(0))
                break
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                continue
            
        rpy=tf.transformations.euler_from_quaternion(qua)
            
        self.key.append(str(round(xyz[0]*1000, 2)))
        self.key.append(str(round(xyz[1]*1000, 2)))
        self.key.append(str(round(xyz[2]*1000, 2)))
        
        self.key.append(str(round(rpy[0]*180/math.pi, 2)))
        self.key.append(str(round(rpy[1]*180/math.pi, 2)))
        self.key.append(str(round(rpy[2]*180/math.pi, 2)))
        
        wx.CallAfter(self.updateDisplay, self.key)
            
    def servo_state_cb(self, data):
        self.servo_state=data.data
        wx.CallAfter(self.update_servo_state, data)
    
    def fault_state_cb(self, data):
        self.fault_state=data.data
        wx.CallAfter(self.update_fault_state, data)
    
    def ref_link_name_cb(self, data):
        if self.ref_link_lock.acquire():
            self.ref_link_name=data.data
            self.ref_link_lock.release()
    
    def end_link_name_cb(self, data):
        if self.end_link_lock.acquire():
            self.end_link_name=data.data
            self.end_link_lock.release()
        
    def listen(self):
        rospy.Subscriber(self.elfin_driver_ns+'enable_state', Bool, self.servo_state_cb)
        rospy.Subscriber(self.elfin_driver_ns+'fault_state', Bool, self.fault_state_cb)
        rospy.Subscriber(self.elfin_basic_api_ns+'reference_link_name', String, self.ref_link_name_cb)
        rospy.Subscriber(self.elfin_basic_api_ns+'end_link_name', String, self.end_link_name_cb)
        
        rospy.Timer(rospy.Duration(nsecs=50000000), self.monitor_status)
  
if __name__=='__main__':  
    rospy.init_node('elfin_gui')




    #app=wx.App(False)  
    #myframe=MyFrame(parent=None,id=-1)  
    #myframe.Show(True)

    #myframe.listen()

    #app.MainLoop()
    num = 0
    num2 = 0
    num3 = 0
    num4 = 0
    num5 = 0
    num6 = 0
    if len(sys.argv) >= 2:
        num = int(sys.argv[1])
    if len(sys.argv) >= 3:
        num2 = int(sys.argv[2])
    if len(sys.argv) >= 4:
        num2 = int(sys.argv[3])
    if len(sys.argv) >= 5:
        num2 = int(sys.argv[4])
    if len(sys.argv) >= 6:
        num2 = int(sys.argv[5])
    if len(sys.argv) >= 7:
        num2 = int(sys.argv[6])
    testcaip(num, num2, num3, num4, num5, num6)
    rospy.spin()
