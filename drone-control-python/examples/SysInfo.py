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
        if self.OS=="Windows":
            from win32api import GetSystemMetrics
            self.Resolution = np.int_([GetSystemMetrics(0),GetSystemMetrics(1)])
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

    def Print(self):
        # System Information
        print ">>> System Information: ("+self.Date+")"

        print PH+"Computer Info:"
        print PH*2+"Computer Name: "+self.PCName
        print PH*2+"Processor: "+self.Processor+" ("+self.Machine+")"
        print PH*2+"Screen Resolution: ("+str(self.Resolution[0])+","+str(self.Resolution[1])+") px"
        print PH*2+"Machine Epsilon: "+str(self.epsilon)+" (Roundoff = e-"+str(self.re)+")"

        print PH+"Program Info:"
        print PH*2+"Rootfolder: "+self.Rootpath

        print PH+"OS Info:"
        print PH*2+"Operating System: "+self.OS+" "+self.OS_Release+" ["+self.Platform+"]"
        print PH*3+"OS Version: "+self.OS_Version

        print PH+"Python Info:"
        print PH*2+"Python version: "+self.PythonVersion
        print PH*2+"Interpreter Architecture: "+"Bits - '"+str(self.InterpreterArchitecture[0])+"'' | Linkage - '"+str(self.InterpreterArchitecture[1])+"'"
        print PH*2+"Compiler: "+self.Compiler
        print PH*2+"Implementation: "+self.PythonImplementation
    
        print PH+"TTY Info:"
        print PH*2+"ANSI Support: "+str(self.ANSI)
        
SysInfo=SysInfo()