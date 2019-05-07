
from hc_wall import wall
from Tkinter import *



origin = (2,2)
world_size = (498, 498)   # 750,750
wall_width = 10
wall_location = [[origin[0]+(world_size[0])/4,origin[1]+wall_width,origin[0]+(world_size[0])/4,origin[1]+wall_width+(world_size[1])*3/4],
                    [origin[0]+(world_size[0])/2,origin[1]+wall_width+(world_size[1])*1/4,origin[0]+(world_size[0])/2,origin[1]-wall_width+world_size[1]],
                    [origin[0]+(world_size[0])*3/4,origin[1]+wall_width,origin[0]+(world_size[0])*3/4,origin[1]+wall_width+(world_size[1])*3/4]] 
#wall_location = [2+498/4   ,  2+width /4   , ]
    
wall = wall(wall_width,wall_location)

master = Tk()
wall_canvas = Canvas(master,width=500,height=500,bg="white")
wall.draw(wall_width, wall_location, wall_canvas)

master.mainloop()