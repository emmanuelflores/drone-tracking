# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2014 Bitcraze AB
#
#  Crazyflie Nano Quadcopter Client
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.

"""
Simple example that connects to the first Crazyflie found, ramps up/down
the motors and disconnects.
"""

import time, sys
from threading import Thread

#FIXME: Has to be launched from within the example folder
sys.path.append("../lib")
import cflib
from cfclient.utils.logconfigreader import LogConfig
from cflib.crazyflie import Crazyflie

from threading import Timer

import logging
logging.basicConfig(level=logging.ERROR)


from UserInput import getKey


PH = " "*3

class CrazyflieControl:
    """
    Class that connects to a Crazyflie and controls it until disconnection
    """
    def __init__(self, link_uri):
        """ Initialize and run the example with the specified link_uri """

        self._cf = Crazyflie()

        self._cf.connected.add_callback(self._connected)
        self._cf.disconnected.add_callback(self._disconnected)
        self._cf.connection_failed.add_callback(self._connection_failed)
        self._cf.connection_lost.add_callback(self._connection_lost)

        self._cf.open_link(link_uri)

        print "Connecting to %s" % link_uri

    def _connected(self, link_uri):
        """ This callback is called form the Crazyflie API when a Crazyflie
        has been connected and the TOCs have been downloaded."""

        # Start a separate thread to do the motor test.
        # Do not hijack the calling thread!
        Thread(target=self._ControlRun).start()

    def _connection_failed(self, link_uri, msg):
        """Callback when connection initial connection fails (i.e no Crazyflie
        at the speficied address)"""
        print "Connection to %s failed: %s" % (link_uri, msg)

    def _connection_lost(self, link_uri, msg):
        """Callback when disconnected after a connection has been made (i.e
        Crazyflie moves out of range)"""
        print "Connection to %s lost: %s" % (link_uri, msg)

    def _disconnected(self, link_uri):
        """Callback when the Crazyflie is disconnected (called in all cases)"""
        print "Disconnected from %s" % link_uri

    def _ControlRun(self):

        self._SetInitialState()
        self._SetCalibratedState()
        
        self._SetGetData()

        self._ControlLoop()

        self._Kill()

    def _ControlLoop(self):

        while self.thrust >= self.thrustmin:
            self._GetState()
            self._PrintState()
            self._SendState()
            
            if abs(self.roll_Real)>=70 or abs(self.pitch_Real)>=70 or getKey("Escape")!=0:
                self._Kill()
        
    def _SetInitialState(self):
        self.thrust_mult = 1
        self.thrust_step = 100#250#500
        # Lift-off at approx. 45000
        self.thrust = 50e3#48e3#45e3#35e3#30e3#20e3
        self.thrustmin = 30e3
        self.thrustmax = 55e3#50e3#45e3#40e3#38e3#35e3#3e30#45e3#25e3
        self.pitch = 0
        self.roll = 0
        self.yawrate = 0

        self.roll_Real  = 0.
        self.pitch_Real = 0.
        self.yaw_Real   = 0.
        
    def _SetCalibratedState(self):
        # Positive: Front || Negative: Back
        self.pitch = 40#38#35#32#28#-28
        # Positive: Right || Negative: Left
        self.roll  = -22#-20#-18#-15#-10#-2
        
    def _GetState(self):
        # Climb & Decent
        if self.thrust >= self.thrustmax:
            self.thrust_mult = -1
        self.thrust += self.thrust_step * self.thrust_mult
        
        self.Stabilize = False
        if self.Stabilize:
            # Stabilize
            if self.roll_Real<self.roll:
                self.roll+=1.
            elif self.roll_Real>self.roll:
                self.roll-=1.
            if self.pitch_Real<self.pitch:
                self.roll+=1.
            elif self.pitch_Real>self.pitch:
                self.pitch-=1.
        
    def _SendState(self):
        self._cf.commander.send_setpoint(self.roll,self.pitch,self.yawrate,self.thrust)
        time.sleep(0.1)

    def _PrintState(self):
        print "-"*30
        print "Set Data:"
        print PH+"Thrust: "+str(round(self.thrust,2))
        print PH+"Roll:   "+str(round(self.roll,2))
        print PH+"Pitch:  "+str(round(self.pitch,2))
        print PH+"Yaw:    "+str(round(self.yawrate,2))
        
    def _SetGetData(self):
        
        # The definition of the logconfig can be made before connecting
        self._lg_stab = LogConfig(name="Stabilizer", period_in_ms=10)
        self._lg_stab.add_variable("stabilizer.roll", "float")
        self._lg_stab.add_variable("stabilizer.pitch", "float")
        self._lg_stab.add_variable("stabilizer.yaw", "float")

        # Adding the configuration cannot be done until a Crazyflie is
        # connected, since we need to check that the variables we
        # would like to log are in the TOC.
        self._cf.log.add_config(self._lg_stab)
        if self._lg_stab.valid:
            # This callback will receive the data
            self._lg_stab.data_received_cb.add_callback(self._stab_log_data)
            # This callback will be called on errors
            self._lg_stab.error_cb.add_callback(self._stab_log_error)
            # Start the logging
            self._lg_stab.start()
        else:
            print("Could not add logconfig since some variables are not in TOC")

        # Start a timer to disconnect in 10s
        t = Timer(20, self._cf.close_link)
        t.start()

    def _stab_log_error(self, logconf, msg):
        """Callback from the log API when an error occurs"""
        print "Error when logging %s: %s" % (logconf.name, msg)

    def _stab_log_data(self, timestamp, data, logconf):
        """Callback froma the log API when data arrives"""
        #print "[%d][%s]: %s" % (timestamp, logconf.name, data)
        
        self.data=data
        self.roll_Real  = data['stabilizer.roll']
        self.pitch_Real = data['stabilizer.pitch']
        self.yaw_Real   = data['stabilizer.yaw']

        # print "-"*30
        # print "Received Data:"
        # print PH+"Roll:  ",data['stabilizer.roll']
        # print PH+"Pitch: ",data['stabilizer.pitch']
        # print PH+"Yaw:   ",data['stabilizer.yaw']
        

    def _Kill(self):
        print ">>>Killing Drone<<<"
        self._cf.commander.send_setpoint(0, 0, 0, 0)
        # Make sure that the last packet leaves before the link is closed
        # since the message queue is not flushed before closing
        time.sleep(0.1)
        self._cf.close_link()

if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)
    # Scan for Crazyflies and use the first one found
    print "Scanning interfaces for Crazyflies..."
    available = cflib.crtp.scan_interfaces()
    print "Crazyflies found:"
    for i in available:
        print PH,i[0]
    print

    if len(available) > 0:
        le = CrazyflieControl(available[0][0])
    else:
        print "No Crazyflies found, cannot run example"