# combines all the modules to run a simulation of the SLAM problem in the maze
from tkinter import Tk, Canvas, mainloop, Frame
from sphero import Sphero
from collision import collision_check
import world as w

# Initialization of GUI
root = Tk()
frame1= Frame(root)
frame1.pack(fill='both')

# given environment
wall_canvas = Canvas(frame1,width=w.WIDTH,height=w.HEIGHT,bg="green")
wall_canvas.pack(side='left')

# map made from observations
map_canvas = Canvas(frame1,width=w.WIDTH,height=w.HEIGHT,bg="white")
map_canvas.pack(side='right')

sphero = Sphero()
sphero.draw(wall_canvas)

while True:
    sphero.move()

    collision_check(sphero)

    wall_canvas.move("ball", sphero.speed_x, sphero.speed_y)
    wall_canvas.after(30)
    wall_canvas.update()
mainloop()
