# describes the walls which are placed in the world

from tkinter import *
from math import sin, cos, pi, fabs

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


class wall(object):
    def __init__(self,wall_width,wall_location):
        self.wall_array = []
        self.wall_with = wall_width 

    # this definition makes a wall by drawing lines between the given point, more info@ http://effbot.org/tkinterbook/canvas.htm
    #w.create_line(Start_X, Start_Y, Einde_X, Einde_Y)
    #range(len(loc)) -> range( lengte( wall_location)))
    def draw(self, wall_width, wall_location, wall_canvas):
        for i in range(len(wall_location)):
            m = self.slope(wall_location[i])
            ww=wall_width
            wc=wall_canvas
            wl=wall_location

            wc.create_line(wl[i][0]-m*ww/2,wl[i][1]-(1-m)*ww/2,wl[i][0]+m*ww/2,wl[i][1]+(1-m)*ww/2)
            wc.create_line(wl[i][2]-m*ww/2,wl[i][3]-(1-m)*ww/2,wl[i][2]+m*ww/2,wl[i][3]+(1-m)*ww/2)
            wc.create_line(wl[i][0]-m*ww/2,wl[i][1]-(1-m)*ww/2,wl[i][2]-m*ww/2,wl[i][3]-(1-m)*ww/2)
            wc.create_line(wl[i][0]+m*ww/2,wl[i][1]+(1-m)*ww/2,wl[i][2]+m*ww/2,wl[i][3]+(1-m)*ww/2)
        
        
    def slope(self,wall):
        ws = wall[:2]
        we = wall[2:]
        if fabs(ws[1]-we[1]) < 1e-3:
            m = 0
        elif fabs(ws[0]-we[0]) < 1e-3:
            m = 1
        else:
            m = -1
            print 'Error: Rectilinear walls are only allowed, check this wall {0}'.format(wall)
            sys.exit()
        return m




