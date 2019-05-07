import matplotlib as mpl


class robotmap(object):

    def __init(self,wall,t):
        self.wall=wall
        self.t=t
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