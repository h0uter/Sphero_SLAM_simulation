from __future__ import division
#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), '..\Strinivas\mayw3'))
	print(os.getcwd())
except:
	pass

#%%
from Tkinter import *
import tkFileDialog
from math import cos, pi, fabs, tan
from numpy import sign,arange, sin, array
import sys
from test_slam import Particle, FastSLAM
from boundaries import boundaries
from walls import walls
from Sphero_test import Sphero
import matplotlib as mpl
import copy
import matplotlib.pyplot as plt
import book_plot as bp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

def start():
    global pose, control, constraints, loop, radius, wall_width, world_size, flag, lw
    scale = 520
    loop = not(loop)
    t = 0
    pmeasurement = []
    while loop:# and i <=300:
        posep = pose 
        pose = fs.predict(pose,control)
        past_orient = pose[0][2]
        pose = s.check_collision(constraints, pose[0], posep, flag)# flag = wall_correction; measurement to be included as prior
        f=s.draw(pose[0])
        if pose[1] != -1:
            measurement = array([pose[0][0],pose[0][1],tan(pose[1]-past_orient)])
            w, wall, lw = fs.correct(measurement,pmeasurement)
            for i in range(len(wall)):
                if i==2 or i==4:
                    wall[i] = list(reversed(wall[i]))
            robot_map(wall,t)
            root.update()
            pmeasurement = measurement
        pose = pose[0]
#         i = i + 1

def stop():
    global loop, lw
    loop = not(loop)
    print "Tree",lw

def boost():
    global control
    control[0] = control[0] + 50
    if control[0] <= 0:
        control[0] =0

def slow():
    global control
    control[0] = control[0] - 50
    if control[0] <= 0:
        control[0] =0

def correct_wall():
    global pose, control, loop, flag
    loop = not(loop)
    pose = [100,150,pi/4]
    control = [100,0]
    loop = 0
    flag = 1
        
def robot_map(wall,t):
    p = []
    for i in range(len(wall)): 
        p.append([j*100/sum(wall[i]) for j in wall[i]])
    a= [[]]
    for i in range(len(p)):
        p[i] = [(1-p[i][k]/max(p[i])) for k in range(len(p[i]))]
        p[i] = list(reversed(p[i]))
        for j in range(len(p[i])):
            a[i].append([p[i][j]]*3)
        a.append([])
        
    
    for i in range(len(a)-1): # Do not plot the empty list in the last of 'a' due to the above operation 
        if i == 0:
            ax1 = fig.add_axes([0.25, 0.01, 0.025, 0.98]) # GUI rectangle creation
            ax1.set_axis_off()
            cmap1 = mpl.colors.ListedColormap(a[0])
            cmap2 = mpl.cm.Greys
            norm = mpl.colors.Normalize()
            cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap1,
                                               norm=norm,
                                               orientation='vertical')
            cb1.outline.set_visible(False)
            plt.gcf().canvas.draw()
            
        elif i == 1:
            ax1 = fig.add_axes([0.01, 0.01, 0.025, 0.98]) # GUI rectangle creation
            ax1.set_axis_off()
            cmap1 = mpl.colors.ListedColormap(a[1])
            cmap2 = mpl.cm.Greys
            norm = mpl.colors.Normalize()
            cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap1,
                                               norm=norm,
                                               orientation='vertical')
            cb1.outline.set_visible(False)
            plt.gcf().canvas.draw()
            
        elif i == 2:
            ax1 = fig.add_axes([0.01, 0.01, 0.98, 0.025]) # GUI rectangle creation
            ax1.set_axis_off()
            cmap1 = mpl.colors.ListedColormap(a[2])
            cmap2 = mpl.cm.Greys
            norm = mpl.colors.Normalize()
            cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap1,
                                               norm=norm,
                                               orientation='horizontal')
            cb1.outline.set_visible(False)
            plt.gcf().canvas.draw()
            
        elif i == 3:
            ax1 = fig.add_axes([0.5, 0.01, 0.025, 0.98]) # GUI rectangle creation
            ax1.set_axis_off()
            cmap1 = mpl.colors.ListedColormap(a[3])
            cmap2 = mpl.cm.Greys
            norm = mpl.colors.Normalize()
            cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap1,
                                               norm=norm,
                                               orientation='vertical')
            cb1.outline.set_visible(False)
            plt.gcf().canvas.draw()
            
        elif i == 4:
            ax1 = fig.add_axes([0.01, 0.965, 0.98, 0.025]) # GUI rectangle creation
            ax1.set_axis_off()
            cmap1 = mpl.colors.ListedColormap(a[4])
            cmap2 = mpl.cm.Greys
            norm = mpl.colors.Normalize()
            cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap1,
                                               norm=norm,
                                               orientation='horizontal')
            cb1.outline.set_visible(False)
            plt.gcf().canvas.draw()
            
        elif i == 5:
            ax1 = fig.add_axes([0.74, 0.01, 0.025, 0.98]) # GUI rectangle creation
            ax1.set_axis_off()
            cmap1 = mpl.colors.ListedColormap(a[5])
            cmap2 = mpl.cm.Greys
            norm = mpl.colors.Normalize()
            cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap1,
                                               norm=norm,
                                               orientation='vertical')
            cb1.outline.set_visible(False)
            plt.gcf().canvas.draw()
        
        elif i == 6:
            ax1 = fig.add_axes([0.967, 0.01, 0.025, 0.98]) # GUI rectangle creation
            ax1.set_axis_off()
            cmap1 = mpl.colors.ListedColormap(a[6])
            cmap2 = mpl.cm.Greys
            norm = mpl.colors.Normalize()
            cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap1,
                                               norm=norm,
                                               orientation='vertical')
            cb1.outline.set_visible(False)
            plt.gcf().canvas.draw()
        
if __name__ =="__main__":

    # Specifications of the world
    origin = (2,2)
    world_size = (498, 498)   # 750,750
    wall_width = 10
    radius = 10
    plotShift = 0
    flag = 0 # For wall correction
    wall_location =[[origin[0]+(world_size[0])/4,origin[1]+wall_width,origin[0]+(world_size[0])/4,origin[1]+wall_width+(world_size[1])*3/4],
                    [origin[0]+(world_size[0])/2,origin[1]+wall_width+(world_size[1])*1/4,origin[0]+(world_size[0])/2,origin[1]-wall_width+world_size[1]],
                    [origin[0]+(world_size[0])*3/4,origin[1]+wall_width,origin[0]+(world_size[0])*3/4,origin[1]+wall_width+(world_size[1])*3/4]]

    
    #Initialization of boundary and walls
    sri = boundaries(world_size,wall_width) 
    mw = walls(wall_width,wall_location)
    
    # Intialization of GUI
    root = Tk()
    root.title("Ball in a maze")
    frame1 = Frame(root)
    frame1.pack()
    w = Canvas(frame1,width=500,height=500,bg="white")
    w.pack(side=LEFT)
    
    # Robot map
    r = Canvas(frame1,width=500,height=500,bg="white")
    r.pack(side=RIGHT)
    fig = plt.figure(figsize=(6.15,6.15),facecolor='w',edgecolor='w')
    canvas = FigureCanvasTkAgg(fig, master=r)
    canvas.get_tk_widget().pack(side=RIGHT)
    
    
    # Creating world objects
    sri.draw(origin,w)
    mw.draw(wall_width,wall_location,w)
    parray = sri.boundary_grid(origin,w)
    warray = mw.wall_grid(wall_width,wall_location,w)
    
    # Creating Sphero robot
    s = Sphero(w)
    constraints = s.sphero_constraint(origin,wall_width,world_size,wall_location)
    
    minimum_correspondence_likelihood = 1e-3
    xstddev = 0.001
    ystddev = 0.001
    measurement_stddev = 0.001
    control_speed_factor = 0.01
    control_head_factor = 0.01
    number_of_particles = 1
    robot_width = 2
    sample_time = 0.01
    
    pose = [100,150,pi/4]
    control = [100,0]
    loop = 0
    
    initial_particles = [copy.copy(Particle(pose))
                         for _ in xrange(number_of_particles)]
    
    fs = FastSLAM(initial_particles,robot_width,minimum_correspondence_likelihood,measurement_stddev,xstddev,ystddev,
                 control_speed_factor,control_head_factor, sample_time)
    
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
    wc = Button(frame2,text="Wall Correction", width=15,command=correct_wall)
    wc.grid(row=0,column=4)
    
    # Draw GUI
    root.mainloop()


