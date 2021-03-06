import tkinter as tk
import solver
import copy

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from CONSTANTS import START_POS_BALL_0, startposition_ball1, startposition_ball2, ACCELERATION

def _create_circle(self, x, y, r, **kwargs):
    """Create a circle
        
    x the abscissa of centre
    y the ordinate of centre
    r the radius of circle
    **kwargs optional arguments
    return the drawing of a circle
    """
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

def _coords_circle(self, target, x, y, r, **kwargs):
    """Define a circle
        
    target the circle object
    x the abscissa of centre
    y the ordinate of centre
    r the radius of circle
    **kwargs optional arguments
    return the circle drawing with updated coordinates
    """
    return self.coords(target, x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.coords_circle = _coords_circle

def rgb(r, g, b):
    return "#%s%s%s" % tuple([hex(c)[2:].rjust(2, "0") for c in (r, g, b)])

"to remember all positions"
current_pos0 = []
last_pos0 = START_POS_BALL_0
current_pos1 = []
last_pos1 = startposition_ball1
current_pos2 = []
last_pos2 = startposition_ball2

# current_poserror1= []
# last_poserror1= startposition_ball1

class Display:
    """Define the window used to display a simulation"""

    def __init__(self, spheros, walls, step, size):
        """Initialize and launch the display"""
        self.spheros = spheros
        self.walls = walls
        self.step = step
        self.size = size
        
        self.step_count = 0

        self.color1 = "#721F1F" 
        self.color2 = "#5F7999" #color Sphero
        self.color3 = "#D9F3FF"
        self.color4 = "#D9F3FF" #color wall
        
        """display window"""
        self.window = tk.Tk()
        frame1= tk.Frame(self.window)
        frame1.pack(fill='both')

        """environment_canvas"""
        self.environment_canvas = tk.Canvas(frame1, width=self.size, height=self.size, bg= self.color1)
        self.environment_canvas.pack(side='left')
        self.environment_canvas.focus_set()

        """mapping canvas"""
        self.mapping_canvas = tk.Canvas(frame1, width=self.size, height=self.size, bg= self.color2)
        self.mapping_canvas.pack(side='left')

        # """error plotting canvas """
        # # a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
        # errormap = tk.Canvas(frame1,width=size,height=size,bg="white")
        # errormap.pack(side='right')
        # fig = plt.figure(figsize=(6,6),facecolor='w')
        # title=plt.title ('Real/Error Movement Tracking')
        # xlabel=plt.xlabel('Positioning in X') 
        # ylabel=plt.ylabel('Positioning in Y') 
        # axis = plt.axis([0,size,0, size])
        # self.error_canvas = FigureCanvasTkAgg(fig, master=errormap)
        # self.error_canvas.get_tk_widget().pack(side='right')

        """draw the world"""
        self.drawing = self.create_actual_sphero_drawing()
        self.prediction_drawing = self.create_predicted_sphero_drawing()
        self.create_walls()
        self.started = False

        """buttons"""
        start_button = tk.Button(self.window, text="Start", command=self.start)
        stop_button = tk.Button(self.window, text="Pause", command=self.stop)
        # plot_button = tk.Button(self.window, text="Plot", command=solver.plot(self.spheros[0]))
        start_button.pack()
        stop_button.pack()
        # plot_button.pack()

        self.window.mainloop()

    def create_actual_sphero_drawing(self):
        """Create a drawing item for each solver.Sphero object 
        return a dictionary with solver.Sphero objects as keys and their circle drawings as items """
        # TODO: merge create & create walls
        return {
            sphero: self.environment_canvas.create_circle(sphero.position[0], sphero.position[1], sphero.radius, fill=self.color2) for sphero in self.spheros 
        }
        
    def create_predicted_sphero_drawing(self):
        return {
            sphero: self.environment_canvas.create_circle(sphero.position[0], sphero.position[1], sphero.radius, fill=self.color3) for sphero in self.spheros 
        }

    def create_walls(self):
        """Create a drawing item for each solver.Wall object 
        return a dictionary with solver.Wall objects as keys and their rectangle drawings as items """
        return {
            wall: self.environment_canvas.create_rectangle(wall.position[0], wall.position[1], wall.position[2], wall.position[3], fill =self.color4) for wall in self.walls
        }

    """
    def update_errormap(self):
        "Create Error figure V. Halithan"
        update_interval = 30

        global last_pos0, last_pos1, last_pos2   #, last_poserror1

        current_pos0=  self.spheros[0].position
        current_pos1=  self.spheros[1].position
        current_pos2=  self.spheros[2].position

        # current_poserror1=  self.spheros[0].speed_sensor_x_estimate

        if abs(current_pos0[0] - last_pos0[0]) > update_interval or abs(current_pos0[1] - last_pos0[1])   > update_interval:
            plt.plot([last_pos0[0],current_pos0[0]],[500-last_pos0[1],500-current_pos0[1]], 'r--')
            # plt.plot([last_poserror1, current_poserror1],[500-last_pos1[1],500-current_pos1[1]], 'r--')

            last_pos0 = copy.deepcopy (self.spheros[0].position)
            # last_poserror1= copy.deepcopy (self.speed_sensor_x_estimate)
            self.error_canvas.draw()

        # if abs(current_pos1[0] - last_pos1[0]) > update_interval or abs(current_pos1[1] - last_pos1[1])   > update_interval:
        #     plt.plot([last_pos1[0],current_pos1[0]],[500-last_pos1[1],500-current_pos1[1]], 'g:')

        #     last_pos1 = copy.deepcopy (self.spheros[1].position)
        #     self.error_canvas.draw()

        # if abs(current_pos2[0] - last_pos2[0]) > update_interval or abs(current_pos2[1] - last_pos2[1])   > update_interval:
        #     plt.plot([last_pos2[0],current_pos2[0]],[500-last_pos2[1],500-current_pos2[1]], 'b-.')
        #     last_pos2 = copy.deepcopy (self.spheros[2].position)
        
            self.error_canvas.draw()
        
        "2nd ball tracking"
        # remmember2=  self.spheros[1].position
        # plt.plot([remmember_last2[0],remmember2[0]],[500-remmember_last2[1],500-remmember2[1]], color = 'red')
        # remmember_last2 = copy.deepcopy (self.spheros[1].position)   
        """

    def update(self):
        """Update the drawing items for a time step"""
        solver.solve_step(self.spheros, self.walls, self.step, self.size, self.step_count)
        
        for sphero in self.spheros:
            self.environment_canvas.coords_circle(self.drawing[sphero], sphero.position[0], sphero.position[1], sphero.radius)
            
            self.environment_canvas.coords_circle(self.prediction_drawing[sphero], sphero.predicted_position[0], sphero.predicted_position[1], sphero.radius)
            
            # draw collisions in mapping environment
            if len(sphero.collision_list_hor) > 0:
                collision = sphero.collision_list_hor.pop()
                self.mapping_canvas.create_rectangle(collision[0]-20, collision[1]-5, collision[0]+20, collision[1]+5, outline=self.color1, fill= rgb(100,100,100) )
            # draw collisions in mapping environment     
            if len(sphero.collision_list_vert) > 0:
                collision = sphero.collision_list_vert.pop()
                self.mapping_canvas.create_rectangle(collision[0]-5, collision[1]-20, collision[0]+5, collision[1]+20, outline=self.color1, fill= rgb(100,100,100) )
        self.environment_canvas.update()

        '''count simulation steps'''
        self.step_count += 1

    def start(self):
        """Start the animation"""
        if not self.started:
            self.started = True
            self.animate()

    def animate(self):
        """Animate the drawing items"""
        if self.started:
            # self.update_errormap()     # To Stop the ErrorMapping, change this to a text
            self.update() 
            self.window.after(0, self.animate)

    def stop(self):
        """Stop the animation"""
        self.started = False
        
if __name__ == "__main__":
    spheros = [solver.Sphero(20., 15., [300., 400.], [-8., -8.], ACCELERATION), solver.Sphero(20., 15., [
        40., 40.], [6., 5.], ACCELERATION), solver.Sphero(20., 15., [40., 120.], [10., 15.], ACCELERATION)]
    walls = [solver.Wall([100,0,110,300]), solver.Wall([400,0,410,300]), solver.Wall([250, int(size-300), 260, int(size)])]
    size = 500.
    step = 0.01
    Display(spheros, walls, step, size)
