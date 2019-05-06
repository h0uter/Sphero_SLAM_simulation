# outputs a topdown view of the world 
# overlayed with the position of the Sphero and the map it has created of it's environment
from tkinter import Tk, Canvas, mainloop
from sphero import Sphero

WIDTH = 500
HEIGHT = 500

window = Tk()
canvas = Canvas(window, width=WIDTH, height=HEIGHT, background="green")
canvas.pack()

sphero = Sphero()
sphero.draw(canvas)

while True:
    sphero.x_left += sphero.speed_x
    sphero.x_right += sphero.speed_x
    sphero.y_top += sphero.speed_y
    sphero.y_bottom += sphero.speed_y

    if sphero.x_right >= WIDTH:
        sphero.speed_x = -sphero.speed_x
    if sphero.x_left <= 0:
        sphero.speed_x = -sphero.speed_x
    if sphero.y_bottom >= HEIGHT:
        sphero.speed_y = -sphero.speed_y
    if sphero.y_top <= 0:
        sphero.speed_y = -sphero.speed_y

    canvas.move('ball', sphero.speed_x, sphero.speed_y)
    canvas.after(30)
    canvas.update()
mainloop()