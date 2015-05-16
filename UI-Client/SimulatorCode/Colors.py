"""
Created on Friday 11.04.2014
Development plattform: Spyder

Script:             Colors.py
Description:        Define colors

Project title:       CC Simulation Environment
Project version:     1.0
Author:              Henricus N. Basien
Author E-Mail:       Henricus@Basien.de
Copyright:           Copyright (c) 2014 CompactCopters
Description:         Simulated computational model for the Unicop2

"""

#==============================================================================
# Imports
#==============================================================================

import numpy as np
from scipy import misc
import os
import colorsys

from colorsys import rgb_to_hsv

PH=" "*3

#==============================================================================
# Settings
#==============================================================================

ColorRange=1.

#===============================================================================
# Colors [RGB = Red, Green, Blue value, scale: 0-255]
#===============================================================================

# Define Color Library
class ColorLibrary():
    def __init__(self):
        self.name="Color Library"
        self.Collections=dict()
    def addCollection(self,name,Collection):
        self.Collections[name]=Collection
        
    def alterLibrary(self,ColorRange):
        for Collection in self.Collections:
            Collection = ColorLibrary.Collections[Collection]
            for color in Collection:
                value=Collection[color]
                value=np.array(value)
                if ColorRange!=255:
                    value=np.array(value).astype(float)/255*ColorRange
                Collection[color]=value
    def generateOverview(self,path):
        # Settings
        Patchsize=200
        ext=".png"

        # Read Collections        
        path=path+"\\"+"ColorLibrary-Overview\\"
        if not os.path.exists(path):
            os.makedirs(path)
        print "Color Overview is being generated in : "+path+"\n"
            
        for CollectionKey in self.Collections:
            print "Reading Collection '"+CollectionKey+"'"
            Collection=self.Collections[CollectionKey]
            
            CollectionPath=path+CollectionKey+"\\"
            if not os.path.exists(CollectionPath):
                os.makedirs(CollectionPath)
            
            for ColorName in Collection:
                Color=Collection[ColorName]
                hue=int(round(rgb_to_hsv(Color[0]/255.,Color[1]/255.,Color[2]/255.)[0]*360,0))#round(color.rgb_to_hsv([c/255 for c in Color])[0]*255,2)
                print PH+ColorName+" - "+str(Color)+" | Hue: "+str(hue)
                # Make Patch
                patchName="("+str(hue)+") "+ColorName+" "+str(Color)
                print PH*2+patchName
                #raw_input("...")
                
                patch=np.zeros([Patchsize,Patchsize,3],dtype=np.uint8)
                for i in range(Patchsize):
                    for j in range(Patchsize):
                        patch[i,j]=Color
                
                misc.imsave(CollectionPath+patchName+ext,patch)
            print

    def generateFullHueOverview(self,path):
        # Settings
        Patchsize=100
        ext=".png"

        # Read Collections        
        path=path+"\\"+"ColorLibrary-Overview\\"
        if not os.path.exists(path):
            os.makedirs(path)
            
        CollectionPath=path+"Full Hue Overview\\"
        if not os.path.exists(CollectionPath):
            os.makedirs(CollectionPath)
        print "Full Hue Color Range Overview is being generated in : "+CollectionPath+"\n"
        
        hrange=360
        dh=1.
        s=1.
        v=1.
        nrElements=int(hrange/dh)
        go=raw_input("Do you want to create "+str(nrElements)+" Patches? (y/n): ")
        if go.lower()=="y" or go.lower()=="j":
            for h in np.arange(0.,hrange+dh,dh):
    #            print h
                h/=hrange
    #            raw_input(str(h))
                h=round(h,4)
            
                # Make Color
                HSV_Color=[h,s,v]
    
                # Make Patch
                self.CreatePatch(CollectionPath,Color=HSV_Color,HSV=True,Patchsize=Patchsize,ext=ext)
                        
            print "\n"+"-"*25+"Full Color Overview has been created!"+"-"*25
        else:
            print"Color Overview Generation Aborted!"

    def generateFullHSVOverview(self,path):
        # Settings
        Patchsize=100
        ext=".png"

        # Read Collections        
        path=path+"\\"+"ColorLibrary-Overview\\"
        if not os.path.exists(path):
            os.makedirs(path)
            
        CollectionPath=path+"Full HSV Overview\\"
        if not os.path.exists(CollectionPath):
            os.makedirs(CollectionPath)
        print "Full HSV/RGB Color Range Overview is being generated in : "+CollectionPath+"\n"
        
        hrange=360
        dh=6.
        ds=0.1
        dv=0.1
        nrElements=int(hrange/dh)*int(1./ds)*int(1./dv)
        go=raw_input("Do you want to create "+str(nrElements)+" Patches? (y/n): ")
        if go.lower()=="y" or go.lower()=="j":
            for h in np.arange(0.,hrange+dh,dh):
                h+=dh*20
    #            print h
                h/=hrange
    #            raw_input(str(h))
                h=round(h,4)
                for s in np.arange(0.,1+ds,ds):
                    s=round(s,4)
                    for v in np.arange(0.,1+dv,dv):
                        v=round(v,4)

                        # Make Color
                        HSV_Color=[h,s,v]

                        # Make Patch
                        self.CreatePatch(CollectionPath,Color=HSV_Color,HSV=True,Patchsize=Patchsize,ext=ext)
                        
            print "\n"+"-"*25+"Full Color Overview has been created!"+"-"*25
        else:
            print"Color Overview Generation Aborted!"

    def CreatePatch(self,path,Color,HSV=False,Patchsize=100,ext=".png"):
        if HSV:
            HSV_Color=Color
            h,s,v=HSV_Color
            HSV_Color[0]=int(HSV_Color[0]*360)
            RGB_Color=np.array(colorsys.hsv_to_rgb(h,s,v))
            RGB_Color=(RGB_Color*255).astype(int)
        else:
            RGB_Color=Color

        patch=np.zeros([Patchsize,Patchsize,3],dtype=np.uint8)
        for i in range(Patchsize):
            for j in range(Patchsize):
                patch[i,j]=RGB_Color#.astype(float)
        # Save Patch
        patchName=""
        if HSV:
            patchName+="HSV "+str(HSV_Color)+" - "
        patchName+="RGB "+str(RGB_Color)
        misc.imsave(path+patchName+ext,patch)
        print PH+patchName+" | has been saved."                    

ColorLibrary=ColorLibrary()

#==============================================================================
# CompactCopters Colors
#==============================================================================

CC_Colors=dict()
ColorLibrary.addCollection("CompactCopters Colors",CC_Colors)

CC_Colors["Blue_1"] = (0,100,255)

#==============================================================================
# Copter Colors
#==============================================================================

Copter_Colors=dict()
ColorLibrary.addCollection("Copter Colors",Copter_Colors)

Copter_Colors["Unicop-2"] = (0,0,0)
Copter_Colors["Aeromys"]  = (0,100,255)

#==============================================================================
# Custom Colors
#==============================================================================

Custom_Colors=dict()
ColorLibrary.addCollection("Custom Color-Library",Custom_Colors)

Custom_Colors["Sky_Blue"] = (72,194,240)

#==============================================================================
# Pre-Defined colors 
#==============================================================================

Colors=dict()
ColorLibrary.addCollection("PreDefined Color-Library",Colors)

'''(Evaluated Source: http://www.tayloredmktg.com/rgb/ )'''

# Whites
Colors["Snow"]                    =   (255,250,250)
Colors["Snow_2"]                  =   (238,233,233)
Colors["Snow_3"]                  =   (205,201,201)
Colors["Snow_4"]                  =   (139,137,137)
Colors["Ghost_White"]             =   (248,248,255)
Colors["White_Smoke"]             =   (245,245,245)
Colors["Gainsboro"]               =   (220,220,220)
Colors["Floral_White"]            =   (255,250,240)
Colors["Old_Lace"]                =   (253,245,230)
Colors["Linen"]                   =   (240,240,230)
Colors["Antique_White"]           =   (250,235,215)
Colors["Antique_White_2"]         =   (238,223,204)
Colors["Antique_White_3"]         =   (205,192,176)
Colors["Antique_White_4"]         =   (139,131,120)
Colors["Papaya_Whip"]             =   (255,239,213)
Colors["Blanched_Almond"]         =   (255,235,205)
Colors["Bisque"]                  =   (255,228,196)
Colors["Bisque_2"]                =   (238,213,183) 
Colors["Bisque_3"]                =   (205,183,158)
Colors["Bisque_4"]                =   (139,125,107)
Colors["Peach_Puff"]              =   (255,218,185)
Colors["Peach_Puff_2"]            =   (238,203,173)
Colors["Peach_Puff_3"]            =   (205,175,149)
Colors["Peach_Puff_4"]            =   (139,119,101)
Colors["Navajo_White"]            =   (255,222,173)
Colors["Moccasin"]                =   (255,228,181)
Colors["Cornsilk"]                =   (255,248,220)
Colors["Cornsilk_2"]              =   (238,232,205)
Colors["Cornsilk_3"]              =   (205,200,177)
Colors["Cornsilk_4"]              =   (139,136,120)
Colors["Ivory"]                   =   (255,255,240)
Colors["Ivory_2"]                 =   (238,238,224)
Colors["Ivory_3"]                 =   (205,205,193)
Colors["Ivory_4"]                 =   (139,139,131)
Colors["Lemon_Chiffon"]           =   (255,250,205)
Colors["Seashell"]                =   (255,245,238)
Colors["Seashell_2"]              =   (238,229,222)
Colors["Seashell_3"]              =   (205,197,191)
Colors["Seashell_4"]              =   (139,134,130)
Colors["Honeydew"]                =   (240,255,240)
Colors["Honeydew_2"]              =   (244,238,224)
Colors["Honeydew_3"]              =   (193,205,193)
Colors["Honeydew_4"]              =   (131,139,131)
Colors["Mint_Cream"]              =   (245,255,250)
Colors["Azure"]                   =   (240,255,255)
Colors["Alice_Blue"]              =   (240,248,255)
Colors["Lavender"]                =   (230,230,250)
Colors["Lavender_Blush"]          =   (255,240,245)
Colors["Misty_Rose"]              =   (255,228,225)
Colors["White"]                   =   (255,255,255)

# Blacks
Colors["Black"]                   =   (0,0,0)
Colors["Dark_Slate_Gray"]         =   (49,79,79)
Colors["Dim_Gray"]                =   (105,105,105)
Colors["Slate_Gray"]              =   (112,138,144)
Colors["Light_Slate_Gray"]        =   (119,136,153)
Colors["Gray"]                    =   (190,190,190)
Colors["Light_Gray"]              =   (211,211,211)

# Blues	
Colors["Blue"]                    =   (0,0,255)
Colors["Midnight_Blue"]           =   (25,25,112)
Colors["Navy"]                    =   (0,0,128)
Colors["Cornflower_Blue"]         =   (100,149,237)
Colors["Dark_Slate_Blue"]         =   (72,61,139)
Colors["Slate_Blue"]              =   (106,90,205)
Colors["Medium_Slate_Blue"]       =   (123,104,238)
Colors["Light_Slate_Blue"]        =   (132,112,255)
Colors["Medium_Blue"]             =   (0,0,205)
Colors["Royal_Blue"]              =   (65,105,225)
Colors["Blue"]                    =   (0,0,255)
Colors["Dodger_Blue"]             =   (30,144,255)
Colors["Deep_Sky_Blue"]           =   (0,191,255)
Colors["Sky_Blue"]                =   (135,206,250)
Colors["Light_Sky_Blue"]          =   (135,206,250)
Colors["Steel_Blue"]              =   (70,130,180)
Colors["Light_Steel_Blue"]        =   (176,196,222)
Colors["Light_Blue"]              =   (173,216,230)
Colors["Powder_Blue"]             =   (176,224,230)
Colors["Pale_Turquoise"]          =   (175,238,238)
Colors["Dark_Turquoise"]          =   (0,206,209)
Colors["Medium_Turquoise"]        =   (72,209,204)
Colors["Turquoise"]               =   (64,224,208)
Colors["Cyan"]                    =   (0,255,255)
Colors["Light_Cyan"]              =   (224,255,255)
Colors["Cadet_Blue"]              =   (95,158,160)

# Greens	
Colors["Medium_Aquamarine"]       =   (102,205,170)
Colors["Aquamarine"]              =   (127,255,212)
Colors["Dark_Green"]              =   (0,100,0)
Colors["Dark_Olive_Green"]        =   (85,107,47)
Colors["Dark_Sea_Green"]          =   (143,188,143)
Colors["Sea_Green"]               =   (46,139,87)
Colors["Medium_Sea_Green"]        =   (60,179,113)
Colors["Light_Sea_Green"]         =   (32,178,170)
Colors["Pale_Green"]              =   (152,251,152)
Colors["Spring_Green"]            =   (0,255,127)
Colors["Lawn_Green"]              =   (124,252,0)
Colors["Chartreuse"]              =   (127,255,0)
Colors["Medium_Spring_Green"]     =   (0,250,154)
Colors["Green_Yellow"]            =   (173,255,47)
Colors["Lime_Green"]              =   (50,205,50)
Colors["Yellow_Green"]            =   (154,205,50)
Colors["Forest_Green"]            =   (34,139,34)
Colors["Olive_Drab"]              =   (107,142,35)
Colors["Dark_Khaki"]              =   (189,183,107)
Colors["Khaki"]                   =   (240,230,140)
Colors["Green"]                   =   (0,255,0)

# Yellows	
Colors["Pale_Goldenrod"]          =   (238,232,170)
Colors["Light_Goldenrod_Yellow"]  =   (250,250,210)
Colors["Light_Yellow"]            =   (255,255,224)
Colors["Yellow"]                  =   (255,255,0)
Colors["Gold"]                    =   (255,215,0)
Colors["Light_Goldenrod"]         =   (238,221,130)
Colors["Goldenrod"]               =   (218,165,32)
Colors["Dark_Goldenrod"]          =   (184,134,11)

# Browns	
Colors["Rosy_Brown"]              =   (188,143,143)
Colors["Indian_Red"]              =   (205,92,92)
Colors["Saddle_Brown"]            =   (139,69,19)
Colors["Sienna"]                  =   (160,82,45)
Colors["Peru"]                    =   (205,133,63)
Colors["Burlywood"]               =   (222,184,135)
Colors["Beige"]                   =   (245,245,220)
Colors["Wheat"]                   =   (245,222,179)
Colors["Sandy_Brown"]             =   (244,164,96)
Colors["Tan"]                     =   (210,180,140)
Colors["Chocolate"]               =   (210,105,30)
Colors["Firebrick"]               =   (178,34,34)
Colors["Brown"]                   =   (165,42,42)

# Oranges	
Colors["Dark_Salmon"]             =   (233,150,122)
Colors["Salmon"]                  =   (250,128,114)
Colors["Light_Salmon"]            =   (255,160,122)
Colors["Orange"]                  =   (255,165,0)
Colors["Dark_Orange"]             =   (255,140,0)
Colors["Coral"]                   =   (255,127,80)
Colors["Light_Coral"]             =   (240,128,128)
Colors["Tomato"]                  =   (255,99,71)
Colors["Orange_Red"]              =   (255,69,0)
Colors["Red"]                     =   (255,0,0)

# Pinks/Violets	
Colors["Hot_Pink"]                =   (255,105,180)
Colors["Deep_Pink"]               =   (255,20,147)
Colors["Pink"]                    =   (255,192,203)
Colors["Light_Pink"]              =   (255,182,193)
Colors["Pale_Violet_Red"]         =   (219,112,147)
Colors["Maroon"]                  =   (176,48,96)
Colors["Medium_Violet_Red"]       =   (199,21,133)
Colors["Violet_Red"]              =   (208,32,144)
Colors["Violet"]                  =   (238,130,238)
Colors["Plum"]                    =   (221,160,221)
Colors["Orchid"]                  =   (218,112,214)
Colors["Medium_Orchid"]           =   (186,85,211)
Colors["Dark_Orchid"]             =   (153,50,204)
Colors["Dark_Violet"]             =   (148,0,211)
Colors["Blue_Violet"]             =   (138,43,226)
Colors["Purple"]                  =   (160,32,240)
Colors["Medium_Purple"]           =   (147,112,219)
Colors["Thistle"]                 =   (216,191,216)

#==============================================================================
# Predefinition Processing
#==============================================================================

ColorLibrary.alterLibrary(ColorRange)

#==============================================================================
# Generate Color Overview
#==============================================================================

#ColorLibrary.generateOverview("C:")
#ColorLibrary.generateFullHSVOverview("C:")
#ColorLibrary.generateFullHueOverview("C:")
