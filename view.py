# outputs a topdown view of the world 
# overlayed with the position of the Sphero and the map it has created of it's environment
from tkinter import *
from sphero import Sphero

WIDTH = 500
HEIGHT = 500

window = Tk()
canvas = Canvas(window, width=WIDTH, height=HEIGHT, background="green")
canvas.pack()

sphero = Sphero()
sphero.draw(canvas)

speed_x = 4
speed_y = 6

while True:
    sphero.x_left += speed_x
    sphero.x_right += speed_x
    sphero.y_top += speed_y
    sphero.y_bottom += speed_y

    if sphero.x_right >= WIDTH:
        speed_x = -speed_x
    if sphero.x_left <= 0:
        speed_x = -speed_x
    if sphero.y_bottom >= HEIGHT:
        speed_y = -speed_y
    if sphero.y_top <= 0:
        speed_y = -speed_y

    canvas.move('ball', speed_x, speed_y)
    canvas.after(30)
    canvas.update()
mainloop()