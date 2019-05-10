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
environment_canvas = Canvas(frame1,width=w.WIDTH,height=w.HEIGHT,bg="green")
environment_canvas.pack(side='left')

# map made from observations by agent
map_canvas = Canvas(frame1,width=w.WIDTH,height=w.HEIGHT,bg="white")
map_canvas.pack(side='right')

# initialize a sphero
sphero = Sphero()
sphero.draw(environment_canvas)

# place to store all collisions
collision_list = []

while True:
  sphero.move()
  collision_check(sphero)
  

  # TODO: beter om current frame te tekenen

  environment_canvas.move("ball", sphero.speed_x, sphero.speed_y)
  environment_canvas.after(30)
  environment_canvas.update()
mainloop()
