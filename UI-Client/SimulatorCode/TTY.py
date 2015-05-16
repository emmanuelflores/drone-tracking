"""
Created on Thursday 25.12.2014
Development plattform: Spyder

Script:              TTY.py
Description:         Defines TTY Interation Function

Project title:       Compact Copters - Flight Simulator
Project version:     1.0
Author:              Henricus N. Basien
Author E-Mail:       Henricus@Basien.de
Copyright:           Copyright (c) 2014 CompactCopters
Description:         Simulated computational model for the Unicop2

"""

#==============================================================================
# Imports
#==============================================================================

from SysInfo import SysInfo

#==============================================================================
# Functions
#==============================================================================

def PrintColor(string,prop='Black'):
    attributes = []
    attr,add="3",""
    
    if "_" in prop:
        prop,add=prop.split("_")
        if "B" in add:
            attr="4"
            
    props={\
    "Grey": "0",\
    "Red": "1",\
    "Green": "2",\
    "Yellow": "3",\
    "Blue": "4",\
    "Pink": "5",\
    "Lightblue": "6",\
    "White": "7",\
    }        
            
    if prop in props:
        if prop=='Underlined':
            attr=props[prop]  
        else:
            attr+=props[prop]
        
    attributes.append(attr)
    
    # Highlight
    if "H" in add:
        attributes.append('1')

    print '\x1b[%sm%s\x1b[0m' % (';'.join(attributes), string)

def PrintSpecial(string,prop=None):

    if SysInfo.ANSI==True and prop!=None:
        PrintColor(string,prop)
    else:
        print string