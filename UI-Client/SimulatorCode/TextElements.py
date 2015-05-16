"""
Created on Thursday 28.08.2014
Development plattform: Spyder

Script:             TextElements.py
Description:        Defines Text Elements for visual Text Output.

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
# Elements
#==============================================================================

if "Linux" == SysInfo.OS:
    sl='/'
elif "Windows" == SysInfo.OS:
    sl='\\'


PH = " "*3

breakline   ="_"*100+"\n"

#seperatorL  ="-"*100+"\n"
#seperatorM  ="-"*50+"\n"
#seperatorS  ="-"*30+"\n"
#seperatorXS ="-"*15#+"\n"

def seperator(size):
    '''
    Verified = True
    Gives a seperator string consisting of "-"'s of a given length.
    '''
    elem="-"

    arg=size.split("_")
    if len(arg)>1:
        if arg[1].upper()=="T":
            elem="_"
    size=arg[0].upper()
    
    if size=="L":
        return elem*100+"\n"
    elif size=="M":
        return elem*50+"\n"
    elif size=="S":
        return elem*30+"\n"
    elif size=="XS":
        return elem*15#+"\n"

def CutNegative(Nr):

    if Nr<0:
        Nr=0
    return Nr

def StringWithBlankspace(Text,NrSpaces):
    if isinstance(Text, str):
        #Text = Text.encode('utf8')
        Text = unicode(Text, "utf-8")
    elif isinstance(Text,unicode):
        pass
    else:
       Text = str(Text).encode('utf8')

    return (Text+" "*CutNegative(NrSpaces-len(Text))).encode('utf8')