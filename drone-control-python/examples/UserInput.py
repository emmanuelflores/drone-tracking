# -*- coding: utf-8 -*-
"""
Created on Tuesday 13.01.2015
Development plattform: Spyder

Script:             UserInput.py
Description:        Gets User Keyboard Input Crossplatform (Windows/Linux)

Project title:       Compact Copters - Flight Simulator
Project version:     1.0
Author:              Henricus N. Basien
Author E-Mail:       Henricus@Basien.de
Copyright:           Copyright (c) 2014 CompactCopters
Description:         Global Drone-Swarm Flightsimulator

"""

#==============================================================================
# Import
#==============================================================================

# Internal
from SysInfo import SysInfo

# External
if SysInfo.OS=="Windows":
    from win32api import GetAsyncKeyState
    import win32con
elif SysInfo.OS=="Linux":
    import struct
    import fcntl
    import os

#============================================================================================================================================================
# Runtime
#============================================================================================================================================================

def Update():
    
    if SysInfo.OS=="Windows":
        pass

    elif SysInfo.OS=="Linux":
        events = getEvents()

#============================================================================================================================================================
# Keyboard
#============================================================================================================================================================

def getKey(key):
    if SysInfo.OS=="Windows":
        return getKey_Windows(key)
        
    elif SysInfo.OS=="Linux":
        return getKey_Linux(key)

#==============================================================================
# Windows
#==============================================================================

def getKey_Windows(key):

    if len(key)==1:
        if ord(key)>=48 and ord(key)<=57: # 0-9
            key=ord(key)
        elif ord(key)>=65 and ord(key)<=90: # A-Z
            key=ord(key)
        elif ord(key)>=97 and ord(key)<=122: # a-z
            key=ord(key)-32
    else:
        key = WindowsKeyDict[key]

    return GetAsyncKeyState(key)

#------------------------------------------------------------------------------
# Dictionary
#------------------------------------------------------------------------------

if SysInfo.OS=="Windows":
    WindowsKeyDict = dict()

    WindowsKeyDict["Shift_L"]   = win32con.VK_LSHIFT
    WindowsKeyDict["Enter"]     = win32con.VK_RETURN
    WindowsKeyDict["Escape"]    = win32con.VK_ESCAPE
    WindowsKeyDict["Ctrl"]      = win32con.MOD_CONTROL
    WindowsKeyDict["Control"]   = win32con.MOD_CONTROL
    WindowsKeyDict["Delete"]    = win32con.VK_DELETE

    WindowsKeyDict["Right"]     = win32con.VK_RIGHT
    WindowsKeyDict["Left"]      = win32con.VK_LEFT
    WindowsKeyDict["Up"]        = win32con.VK_UP
    WindowsKeyDict["Down"]      = win32con.VK_DOWN

    WindowsKeyDict["Page Up"]   = win32con.VK_PRIOR
    WindowsKeyDict["Page Down"] = win32con.VK_NEXT

    keys = {
    "shift": win32con.MOD_SHIFT
    , "control": win32con.MOD_CONTROL
    , "ctrl": win32con.MOD_CONTROL
    , "alt": win32con.MOD_ALT
    , "win": win32con.MOD_WIN
    , "up": win32con.VK_UP
    , "down": win32con.VK_DOWN
    , "left": win32con.VK_LEFT
    , "right": win32con.VK_RIGHT
    , "pgup": win32con.VK_PRIOR
    , "pgdown": win32con.VK_NEXT
    , "home": win32con.VK_HOME
    , "end": win32con.VK_END
    , "insert": win32con.VK_INSERT
    , "enter": win32con.VK_RETURN
    , "return": win32con.VK_RETURN
    , "tab": win32con.VK_TAB
    , "space": win32con.VK_SPACE
    , "backspace": win32con.VK_BACK
    , "delete": win32con.VK_DELETE
    , "del": win32con.VK_DELETE
    , "apps": win32con.VK_APPS
    , "popup": win32con.VK_APPS
    , "escape": win32con.VK_ESCAPE
    , "npmul": win32con.VK_MULTIPLY
    , "npadd": win32con.VK_ADD
    , "npsep": win32con.VK_SEPARATOR
    , "npsub": win32con.VK_SUBTRACT
    , "npdec": win32con.VK_DECIMAL
    , "npdiv": win32con.VK_DIVIDE
    , "np0": win32con.VK_NUMPAD0
    , "numpad0": win32con.VK_NUMPAD0
    , "np1": win32con.VK_NUMPAD1
    , "numpad1": win32con.VK_NUMPAD1
    , "np2": win32con.VK_NUMPAD2
    , "numpad2": win32con.VK_NUMPAD2
    , "np3": win32con.VK_NUMPAD3
    , "numpad3": win32con.VK_NUMPAD3
    , "np4": win32con.VK_NUMPAD4
    , "numpad4": win32con.VK_NUMPAD4
    , "np5": win32con.VK_NUMPAD5
    , "numpad5": win32con.VK_NUMPAD5
    , "np6": win32con.VK_NUMPAD6
    , "numpad6": win32con.VK_NUMPAD6
    , "np7": win32con.VK_NUMPAD7
    , "numpad7": win32con.VK_NUMPAD7
    , "np8": win32con.VK_NUMPAD8
    , "numpad8": win32con.VK_NUMPAD8
    , "np9": win32con.VK_NUMPAD9
    , "numpad9": win32con.VK_NUMPAD9
    , "f1": win32con.VK_F1
    , "f2": win32con.VK_F2
    , "f3": win32con.VK_F3
    , "f4": win32con.VK_F4
    , "f5": win32con.VK_F5
    , "f6": win32con.VK_F6
    , "f7": win32con.VK_F7
    , "f8": win32con.VK_F8
    , "f9": win32con.VK_F9
    , "f10": win32con.VK_F10
    , "f11": win32con.VK_F11
    , "f12": win32con.VK_F12
    , "f13": win32con.VK_F13
    , "f14": win32con.VK_F14
    , "f15": win32con.VK_F15
    , "f16": win32con.VK_F16
    , "f17": win32con.VK_F17
    , "f18": win32con.VK_F18
    , "f19": win32con.VK_F19
    , "f20": win32con.VK_F20
    , "f21": win32con.VK_F21
    , "f22": win32con.VK_F22
    , "f23": win32con.VK_F23
    , "f24": win32con.VK_F24
}


#==============================================================================
# Linux
#==============================================================================

def getKey_Linux(key):
       
    # Check Events
    KeyCode = LinuxKeyDict[key]

    for event in events:

        if KeyCode==getCodefromEvent(event):
            return 1

    return 0

#------------------------------------------------------------------------------
# Preliminaries
#------------------------------------------------------------------------------

if SysInfo.OS=="Linux":
    # Initialize Device
    format = 'llHHI'
    event_size = struct.calcsize(format)
     
    dev = open('/dev/input/event3', 'rb')
    fd = dev.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    # Initialize Events
    events=[]

#------------------------------------------------------------------------------
# Dictionary
#------------------------------------------------------------------------------

if SysInfo.OS=="Linux":

    LinuxKeyDict = dict()

    LinuxKeyDict["A"] = 30
    LinuxKeyDict["B"] = 48
    LinuxKeyDict["C"] = 46
    LinuxKeyDict["D"] = 32
    LinuxKeyDict["E"] = 18
    LinuxKeyDict["F"] = 33
    LinuxKeyDict["G"] = 34
    LinuxKeyDict["H"] = 35
    LinuxKeyDict["I"] = 23
    LinuxKeyDict["J"] = 36
    LinuxKeyDict["K"] = 37
    LinuxKeyDict["L"] = 38
    LinuxKeyDict["M"] = 50
    LinuxKeyDict["N"] = 49
    LinuxKeyDict["O"] = 24
    LinuxKeyDict["P"] = 25
    LinuxKeyDict["Q"] = 16
    LinuxKeyDict["R"] = 19
    LinuxKeyDict["S"] = 31
    LinuxKeyDict["T"] = 20
    LinuxKeyDict["U"] = 22
    LinuxKeyDict["V"] = 47
    LinuxKeyDict["W"] = 17
    LinuxKeyDict["X"] = 45
    LinuxKeyDict["Y"] = 44
    LinuxKeyDict["Z"] = 21

    LinuxKeyDict["0"] = 11
    LinuxKeyDict["1"] = 2
    LinuxKeyDict["2"] = 3
    LinuxKeyDict["3"] = 4
    LinuxKeyDict["4"] = 5
    LinuxKeyDict["5"] = 6
    LinuxKeyDict["6"] = 7
    LinuxKeyDict["7"] = 8
    LinuxKeyDict["8"] = 9
    LinuxKeyDict["9"] = 10

    LinuxKeyDict["Shift_L"]   = 42
    LinuxKeyDict["Enter"]     = 28
    LinuxKeyDict["Escape"]    = 1

    LinuxKeyDict["Right"]     = 106
    LinuxKeyDict["Left"]      = 105
    LinuxKeyDict["Up"]        = 103
    LinuxKeyDict["Down"]      = 108

    LinuxKeyDict["Page Up"]   = 104
    LinuxKeyDict["Page Down"] = 109

#------------------------------------------------------------------------------
# Additional Functions
#------------------------------------------------------------------------------

def getEvents():
    # Get Events
    global events
    events=[]

    while True:
        try:
            events.append(dev.read(event_size))

        except IOError:
            return# events

def getCodefromEvent(event):
    
    #event=str(event)

    #data=[datum.strip(" ") for datum in event.split(",")]

    #Code  = int(data[1].split(" ")[1])
    #Type  = int(data[2].split(" ")[1])
    #Value = int(data[3].split(" ")[1])
    

    tv_sec, tv_usec, typ, Code, Value = struct.unpack(format, event)

    if Value>2 or Code==0:
        return False
    else:
        return Code


'''
class Hotkey(object):

    def __init__(self, keyId, modifiers, virtualkeys, execute):

        self.keyId = keyId
        self.modifiers = modifiers
        self.virtualkeys = virtualkeys
        self.execute = execute

    def register(self, window):
        """
        Registers the hotkeys into windows
        Returns true on success
        Returns false on error
        """

        if ctypes.windll.user32.RegisterHotKey(window.hWindow
                , self.keyId
                , self.modifiers
                , self.virtualkeys):

            return True

        else:

            return False

    def unregister(self, window):
        """
        Unregisters the hotkeys that are created on initialization
        """

        ctypes.windll.user32.UnregisterHotKey(window.hWindow, self.keyId)

'''