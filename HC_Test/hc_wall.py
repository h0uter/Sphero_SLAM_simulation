# describes the walls which are placed in the world
from tkinter import *
from math import sin, cos, pi, fabs
from numpy import sign
import numpy as np

""" This file will be used as an import, where the variables inside the object will be given in the master python.

the variables: 
    wall_width = width of the used wall in the canvas
    wall_location = An array whichi gives the starting location of each wall piece
    wall_canvas = gives the size of the Canvas, more info @ http://effbot.org/tkinterbook/canvas.htm    -> bij strinivas is wall_canvas = w

    Example wall location  [ origin = (2,2), worldsize = (498,498)]
      =[[origin[0]+(world_size[0])/4,origin[1]+wall_width,origin[0]+(world_size[0])/4,origin[1]+wall_width+(world_size[1])*3/4],
                    [origin[0]+(world_size[0])/2,origin[1]+wall_width+(world_size[1])*1/4,origin[0]+(world_size[0])/2,origin[1]-wall_width+world_size[1]],
                    [origin[0]+(world_size[0])*3/4,origin[1]+wall_width,origin[0]+(world_size[0])*3/4,origin[1]+wall_width+(world_size[1])*3/4]] 
    
"""


"VARIABLES"

origin = (2,2)
world_size = (498, 498)   # 750,750
wall_width = 10
wall_heigth= world_size[0] *3 /4


ww= wall_width
wh= wall_heigth
ws= world_size #wallheight

wl1= [ws[0] *1 /4   , ww              ,   (ws[0] *1 / 4) + ww     , wh]
wl2= [ws[0] *2 /4   , ww+ (ws[0]/4)   ,   (ws[0] *2 / 4) + ww     , (ww + ws[0]/4) +   wh - 2*ww ]
wl3= [ws[0] *3 /4   , ww              ,   (ws[0] *3 / 4) + ww     , wh]


wl1_ar= origin[0] +np.array(wl1)
wl2_ar= origin[0] +np.array(wl2)
wl3_ar= origin[0] +np.array(wl3)

wall_location=      [wl1_ar, wl2_ar, wl3_ar]

"CLASSES INSIDE WALLS AND BOUNDARIE WALLS"

class wall(object):
    def __init__(self,wall_width,wall_location):
        self.warray = []
        self.wall_width = wall_width 

    # this definition makes a wall by drawing lines between the given point, more info@ http://effbot.org/tkinterbook/canvas.htm
    #w.create_line(Start_X, Start_Y, Einde_X, Einde_Y)
    #range(len(loc)) -> range( lengte( wall_location)))
    def draw(self, wall_width, wall_location, wall_canvas):
        for i in range(len(wall_location)):
            #m = self.slope(wall_location[i])
            ww=wall_width
            wc=wall_canvas
            wl=wall_location
            wc.create_rectangle(wl[i][0],wl[i][1],wl[i][2],wl[i][3])

    def wall_grid(self,ww,loc,w):
        
        d = 100  # Discretization of the grid
        
        for i in range(len(loc)):
            ws = loc[i][:2]
            we = loc[i][2:]
            for i in range(d):
                self.warray.append([ws[0]+sign(we[0]-ws[0])*(we[0]-ws[0])/d,
                                   ws[1]+sign(we[1]-ws[1])*(we[1]-ws[1])*i/d])
                w.create_line(self.warray[-1][0]+sign(we[1]-ws[1])*ww,self.warray[-1][1]+sign(we[0]-ws[0])*ww/2-5,
                              self.warray[-1][0]+sign(we[1]-ws[1])-1,self.warray[-1][1]+sign(we[0]-ws[0])*ww/2-5)
                
        return self.warray
    
"""
            wc.create_line(wl[i][0],wl[i][1],wl[i][2],wl[i][1])
            wc.create_line(wl[i][0],wl[i][1],wl[i][0],wl[i][3])
            wc.create_line(wl[i][2],wl[i][1],wl[i][2],wl[i][3])
            wc.create_line(wl[i][0],wl[i][3],wl[i][2],wl[i][3])
""" 






class boundaries(object):
    
    def __init__(self,world_size,wall_width):
        self.world_size = world_size
        self.wall_width = wall_width
        self.parray = []   # Consider preallocation for faster memory access
        
    def draw(self,origin,w):
        a = origin[0] 
        b = origin[1]    # to be added in the main loop
        # Outer boundary
        w.create_line(a,b,a+self.world_size[0],b)
        w.create_line(a+self.world_size[0],b, a+self.world_size[0],b+self.world_size[1])
        w.create_line(a,b,a,b+self.world_size[1])
        w.create_line(a,b+self.world_size[1],a+self.world_size[0],b+self.world_size[1])
        
        # Inner boundary
        w.create_line(a+self.wall_width,b+self.wall_width,
                      a-self.wall_width+self.world_size[0],b+self.wall_width)
        w.create_line(a-self.wall_width+self.world_size[0],b+self.wall_width, 
                      a-self.wall_width+self.world_size[0],b-self.wall_width+self.world_size[1])
        w.create_line(a+self.wall_width,b+self.wall_width,
                      a+self.wall_width,b-self.wall_width+self.world_size[1])
        w.create_line(a+self.wall_width,b-self.wall_width+self.world_size[1],
                      a-self.wall_width+self.world_size[0],b-self.wall_width+self.world_size[1])
        
    def boundary_grid(self,origin,w): # Defining the probability grid for the boundary by taking input as the corners
        # Assuming corners are available in the form of a list (given in an sequential fashion)
        a = origin[0]
        b = origin[1]
        d = 100     # Extent or level of discretization 
        
        # Addition of corners in a clockwise fashion
        corner = []
        corner.append([a + self.wall_width, b + self.wall_width])
        corner.append([a-self.wall_width+self.world_size[0],b+self.wall_width])
        corner.append([a-self.wall_width+self.world_size[0],b-self.wall_width+self.world_size[1]])
        corner.append([a+self.wall_width,b-self.wall_width+self.world_size[1]])

        for j in range(len(corner)):
            length = self.length_boundary(corner[j%len(corner)],corner[(j+1)%len(corner)])
            if length[1] == -1:
                print "Error in computing slope - Not a rectilinear world"
                sys.exit()

            for i in range(d):
                self.parray.append([corner[j][0]+sign(corner[(j+1)%len(corner)][0]-corner[j%len(corner)][0])*sin(length[1])*length[0]*i/d,
                                    corner[j][1]+sign(corner[(j+1)%len(corner)][1]-corner[j%len(corner)][1])*cos(length[1])*length[0]*i/d,0])
                w.create_line(self.parray[-1][0],self.parray[-1][1],
                              self.parray[-1][0]+sign(corner[(j+1)%len(corner)][1]-corner[j%len(corner)][1])*self.wall_width,
                              self.parray[-1][1]-sign(corner[(j+1)%len(corner)][0]-corner[j%len(corner)][0])*self.wall_width)
#                 w.create_rectangle(self.parray[-1][0],self.parray[-1][1],
#                                    self.parray[-2][0]+sign(corner[(j+1)%len(corner)][1]-corner[j%len(corner)][1])*self.wall_width,
#                                    self.parray[-2][1]-sign(corner[(j+1)%len(corner)][0]-corner[j%len(corner)][0])*self.wall_width)
            w.create_line(corner[j%len(corner)][0],corner[j%len(corner)][1],
                          corner[j%len(corner)][0]+sign(corner[j%len(corner)][1]-corner[(j-1)%len(corner)][1])*self.wall_width,
                          corner[j%len(corner)][1]-sign(corner[j%len(corner)][0]-corner[(j-1)%len(corner)][0])*self.wall_width)
        return self.parray    
#     def histogram_distribution(self,collision,parray):
   
    def length_boundary(self,cornerA,cornerB):
        
        a = max(fabs(cornerA[0]-cornerB[0]),fabs(cornerA[1]-cornerB[1])) # length of the line
        # To compute the slope of the line
        if cornerA[0]-cornerB[0]==0:
            b = 0
        elif cornerA[1]-cornerB[1]==0:
            b = pi/2
        else: # It is already in clockwise fashion; to report if something goes false
            b = -1
            
        return (a,b)
    
if __name__=="__main__":
    sri = boundaries(world_size,wall_width)
