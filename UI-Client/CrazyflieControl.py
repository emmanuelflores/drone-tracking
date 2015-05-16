# -*- coding: utf-8 -*-
"""
Created on Saturday 07.03.2015

Script:              CrazyflieControl.py
Description:         

Project title:       Personal Crazyflie Python Client
Project version:     1.0
Author:              Henricus N. Basien,Gourav Mahapatra
Author E-Mail:       Henricus@Basien.de
Copyright:           Copyright (c) 2015 Henricus N. Basien
Description:         Personal Crazyflie Python Client.
                     Controls (multiple) Crazyflie Nanodrones

"""

#==============================================================================
# Imports
#==============================================================================

## System Paths
import sys
sys.path.append("Telemetry")
sys.path.append("SimulatorCode")
sys.path.append("../Control")
sys.path.append("../Mathematics")
sys.path.append("../TTY")
sys.path.append("../Animation (VPython)")
sys.path.append("../Libraries")
sys.path.append("../Data Processing")
sys.path.append("..")
sys.path.append("../../Settings")

## External
# System
from time import sleep as wait
from timeit import default_timer as getTime
import random
import numpy as np
from copy import copy
from visual import *
# Crazyflie Client
from cfclient.utils.logconfigreader import LogConfig
from cflib.crazyflie import Crazyflie
from threading import Timer
import logging
from threading import Thread
import pygame as pg

## Internal
from UserInput import getKey
from VectorOperations import CoordinateSystem,EulerRotation,VectorAbs,rotation_matrix
from DebugGraphs import Debug_Display
from SysInfo import SysInfo
from Models import CoordinateSystem3D,Grid,VGrid
from Colors import Colors
from TextElements import StringWithBlankspace
from TTY import PrintSpecial
from Paths import CursorPath,GraphicsPath

def PrintInfo(Text):
    PrintSpecial("INFO: "+Text,"Green")

def PrintError(Text):
    PrintSpecial("Error: "+Text,"Red")

#==============================================================================
# Settings
#==============================================================================

# Logger Configuration
logging.basicConfig(level=logging.ERROR)

# Text Elements
PH = " "*3

# Modules
Calibrate = True#False
Stabilize = False
Plotting  = True#False
Animation = False
GUI       = False

#==============================================================================
# Control Class
#==============================================================================

class CrazyflieControl:
    """
    Class that connects to a Crazyflie and controls it until disconnection.
    """

    #------------------------------------------------------------------------------
    # Initialization
    #------------------------------------------------------------------------------

    def __init__(self, link_uri):
        """
        Initializes the control class and executes all needed functions.
        """

        # Connect Crazyflie
        self.Crazyflie = Crazyflie()
        self.Connected = False
        self.Connect(link_uri)

        while not self.Connected:
            wait(0.1)
            pass

        # Start Program
        self.t0 = 0#getTime()
        self.Running = True

        # Initialize
        self.SetInitialState()      
        self.InitializeReferenceCS()
        if Plotting:
            self.InitializePlotting()
        if GUI:
            self.InitializeGUI()
        if Animation:
            self.InitializeAnimation()

        # Run Main Loops
        Thread(target=self.MainLoop).start()
        if GUI:
            Thread(target=self.GUILoop).start()
        if Animation:
            Thread(target=self.AnimationLoop).start()

    def SetInitialState(self):
        '''
        Sets all initial control variables to be used later on.
        '''

        # Intial Values
        self.thrust_mult = 1
        self.thrust_step = 100#250#500
        # Lift-off at approx. 45000
        self.thrust    = 25e3#35e3#25e3#35e3#40e3#36e3#22e3#-#50e3#48e3#45e3#35e3#30e3#20e3
        self.thrustmin = 23e3#30e3#23e3#30e3#38e3#30e3#20e3#-#30e3
        self.thrustmax = 26e3#38e3#26e3#38e3#42e3#38e3#30e3#-#55e3#50e3#45e3#40e3#38e3#35e3#3e30#45e3#25e3
        self.pitch     = 0
        self.roll      = 0
        self.yawrate   = 0

        # self.thrust_mult = thrust_mult
        # self.thrust_step = thrust_step

        # self.thrust    = thrust
        # self.thrustmin = thrustmin
        # self.thrustmax = thrustmax
        # self.pitch     = pitch
        # self.roll      = roll
        # self.yawrate   = yawrate

        self.roll_Real  = 0.
        self.pitch_Real = 0.
        self.yaw_Real   = 0.
        self.att        = np.zeros(3)

        self.pos = np.zeros(3)
        self.vel = np.zeros(3)
        self.a   = np.zeros(3)
        self.velRel = np.zeros(3)
        self.aRel   = np.zeros(3)
        self.aRaw   = np.zeros(3)

        self.a_DataTimer = 0

        self.baro    = 0.
        self.baro_0  = 0.
        self.battery = 0.
        self.motors  = np.zeros(4)
        self.gyro    = np.zeros(3)
        self.mag     = np.zeros(3)

        PrintInfo("Initial Values Set")

    def InitializeReferenceCS(self):
        '''
        Initializes the Coordinate Systems of the Crazyflie
        '''
        self.refCS = np.array([\
        [0,1,0],\
        [-1,0,0],\
        [0,0,1]\
        ])

        self.CS0 = CoordinateSystem(refCS=self.refCS,RotationSigns=[1,1,-1],name="Default Coordinate System")
        self.CS  = CoordinateSystem(refCS=self.refCS,RotationSigns=[1,1,-1],name="Crazyflie Coordinate System")

        PrintInfo("Reference Systems initialized")

    def InitializeGUI(self):
        '''
        Initializes the GUI for the state representation and user interaction
        '''
        self.InitStateWindow()
        self.CrazyflieDataText=""

        PrintInfo("GUI initialized")

    def InitializeAnimation(self):
        '''
        Initializes the Animation Window and the 3D Model of the Crazyflie
        '''
        self.Model3D = None
        self.Window = Window()
        self.Create_3DModel()

        PrintInfo("Animation initialized")

    #------------------------------------------------------------------------------
    # Crazyflie Connection Status Callbacks
    #------------------------------------------------------------------------------

    def Connect(self,link_uri):

        self.Crazyflie.connected.add_callback(self.connected)
        self.Crazyflie.disconnected.add_callback(self.disconnected)
        self.Crazyflie.connection_failed.add_callback(self.connection_failed)
        self.Crazyflie.connection_lost.add_callback(self.connection_lost)

        self.Crazyflie.open_link(link_uri)

        print "Connecting to %s" % link_uri

    def connected(self, link_uri):
        """
        This callback is called form the Crazyflie API when a Crazyflie
        has been connected and the TOCs have been downloaded.
        """

        # Start a separate thread to do the motor test.
        # Do not hijack the calling thread!
        #Thread(target=self.MainLoop).start()
        self.Connected = True
        PrintInfo("Connection to %s is established" % link_uri)

    def connection_failed(self, link_uri, msg):
        """
        Callback when connection initial connection fails (i.e no Crazyflie
        at the speficied address)
        """

        PrintError("Connection to %s failed: %s" % (link_uri, msg))

    def connection_lost(self, link_uri, msg):
        """
        Callback when disconnected after a connection has been made (i.e
        Crazyflie moves out of range)
        """

        PrintError("Connection to %s lost: %s" % (link_uri, msg))

    def disconnected(self, link_uri):
        """
        Callback when the Crazyflie is disconnected (called in all cases)
        """

        PrintError("Disconnected from %s" % link_uri)
        
    #------------------------------------------------------------------------------
    # Main Loop
    #------------------------------------------------------------------------------

    def MainLoop(self):

        self.run = 0

        self.SetCalibratedState()
        
        self.InitializeLogging()
        
        self.InitializeGetParameters()

        self.ControlLoop()

        self.Kill()
        
    def Kill(self):
        print ">>>Killing Drone<<<"
        self.Crazyflie.commander.send_setpoint(0, 0, 0, 0)
        # Make sure that the last packet leaves before the link is closed
        # since the message queue is not flushed before closing
        self.Running = False
        wait(0.1)
        self.Crazyflie.close_link()

    def KillCheck(self):
        if abs(self.att[0])>=70 or abs(self.att[1])>=70:
            print ">Angle Kill<"
            self.Running=False
        if getKey("Escape")!=0:
            print ">Escape Kill<"
            self.Running=False
        # if self.thrust <= self.thrustmin:
        #     print ">ThrustMin Kill<"
        #     self.Running=False
        
    #------------------------------------------------------------------------------
    # Personal Control
    #------------------------------------------------------------------------------

    def ControlLoop(self):

        while self.Running:

            self.run+=1
            # print "Run #"+str(self.run)

            self.GetState()
            #self.PrintState()
            self.GetInfoText()

            self.SendState()
            self.EvaluateData()
            
            self.KillCheck()

    def GUILoop(self):

        while self.Running:
            if True:
                # try:
                    self.StateWindow.fill([0]*3)
                    lines = self.CrazyflieDataText.split("\n")
                    for i in range(len(lines)):
                        line = lines[i]
                        render_text(self.StateWindow,line,[300,100+i*30],self.Font)
                    pg.display.flip()
                    pg.event.wait()
                # except:
                #     PrintSpecial("Display Failed!","Red")
            else:
                self.PrintData()

    def AnimationLoop(self):

            if self.Model3D!=None:
                self.Model3D.Update()
        
    def SetCalibratedState(self):
        if Calibrate:
            # Positive: Front || Negative: Back
            self.pitch = 4#5#-#40#38#35#32#28#-28
            # Positive: Right || Negative: Left
            self.roll  = 0#-#-22#-20#-18#-15#-10#-2
        
    def GetState(self):
        # Climb & Decent
        if self.thrust >= self.thrustmax:
            self.thrust_mult = 0#-1
        self.thrust += self.thrust_step * self.thrust_mult
        self.thrust=0
        
        if Stabilize:
            # Stabilize
            if self.roll_Real<self.roll:
                self.roll+=1.
            elif self.roll_Real>self.roll:
                self.roll-=1.
            if self.pitch_Real<self.pitch:
                self.roll+=1.
            elif self.pitch_Real>self.pitch:
                self.pitch-=1.
        
    def SendState(self):
        self.Crazyflie.commander.send_setpoint(self.roll,self.pitch,self.yawrate,self.thrust)
        wait(0.1)

    def PrintState(self):
        print "-"*30
        print "Set Data:"
        print PH+"Thrust: "+str(round(self.thrust,2))
        print PH+"Roll:   "+str(round(self.roll,2))
        print PH+"Pitch:  "+str(round(self.pitch,2))
        print PH+"Yaw:    "+str(round(self.yawrate,2))
        
    #------------------------------------------------------------------------------
    # Logging
    #------------------------------------------------------------------------------
    
    def EvaluateData(self):
        self.att = np.array([self.roll_Real,-self.pitch_Real,-self.yaw_Real])
        # Update CS
        self.CS.setCS(self.att)

        if Plotting:
            if self.t0==0:
                self.t0=getTime()
            # print "Timestamp: ",timestamp
            t = getTime()-self.t0
            self.Stabilizer_Plot.UpdateGraph(graphname="Roll" ,pos=[t,np.degrees(self.roll_Real)])
            self.Stabilizer_Plot.UpdateGraph(graphname="Pitch",pos=[t,np.degrees(self.pitch_Real)])
            self.Stabilizer_Plot.UpdateGraph(graphname="Yaw"  ,pos=[t,np.degrees(self.yaw_Real)])

            self.Velocity_Plot.UpdateGraph(graphname="X"    ,pos=[t,self.vel[0]])
            self.Velocity_Plot.UpdateGraph(graphname="Y"    ,pos=[t,self.vel[1]])
            self.Velocity_Plot.UpdateGraph(graphname="Z"    ,pos=[t,self.vel[2]])
            #print self.aRaw[2],VectorAbs(self.aRaw)#self.a
            self.Acceleration_Plot.UpdateGraph(graphname="X_Earth",pos=[t,self.a[0]])
            self.Acceleration_Plot.UpdateGraph(graphname="Y_Earth",pos=[t,self.a[1]])
            self.Acceleration_Plot.UpdateGraph(graphname="Z_Earth",pos=[t,self.a[2]])
            self.Acceleration_Plot.UpdateGraph(graphname="X_Raw",pos=[t,self.aRaw[0]])
            self.Acceleration_Plot.UpdateGraph(graphname="Y_Raw",pos=[t,self.aRaw[1]])
            self.Acceleration_Plot.UpdateGraph(graphname="Z_Raw",pos=[t,self.aRaw[2]])

    def InitializePlotting(self):

        self.Stabilizer_Plot = Debug_Display("Attitude",u"°",x=0,y=0,w=SysInfo.Resolution[0]/2,h=SysInfo.Resolution[1]/3,IndicationInterval=5,IndicationRange=20)

        self.Stabilizer_Plot.addGraph(name="Roll" ,color=Colors["Red"]  ,label=False)
        self.Stabilizer_Plot.addGraph(name="Pitch",color=Colors["Green"],label=False)
        self.Stabilizer_Plot.addGraph(name="Yaw"  ,color=Colors["Blue"] ,label=False)

        self.Velocity_Plot = Debug_Display("Velocity",u"m/s",x=0,y=SysInfo.Resolution[1]/3,w=SysInfo.Resolution[0]/2,h=SysInfo.Resolution[1]/3,IndicationInterval=2,IndicationRange=8)

        self.Velocity_Plot.addGraph(name="X",color=Colors["Red"]  ,label=False)
        self.Velocity_Plot.addGraph(name="Y",color=Colors["Green"],label=False)
        self.Velocity_Plot.addGraph(name="Z",color=Colors["Blue"] ,label=False)

        self.Acceleration_Plot = Debug_Display("Acceleration",u"m/s²",x=0,y=SysInfo.Resolution[1]*2/3,w=SysInfo.Resolution[0]/2,h=SysInfo.Resolution[1]/3,IndicationInterval=2,IndicationRange=8)

        self.Acceleration_Plot.addGraph(name="X_Earth",color=Colors["Red"]  ,label=False)
        self.Acceleration_Plot.addGraph(name="Y_Earth",color=Colors["Green"],label=False)
        self.Acceleration_Plot.addGraph(name="Z_Earth",color=Colors["Blue"] ,label=False)
        self.Acceleration_Plot.addGraph(name="X_Raw",color=Colors["Red"]  *0.5,label=False)
        self.Acceleration_Plot.addGraph(name="Y_Raw",color=Colors["Green"]*0.5,label=False)
        self.Acceleration_Plot.addGraph(name="Z_Raw",color=Colors["Blue"] *0.5,label=False)

    def InitializeLogging(self):
        
        # Attitude (if period_in_ms = <10 -> Invalid -> other Logs start working again?! O.o)
        self.StabilizerLog = LogConfig(name="Stabilizer", period_in_ms=10)
        self.StabilizerLog.add_variable("stabilizer.roll", "float")
        self.StabilizerLog.add_variable("stabilizer.pitch", "float")
        self.StabilizerLog.add_variable("stabilizer.yaw", "float")

        self.Crazyflie.log.add_config(self.StabilizerLog)

        # Battery
        self.BatteryLog = LogConfig(name="Battery", period_in_ms=200)
        self.BatteryLog.add_variable("pm.vbat", "float")

        self.Crazyflie.log.add_config(self.BatteryLog)

        # Barometer
        self.BarometerLog = LogConfig(name="Barometer", period_in_ms=10)
        self.BarometerLog.add_variable("baro.aslLong", "float")

        self.Crazyflie.log.add_config(self.BarometerLog)

        # Accelerometer (if period_in_ms = <10 -> Invalid -> other Logs start working again?! O.o)
        self.AccelerometerLog = LogConfig(name="Accelerometer", period_in_ms=10)
        self.AccelerometerLog.add_variable("acc.x", "float")
        self.AccelerometerLog.add_variable("acc.y", "float")
        self.AccelerometerLog.add_variable("acc.z", "float")

        self.Crazyflie.log.add_config(self.AccelerometerLog)

        # Motors
        self.MotorsLog = LogConfig(name="Motors", period_in_ms=50)
        self.MotorsLog.add_variable("motor.m1", "int32_t")
        self.MotorsLog.add_variable("motor.m2", "int32_t")
        self.MotorsLog.add_variable("motor.m3", "int32_t")
        self.MotorsLog.add_variable("motor.m4", "int32_t")

        self.Crazyflie.log.add_config(self.MotorsLog)

        # Gyro
        self.GyroLog = LogConfig(name="Gyro", period_in_ms=50)
        self.GyroLog.add_variable("gyro.x", "float")
        self.GyroLog.add_variable("gyro.y", "float")
        self.GyroLog.add_variable("gyro.z", "float")

        self.Crazyflie.log.add_config(self.GyroLog)

        # Magnetometer
        self.MagnetometerLog = LogConfig(name="Magnetometer", period_in_ms=50)
        self.MagnetometerLog.add_variable("mag.x", "float")#int16_t")
        self.MagnetometerLog.add_variable("mag.y", "float")#int16_t")
        self.MagnetometerLog.add_variable("mag.z", "float")#int16_t")

        self.Crazyflie.log.add_config(self.MagnetometerLog)

        #wait(10)

        if self.StabilizerLog.valid:
            # This callback will receive the data
            self.StabilizerLog.data_received_cb.add_callback(self.Stabilizer_log_data)
            # This callback will be called on errors
            self.StabilizerLog.error_cb.add_callback(self.log_error)
            # Start the logging
            self.StabilizerLog.start()
        else:
            print("Could not add logconfig '"+str(self.StabilizerLog.name)+"' since some variables are not in TOC")
            wait(2)

        if self.BatteryLog.valid:
            # This callback will receive the data
            self.BatteryLog.data_received_cb.add_callback(self.Battery_log_data)
            # This callback will be called on errors
            self.BatteryLog.error_cb.add_callback(self.log_error)
            # Start the logging
            self.BatteryLog.start()
        else:
            print("Could not add logconfig '"+str(self.BatteryLog.name)+"' since some variables are not in TOC")
            wait(2)

        if self.BarometerLog.valid:
            # This callback will receive the data
            self.BarometerLog.data_received_cb.add_callback(self.Barometer_log_data)
            # This callback will be called on errors
            self.BarometerLog.error_cb.add_callback(self.log_error)
            # Start the logging
            self.BarometerLog.start()
        else:
            print("Could not add logconfig '"+str(self.BarometerLog.name)+"' since some variables are not in TOC")
            wait(2)

        if self.AccelerometerLog.valid:
            # This callback will receive the data
            self.AccelerometerLog.data_received_cb.add_callback(self.Accelerometer_log_data)
            # This callback will be called on errors
            self.AccelerometerLog.error_cb.add_callback(self.log_error)
            # Start the logging
            self.AccelerometerLog.start()
        else:
            print("Could not add logconfig '"+str(self.AccelerometerLog.name)+"' since some variables are not in TOC")
            wait(2)

        if self.MotorsLog.valid:
            # This callback will receive the data
            self.MotorsLog.data_received_cb.add_callback(self.Motors_log_data)
            # This callback will be called on errors
            self.MotorsLog.error_cb.add_callback(self.log_error)
            # Start the logging
            self.MotorsLog.start()
        else:
            print("Could not add logconfig '"+str(self.MotorsLog.name)+"' since some variables are not in TOC")
            wait(2)

        if self.GyroLog.valid:
            # This callback will receive the data
            self.GyroLog.data_received_cb.add_callback(self.Gyro_log_data)
            # This callback will be called on errors
            self.GyroLog.error_cb.add_callback(self.log_error)
            # Start the logging
            self.GyroLog.start()
        else:
            print("Could not add logconfig '"+str(self.GyroLog.name)+"' since some variables are not in TOC")
            wait(2)

        if self.MagnetometerLog.valid:
            # This callback will receive the data
            self.MagnetometerLog.data_received_cb.add_callback(self.Magnetometer_log_data)
            # This callback will be called on errors
            self.MagnetometerLog.error_cb.add_callback(self.log_error)
            # Start the logging
            self.MagnetometerLog.start()
        else:
            print("Could not add logconfig '"+str(self.MagnetometerLog.name)+"' since some variables are not in TOC")
            wait(2)

    def Stabilizer_log_data(self, timestamp, data, logconf):
        """Callback from the log API when data arrives"""
        #print "[%d][%s]: %s" % (timestamp, logconf.name, data)
        
        self.roll_Real  = np.radians(data['stabilizer.roll'])
        self.pitch_Real = np.radians(data['stabilizer.pitch'])
        self.yaw_Real   = np.radians(data['stabilizer.yaw'])

    def Battery_log_data(self, timestamp, data, logconf):
        """Callback from the log API when data arrives"""
        
        self.battery = data['pm.vbat']

    def Barometer_log_data(self, timestamp, data, logconf):
        """Callback from the log API when data arrives"""
        
        if self.baro_0==0:
            self.baro_0 = copy(data['baro.aslLong'])

        self.baro = data['baro.aslLong']-self.baro_0

    def Accelerometer_log_data(self, timestamp, data, logconf):
        """Callback from the log API when data arrives"""
        
        if self.a_DataTimer==0:
            self.a_DataTimer = getTime()
        dt = getTime()-self.a_DataTimer
        self.a_DataTimer = getTime()

        self.aRaw = np.array([\
        data['acc.x'],\
        data['acc.y'],\
        data['acc.z']\
        ]).astype(float)*10#/1000

    #     self.EvaluateAccelerometerData()

    # def EvaluateAccelerometerData(self):
        self.aRel = copy(self.aRaw)
        #print self.aRel
        Gravity = 9.81
        relative_Gravity = [0,0,-Gravity]
        relative_Gravity = EulerRotation(relative_Gravity,[1,0,0],self.roll_Real)
        relative_Gravity = EulerRotation(relative_Gravity,[0,1,0],self.pitch_Real)
        self.aRel+=relative_Gravity


        # Body_to_Earth = rotation_matrix([1,0,0],self.att[0],matrix=True)*rotation_matrix([0,1,0],self.att[1],matrix=True)*rotation_matrix([0,0,1],self.att[2],matrix=True)
        self.a=self.aRel#self.a = np.dot(Body_to_Earth,self.aRel)

        self.velRel += self.aRel*dt
        self.pos    += self.velRel*dt
        #print self.pos

    def Motors_log_data(self, timestamp, data, logconf):
        """Callback from the log API when data arrives"""
        
        self.motors = np.array([\
        data["motor.m1"],\
        data["motor.m2"],\
        data["motor.m3"],\
        data["motor.m4"]\
        ])

    def Gyro_log_data(self, timestamp, data, logconf):
        """Callback from the log API when data arrives"""
        
        self.gyro = np.array([\
        data['gyro.x'],\
        data['gyro.y'],\
        data['gyro.z']\
        ])

    def Magnetometer_log_data(self, timestamp, data, logconf):
        """Callback from the log API when data arrives"""
        
        self.mag = [\
        data['mag.x'],\
        data['mag.y'],\
        data['mag.z']\
        ]

    def log_error(self, logconf, msg):
        """Callback from the log API when an error occurs"""
        print "Error when logging %s: %s" % (logconf.name, msg)

    def PrintData(self):

        print self.CrazyflieDataText

    def GetInfoText(self):

        self.CrazyflieDataText = ""

        self.CrazyflieDataText += "-"*30+"\n"
        self.CrazyflieDataText += "Received Data:"+"\n"
        self.CrazyflieDataText += PH+"Roll:  "+str(round(np.degrees(self.att[0]),3))+u" [°]"+"\n"#roll_Real ),3))+u" [°]"+"\n"
        self.CrazyflieDataText += PH+"Pitch: "+str(round(np.degrees(self.att[1]),3))+u" [°]"+"\n"#pitch_Real),3))+u" [°]"+"\n"
        self.CrazyflieDataText += PH+"Yaw:   "+str(round(np.degrees(self.att[2]),3))+u" [°]"+"\n"#yaw_Real  ),3))+u" [°]"+"\n"
        self.CrazyflieDataText += "\n"                                         
        self.CrazyflieDataText += PH+"Accelerometer: ["+str(round(self.a  [0],3))+","+str(round(self.a  [1],3))+","+str(round(self.a  [2],3))+"] ("+str(round(VectorAbs(self.a  ),3))+")"+u" [m/s²]"+"\n"
        self.CrazyflieDataText += PH+"Velocity:      ["+str(round(self.vel[0],3))+","+str(round(self.vel[1],3))+","+str(round(self.vel[2],3))+"] ("+str(round(VectorAbs(self.vel),3))+")"+u" [m/s]"+"\n"
        self.CrazyflieDataText += PH+"Position:      ["+str(round(self.pos[0],3))+","+str(round(self.pos[1],3))+","+str(round(self.pos[2],3))+"] ("+str(round(VectorAbs(self.pos),3))+")"+u" [m]"+"\n"

        self.CrazyflieDataText += "\n"  

        self.CrazyflieDataText += PH+"Barometer: "+str(round(self.baro    ,3))+u" [m]" +" || Barometer_0:    "+str(round(self.baro_0,3))+u" [m]" +"\n"+"\n"
        self.CrazyflieDataText += PH+"Battery:   "+str(round(self.battery*10**3,3))+u" [mV]"+"\n"
        self.CrazyflieDataText += PH+"Motors:    "+\
        str(round(self.motors[0],3))+","+\
        str(round(self.motors[1],3))+","+\
        str(round(self.motors[2],3))+","+\
        str(round(self.motors[3],3))+\
        u" [?]" +"\n"
        self.CrazyflieDataText += PH+"Gyro:      "+str(round(self.gyro[0],3))+","+str(round(self.gyro[1],3))+","+str(round(self.gyro[2],3))+u" [?]" +"\n"
        self.CrazyflieDataText += PH+"Magneto:   "+str(round(self.mag[0] ,3))+","+str(round(self.mag[1] ,3))+","+str(round(self.mag[2] ,3))+u" [?]"+"\n"

        # print "-"*30
        # print "Received Data:"
        # print PH+"Roll:    "+str(round(self.roll_Real    ,3))+u" [°]"
        # print PH+"Pitch:   "+str(round(self.pitch_Real   ,3))+u" [°]"
        # print PH+"Yaw:     "+str(round(self.yaw_Real     ,3))+u" [°]"
        # # print                                              
        # # print PH+"Accelerometer: "+str(np.round(self.a,3))+u" [m/s²]"
        # # print   
        # # print PH+"Baro:    "+str(round(self.baro         ,3))+u" [m]"
        # # print PH+"Battery: "+str(round(self.battery*10**3,3))+u" [mV]" 
        # # print PH+"Motors:  "+str(np.round(self.motors    ,3))+u" [?]" 
        # # print PH+"Gyro:    "+str(np.round(self.gyro      ,3))+u" [?]" 
        # # print PH+"Magneto: s"+str(np.round(self.mag       ,3))+u" [?]"
    
    #------------------------------------------------------------------------------
    # Get Parameters
    #------------------------------------------------------------------------------
    
    def InitializeGetParameters(self):#, link_uri):        
        
        """ This callback is called form the Crazyflie API when a Crazyflie
        has been connected and the TOCs have been downloaded."""
        #print "Connected to %s" % link_uri
        
        # Variable used to keep main loop occupied until disconnect
        self.is_connected = True

        self.param_check_list = []
        self.param_groups = []

        random.seed()

        # Print the param TOC
        self.CrazyflieParameters = dict()

        p_toc = self.Crazyflie.param.toc.toc
        for group in sorted(p_toc.keys()):
            Group = "{}".format(group)
            #print Group # <-------------------------------------------------------------------------------
            self.CrazyflieParameters[Group] = dict()
            for param in sorted(p_toc[group].keys()):
                Parameter = "{}".format(param)
                #print "\t"+Parameter # <-------------------------------------------------------------------------------
                self.CrazyflieParameters[Group][Parameter] = 1
                self.param_check_list.append("{0}.{1}".format(group, param))
            self.param_groups.append("{}".format(group))
            # For every group, register the callback
            self.Crazyflie.param.add_update_callback(group=group, name=None,
                                               cb=self.param_callback)

        #self.PrintParameters()


        # # You can also register a callback for a specific group.name combo
        # self.Crazyflie.param.add_update_callback(group="cpu", name="flash",
        #                                    cb=self.cpu_flash_callback)

        print
        print "Reading back all parameter values"
        # Request update for all the parameters using the full name
        # group.name
        for p in self.param_check_list:
            self.Crazyflie.param.request_param_update(p)


        # # Set LED-Ring Test
        # wait(20)
        # Color = [0,0,40]
        # print "LED Ring effect changed to Color :"+str(Color)
        # self.SetLED_RGB(Color)

        # ringeffect = 1
        # print "LED Ring effect changed to Mode #"+str(ringeffect)
        # #self.Crazyflie.param.set_value("ring.effect","{:.2f}".format(ringeffect))
        # SetParameter("ring","effect","1")

    def SetParameter(self,Group,Parameter,Value):
        # print "Set Parameter:",Group+"."+Parameter,"{:.2f}".format(Value)
        # self.Crazyflie.param.set_value(Group+"."+Parameter,"{:.2f}".format(Value))
        print "Set Parameter:",Group+"."+Parameter,"{:2}".format(Value)
        self.Crazyflie.param.set_value(Group+"."+Parameter,"{:2}".format(Value))

    def SetLED_RGB(self,Color):
        self.SetParameter("ring","effect",str(7))
        self.SetParameter("ring","solidRed"  ,str(Color[0]))
        self.SetParameter("ring","solidGreen",str(Color[1]))
        self.SetParameter("ring","solidBlue" ,str(Color[2]))

        print "LED color changed to: "+str(Color)

    def PrintParameters(self):
        print ">>>Crazyflie Parameters<<<"
        for Group in self.CrazyflieParameters:
            print Group
            for Parameter in self.CrazyflieParamet,ers[Group]:
                print PH+"- "+StringWithBlankspace(Parameter,20)+": "+str(self.CrazyflieParameters[Group][Parameter])

    def cpu_flash_callback(self, name, value):
        """Specific callback for the cpu.flash parameter"""
        print "The connected Crazyflie has {}kb of flash".format(value)

    def param_callback(self, name, value):
        """Generic callback registered for all the groups"""
        print "{0}: {1}".format(name, value) # <-------------------------------------------------------------------------------


        # Group,Parameter=name.split(".")
        # print ">",Group,Name,Value
        # self.CrazyflieParameters[Group][Parameter] = value
        Categories = name.split(".")
        Group,Parameter = Categories[0],Categories[1]
        #print ">",Group,Parameter,value#,Name,Value
        self.CrazyflieParameters[Group][Parameter] = value

        self.Crazyflie.param.add_update_callback(group=Group,name=Paramater,cb=self.parameter_update_callback)
        

        # Remove each parameter from the list and close the link when
        # all are fetched
        self.param_check_list.remove(name)
        if len(self.param_check_list) == 0:
            print ">>>Have fetched all parameter values."

            # First remove all the group callbacks
            for g in self.param_groups:
                self.Crazyflie.param.remove_update_callback(group=g,cb=self.param_callback)

            # # Create a new random value [0.00,1.00] for pid_attitude.pitch_kd
            # # and set it
            # pkd = random.random()
            # print
            # print "Write: pid_attitude.pitch_kd={:.2f}".format(pkd)
            # self.Crazyflie.param.add_update_callback(group="pid_attitude",
            #                                    name="pitch_kd",
            #                                    cb=self.a_pitch_kd_callback)
            # # When setting a value the parameter is automatically read back
            # # and the registered callbacks will get the updated value
            # self.Crazyflie.param.set_value("pid_attitude.pitch_kd",
            #                          "{:.2f}".format(pkd))

            self._cf.param.add_update_callback(group="ring",name="effect",cb=self._a_ring_effect_callback)
            self._cf.param.set_value("ring.effect","1")


            self.PrintParameters()

            # Set LED-Ring Test
            Color = [0,0,40]
            print "LED Ring effect changed to Color :"+str(Color)
            self.SetLED_RGB(Color)

    def _a_ring_effect_callback(self, name, value):
        """Callback for ring_effect"""
        print "Readback (LED_effect): {0}={1}".format(name, value)
        print

    def parameter_update_callback(self,name,value):
        print "Readback: {0}={1}".format(name, value)

    #------------------------------------------------------------------------------
    # 3D-Model
    #------------------------------------------------------------------------------

    def Create_3DModel(self):
        self.Model3D = Crazyflie3D(self)

    def InitStateWindow(self):
        init_pygame()

        pos = [0,0]#[100,100]#[0,0]
        resolution = [SysInfo.Resolution[0]/4,SysInfo.Resolution[1]]
        #PrintSpecial("Opening State Window","Red")
        self.StateWindow = scr_init(pos=pos,reso=resolution,fullscreen=False,frameless=False,mouse=True,caption="Crazyflie Status")#,icon="Instrument Icon.png")
        #PrintSpecial("State Window Opened","Red")
        font='LCD.TTF'
        self.Font = pg.font.SysFont(font,30)#'fonts/'+

        # render_text(self.StateWindow,"This is some TestText",[100,100],self.Font)
        # print "TestText rendered"

        # pg.display.flip()

#==============================================================================
# Pygame Functions
#==============================================================================

def init_pygame():
    '''
    Initializes Pygame, the font module and the mixer module
    '''
    # Initiate pygame
    pg.init()
    # Initiate font module
    pg.font.init()
    # Initirate mixer module
    pg.mixer.init()
    #pg.mixer.init(44100,-16,2,8192)
    
def scr_init(pos,reso,fullscreen,frameless,mouse,caption,icon=False):
    '''
    Initializes the screen based on given resolution, caption and icon.
    In either Fullscreen, Frameless oder normal mode.
    '''    

    # Set Position
    import os
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (pos[0],pos[1])

    reso = np.array(reso).astype(int)
    # Initiate screen
    if fullscreen:
        scr = pg.display.set_mode(reso, pg.FULLSCREEN)
    elif frameless:
        scr = pg.display.set_mode(reso, pg.NOFRAME)
    else:
        scr = pg.display.set_mode(reso)

    #import time
    #wait(1)

    # Add caption
    pg.display.set_caption(caption)
    # Load/Set icon
    if icon!=False:
        icon = GraphicsPath+icon
        icon = pg.image.load(icon)
        icon = pg.transform.scale(icon, (32,32))
        pg.display.set_icon(icon)
    # Disable Mouse
    if not mouse:
        pg.mouse.set_visible(0)
        
    # CursorString = Cursor2
    # CursorData = pg.cursors.compile(CursorString, black='X', white='.', xor='o')
    # CursorSize = [len(CursorString[0])]*2
    # pg.mouse.set_cursor(CursorSize, (0,0), CursorData[0],CursorData[1])

    # Return screen surface   
    return scr
        
## Get Keyboard input
def get_keyboard():
    '''
    Returns a dictionary with logical for all keyboard keys if pressed.
    '''
    pg.event.pump()
    return pg.key.get_pressed()
 
def render_text(screen,Text,pos,font,color=Colors["White"]*255,ang=0,aa=1,mid=False):
    pos = np.array(pos).astype(int)
    Text = font.render(Text, aa, color)
    TextPos = Text.get_rect()
    if mid:
        shift = Rotate([TextPos.w*-0.2,0],radians(ang))
    else:
        shift = np.zeros(2)
    TextPos.centerx = pos[0]+shift[0]
    TextPos.centery = pos[1]+shift[1]
    Text = pg.transform.rotate(Text,ang)
    screen.blit(Text, TextPos)

#==============================================================================
# Window
#==============================================================================

class Window():

    def __init__(self):

        GridDimension = 2#4#10
        Color = color.blue
        Gap = 0.25#GridDimension/10

        self.Windowname="Crazyflie 2.0 Trace"
        self.Position = [SysInfo.Resolution[0]/2,0]
        self.Resolution = SysInfo.Resolution
        self.Fullscreen = False
        self.Option3D = 'crosseyed'
        self.initCamPos = np.zeros(3)
        self.initDir    = [-1,-1,-1]
        self.initRange  = np.ones(3)*GridDimension#10

        self.Window = display(title=self.Windowname,x=self.Position[0], y=self.Position[1], width=self.Resolution[0], height=self.Resolution[1], background=Colors["Black"],fullscreen = self.Fullscreen)


        self.CS = CoordinateSystem3D(name="Crazyflie Coordinate System",offset = GridDimension/2)#,scale=0.1)
        # Window.x = Position[0]
        # Window.y = Position[1]
        # Window.width  = Resolution[0]#SysInfo.Resolution[0]
        # Window.height = Resolution[1]#SysInfo.Resolution[1]
        
        #Window.exit = False
        if self.Option3D!=False:
            self.Window.stereo = self.Option3D
            #Window.stereodepth = #1,2
            PrintSpecial(PH+"3D view enabled!","Yellow")

        self.Window.show_rendertime = True
        self.Window.enable_shaders=True

        # Initial Camera position
        self.Window.center = self.initCamPos
        self.Window.forward= self.initDir
        self.Window.range  = self.initRange
        self.Window.up     = [0,0,1]

        PrintSpecial("VPython Animation Window Opened at ("+str(int(self.Window.x))+","+str(int(self.Window.y))+") [Res: "+str(int(self.Window.width))+","+str(int(self.Window.height))+"] px\n","Green") 

        self.Grid  = Grid(GridDimension,GridDimension,height=0,gap=Gap,color=Color,radius=0.)
        self.VGrid = VGrid(GridDimension,GridDimension,height=GridDimension*0.8,gap=Gap,color=Color,radius=0)

#==============================================================================
# 3D-Model
#==============================================================================

#from Crazyflie2 import Crazyflie2_3D

class Crazyflie3D():

    def __init__(self,Crazyflie):

        self.Crazyflie = Crazyflie

        self.CS = CoordinateSystem3D(refCS=Crazyflie.CS0.matrix,RotationSigns=Crazyflie.CS0.RotationSigns,name="Crazyflie Coordinate System")#,scale=0.1)

        self.Trace = curve(pos=[self.Crazyflie.pos],color=Colors["Red"])

        self.Update()

    def Update(self):
        self.CS.pos = self.Crazyflie.pos
        self.CS.setCS(att=self.Crazyflie.att)

        self.Trace.append(pos=self.Crazyflie.pos)