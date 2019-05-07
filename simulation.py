# combines all the modules to run a simulation of the SLAM problem in the maze
from tkinter import Tk, Canvas, mainloop
from sphero import Sphero
from collision import collision_check
import world as w

window = Tk()
canvas = Canvas(window, width=w.WIDTH, height=w.HEIGHT, background="green")
canvas.pack()

sphero = Sphero()
sphero.draw(canvas)

while True:
    sphero.move()

    collision_check(sphero)

    canvas.move("ball", sphero.speed_x, sphero.speed_y)
    canvas.after(30)
    canvas.update()
mainloop()
