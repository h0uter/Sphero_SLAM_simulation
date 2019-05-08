# outputs a topdown view of the world
# overlayed with the position of the Sphero and the map it has created of it's environment
from tkinter import Tk, Canvas, mainloop
from sphero import Sphero
from collision import collision_check
import world as w

# TODO: view is not yet implemented 

def create_view():
  window = Tk()
  canvas = Canvas(window, width=w.WIDTH, height=w.HEIGHT, background="green")
  canvas.pack()
  return window, canvas

def update_view(canvas):
  canvas.move("ball", sphero.speed_x, sphero.speed_y)
  canvas.after(30)
  canvas.update()  

# window = Tk()
# canvas = Canvas(window, width=w.WIDTH, height=w.HEIGHT, background="green")
# canvas.pack()
