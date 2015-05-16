infoText="""\
Created on Saturday 07.03.2015
"""
"""
Script:              PCPC.py
Description:         Main Script
"""
infoText+="""
Project title:       Personal Crazyflie Python Client
Project version:     1.0
Author:              Henricus N. Basien,Gourav Mahapatra
Author E-Mail:       Henricus@Basien.de
Copyright:           Copyright (c) 2015 Henricus N. Basien
Description:         Personal Crazyflie Python Client.
                     Controls (multiple) Crazyflie Nanodrone
"""
#==============================================================================
# Imports
#==============================================================================

## Sytem Paths
import sys
sys.path.append("Telemetry")
# sys.path.append("../lib") # FIXME: Has to be launched from within the example folder

## External
# Crazyflie Client
import cflib

## Internal
# Crazflie Control
from CrazyflieControl import CrazyflieControl,PH
# # Touch interfacce
# sys.path.append("../Multitouch")
# from touchtracer import TouchtracerApp
# from threading import Thread
# Thread(target=TouchtracerApp().run).start()

#==============================================================================
# Header
#==============================================================================

print r'''
______________________________________  
\______   \_   ___ \______   \_   ___ \ 
 |     ___/    \  \/|     ___/    \  \/ 
 |    |   \     \___|    |   \     \____
 |____|    \______  /____|    \______  /
                  \/                 \/
'''

print infoText+"\n"

#==============================================================================
# Program Initialization
#==============================================================================

print "_"*100+"\n"

raw_input(">Press Enter to start Program Initialization...")

print "_"*100+"\n"

def InitializeCrazyflieDrivers():
    '''
    Initialize the low-level drivers (don't list the debug drivers)
    '''
    cflib.crtp.init_drivers(enable_debug_driver=False)

def ScanForCrazyflies():
    '''
    Scan for Crazyflies and use the first one found
    '''
    
    print "Scanning interfaces for Crazyflies..."
    AvailableCrazyflies = cflib.crtp.scan_interfaces()
    
    NrCrazyflies = len(AvailableCrazyflies)
    if NrCrazyflies>0:
        print "Crazyflies found ("+str(NrCrazyflies)+"):"
        for i in AvailableCrazyflies:
            print PH,i[0]
        print

    return AvailableCrazyflies

def ConnectAndRun(PreferredChannel = 80):
    PreferredChannel = "radio://0/"+str(PreferredChannel)+"/250K"
    
    AvailableCrazyflies = ScanForCrazyflies()
    if len(AvailableCrazyflies) > 0:
        Channels = [CF[0] for CF in AvailableCrazyflies]
        if PreferredChannel in Channels:
            Channel = PreferredChannel
        else:
            Channel = Channels[0]
        print "Chosen Channel: '"+Channel+"'"#print "Attempt to connect to '"+Channel+"'"
        print "-"*35
        Crazyflie = CrazyflieControl(Channel)
        return Crazyflie
    else:
        print "No Crazyflies found, cannot run program!"
        return False
        
#==============================================================================
# Main Code
#==============================================================================
        
if __name__ == '__main__':

    InitializeCrazyflieDrivers()

    ConnectAttemptNr = 0

    while True:
        ConnectAttemptNr+=1
        print "Connection Attempt #"+str(ConnectAttemptNr)+"\n"+"-"*22
        if ConnectAndRun()==False:
            if raw_input("\n"+">>> Attempt Reconnect? (y/n): ").lower() in ["j","y",""]:
                print "\n"+"-"*50
            else:
                break
        else:
            while True:
                pass

print "\n"+"-"*3+"Main Program Terminated"+"-"*3