"""
Created on Thursday 21.06.2014
Development plattform: Spyder

Script:             SysInfo.py
Description:        Get & Output System information.

Project title:       Compact Copters - Flight Simulator
Project version:     1.0
Author:              Henricus N. Basien
Author E-Mail:       Henricus@Basien.de
Copyright:           Copyright (c) 2014 CompactCopters
Description:         Global Drone-Swarm Flightsimulator

"""

#==============================================================================
# Imports
#==============================================================================

# External
import sys,os,platform
import numpy as np
from math import log
from copy import copy
import datetime

PH=" "*3

def GetVPythonVersion():
    try:
        import visual
        return str(visual.__version__)

    except:
        try:
            visual.shapes
            visual.paths
            return "5.5"
        except:
            return "0"
            
class Monitor(): 
    
    def __init__(self,Nr,pos,Resolution,Name=None):
        self.Nr         = Nr
        if Name==None:
            self.Name   = "Monitor #"+str(Nr)
        else:
            self.Name   = Name
        self.pos        = np.array(pos).astype(int)
        self.Resolution = np.array(Resolution).astype(int)

        self.Info       = self.Name+": "+str(self.Resolution[0])+"x"+str(self.Resolution[1])+" "+str(self.pos)
        
#==============================================================================
# System Information
#==============================================================================

class SysInfo():
    '''
    Class that contains general system and program information.
    '''
    def __init__(self):
        ## OS/System & Software/Hardware Data

        # Structure
        self.Rootpath=""

        # Operating System
        self.Platform   = sys.platform
        self.OS         = platform.system()
        self.OS_Release = platform.release()
        self.OS_Version = platform.platform()

        # PC Info
        self.PCName    = platform.node()
        self.Processor = platform.processor()
        self.Machine   = platform.machine()

        # Python Info
        self.PythonVersion           = sys.version
        self.InterpreterArchitecture = platform.architecture()
        self.Compiler                = platform.python_compiler()
        self.PythonImplementation    = platform.python_implementation()

        # Resolution
        MainscreenNr = 1

        if self.OS=="Windows":            
            import win32api
            monitors = win32api.EnumDisplayMonitors()
            monitors.sort(key=lambda x: x[2][0])
            self.Monitors = []
            for i in range(len(monitors)):
                monitor = monitors[i]
                left,top,right,bottom = monitor[2]
                width = right - left
                height = bottom-top
                monitor = Monitor(Nr=i+1,pos=[left,top],Resolution=[width,height])
                self.Monitors.append(monitor)

                if monitor.Nr==MainscreenNr:
                    self.Mainscreen = monitor
                    self.Resolution = copy(monitor.Resolution)

            # from win32api import GetSystemMetrics
            # self.Resolution = np.int_([GetSystemMetrics(0),GetSystemMetrics(1)])
        elif self.OS=="Linux":
            import subprocess
            Resolution = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]
            self.Resolution = np.array(Resolution.strip("\n").split("x")).astype(int)

        # Machine Epsilon
        self.epsilon=sys.float_info.epsilon
        self.re=int(abs(log(self.epsilon, 10)))     -5 #! -n
        
        # Date
        date = datetime.date.today()
        self.Date = str(date.day)+"."+str(date.month)+"."+str(date.year)

        # ANSI Support
        self.ANSI = self.Check_ANSI_Support()

        # Module Versions
        self.GetModuleVersions()
        
    def Check_ANSI_Support(self):
        for handle in [sys.stdout, sys.stderr]:
            if (hasattr(handle, "isatty") and handle.isatty()) or ('TERM' in os.environ and os.environ['TERM']=='ANSI'):
                if platform.system()=='Windows' and not ('TERM' in os.environ and os.environ['TERM']=='ANSI'):
                    return "Windows console, no ANSI support!"

        return True   

    def GetModuleVersions(self):

        self.VPython_Version = int(GetVPythonVersion().split(".")[0])

    def Print(self,i=0):
        # System Information
        print ">>> System Information: ("+self.Date+")"

        print PH*(i)+"Computer Info:"
        print PH*(i+1)+"Computer Name: "+self.PCName
        print PH*(i+1)+"Processor: "+self.Processor+" ("+self.Machine+")"
        print PH*(i+1)+"Machine Epsilon: "+str(self.epsilon)+" (Roundoff = e-"+str(self.re)+")"
    
        print PH*(i)+"Monitors:"
        for monitor in self.Monitors:
            print PH*(i+1)+monitor.Info
        print PH*(i+1)+"Main Screen Resolution: ("+str(self.Resolution[0])+","+str(self.Resolution[1])+") px"

        print PH*(i)+"Program Info:"
        print PH*(i+1)+"Rootfolder: "+self.Rootpath

        print PH*(i)+"OS Info:"
        print PH*(i+1)+"Operating System: "+self.OS+" "+self.OS_Release+" ["+self.Platform+"]"
        print PH*(i+2)+"OS Version: "+self.OS_Version

        print PH*(i)+"Python Info:"
        print PH*(i+1)+"Python version: "+self.PythonVersion
        print PH*(i+1)+"Interpreter Architecture: "+"Bits - '"+str(self.InterpreterArchitecture[0])+"'' | Linkage - '"+str(self.InterpreterArchitecture[1])+"'"
        print PH*(i+1)+"Compiler: "+self.Compiler
        print PH*(i+1)+"Implementation: "+self.PythonImplementation
    
        print PH*(i)+"TTY Info:"
        print PH*(i+1)+"ANSI Support: "+str(self.ANSI)
        
SysInfo=SysInfo()

''' 
#Getting all Window Titels

import ctypes

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible
 
titles = []
def foreach_window(hwnd, lParam):
    if IsWindowVisible(hwnd):
        length = GetWindowTextLength(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowText(hwnd, buff, length + 1)
        titles.append(buff.value)
    return True
EnumWindows(EnumWindowsProc(foreach_window), 0)
 
for title in titles:
    print title

'''