
from hc_wall import *
from hc_robotmap import *
from hc_button import *
from Tkinter import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg




# Initialization of GUI
bounds = boundaries(world_size,wall_width) 
walls = wall(wall_width,wall_location)
root = Tk()
frame1= Frame(root)
frame1.pack(fill=BOTH)
wall_canvas = Canvas(frame1,width=500,height=500,bg="white")
wall_canvas.pack(side=LEFT)


# Robot map
r = Canvas(frame1,width=500,height=500,bg="white")
r.pack(side=RIGHT)
fig = plt.figure(figsize=(6.15,6.15),facecolor='w',edgecolor='w')
canvas = FigureCanvasTkAgg(fig, master=r)
canvas.get_tk_widget().pack(side=RIGHT)

# Real MAp
walls.draw(wall_width, wall_location, wall_canvas)
bounds.draw(origin, wall_canvas)

parray = bounds.boundary_grid(origin,wall_canvas)
warray = walls.wall_grid(wall_width,wall_location,wall_canvas)



#KNOPPEN

frame2 = Frame(root)
frame2.pack()
start = Button(frame2,text="START", width=10,command=start)
start.grid(row=0,column=0)
stop = Button(frame2,text="STOP",width=10,command=stop)
stop.grid(row=0,column=1)
boost = Button(frame2,text="BOOST", width=10,command=boost)
boost.grid(row=0,column=2)
slow = Button(frame2,text="SLOW", width=10,command=slow)
slow.grid(row=0,column=3)



root.mainloop()


