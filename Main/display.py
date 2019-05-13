import tkinter as tk
import solver

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

class Display:
    """Define the window used to display a simulation"""
    
    def __init__(self, spheros, walls, step, size):
        """Initialize and launch the display"""
        self.spheros = spheros
        self.walls = walls
        self.step = step
        self.size = size

        self.color1 = "#721F1F" 
        self.color2 = "#5F7999" #color Sphero
        self.color3 = "#D9F3FF"
        self.color4 = "#D9F3FF" #color wall
        
        self.window = tk.Tk()
        frame1= tk.Frame(self.window)
        frame1.pack(fill='both')
        # environment_canvas
        self.environment_canvas = tk.Canvas(frame1, width=self.size, height=self.size, bg= self.color1)
        self.environment_canvas.pack(side='left')
        self.environment_canvas.focus_set()
        # mapping canvas
        self.mapping_canvas = tk.Canvas(frame1, width=self.size, height=self.size, bg= self.color2)
        self.mapping_canvas.pack(side='right')


        self.drawing = self.create()
        self.create_walls()
        self.started = False
    
        start_button = tk.Button(self.window, text="Start", command=self.start)
        stop_button = tk.Button(self.window, text="Pause", command=self.stop)
        start_button.pack()
        stop_button.pack()
    
        self.window.mainloop()
    
    def create(self):
        """Create a drawing item for each solver.Sphero object
            
        return a dictionary with solver.Sphero objects as keys and their circle drawings as items
        """
        # TODO: merge create & create walls
        return {
            sphero: self.environment_canvas.create_circle(sphero.position[0], sphero.position[1], sphero.radius, fill=self.color2) for sphero in self.spheros
        }

    def create_walls(self):
        return {
            wall: self.environment_canvas.create_rectangle(wall.position[0], wall.position[1], wall.position[2], wall.position[3], fill =self.color4) for wall in self.walls
        }

    def update(self):
        """Update the drawing items for a time step"""
        solver.solve_step(self.spheros, self.walls, self.step, self.size)
        for sphero in self.spheros:
            self.environment_canvas.coords_circle(self.drawing[sphero], sphero.position[0], sphero.position[1], sphero.radius)
            # draw collisions in mapping environment
            if len(sphero.collision_list_hor) > 0:
                collision = sphero.collision_list_hor.pop()
                self.mapping_canvas.create_rectangle(collision[0]-20, collision[1]-5, collision[0]+20, collision[1]+5, outline=self.color1, fill= rgb(100,100,100) )
                            # draw collisions in mapping environment     
            if len(sphero.collision_list_vert) > 0:
                collision = sphero.collision_list_vert.pop()
                collision_int= int(round(collision[0]))
                self.mapping_canvas.create_rectangle(collision[0]-5, collision[1]-20, collision[0]+5, collision[1]+20, outline=self.color1, fill= rgb(100,100,100) )
        self.environment_canvas.update()


    def start(self):
        """Start the animation"""
        if not self.started:
            self.started = True
            self.animate()

    def animate(self):
        """Animate the drawing items"""
        if self.started:
            self.update()
            self.window.after(0, self.animate)

    def stop(self):
        """Stop the animation"""
        self.started = False

# Test this module
if __name__ == "__main__":
    balls = [solver.Sphero(20., 20., [40.,40.], [5.,5.]), solver.Sphero(10., 10., [480.,480.], [-15.,-15.]), solver.Sphero(15., 15., [30.,470.], [10.,-10.])]
    size = 500.
    step = 0.01
    Display(balls, step, size)
