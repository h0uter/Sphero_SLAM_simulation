# outputs a topdown view of the world 
# overlayed with the position of the Sphero and the map it has created of it's environment
from tkinter import *

WIDTH = 500
HEIGHT = 500

window = Tk()
canvas = Canvas(window, width=WIDTH, height=HEIGHT, background="green")
canvas.pack()

ball_x_left = 225
ball_y_top = 225
ball_x_right = 275
ball_y_bottom = 275
ball = canvas.create_oval(ball_x_left, ball_y_top, ball_x_right, ball_y_bottom, fill="blue", tag='ball')

speed_x = 4
speed_y = 6

while True:
    ball_x_left += speed_x
    ball_x_right += speed_x
    ball_y_top += speed_y
    ball_y_bottom += speed_y

    if ball_x_right >= WIDTH:
        speed_x = -speed_x
    if ball_x_left <= 0:
        speed_x = -speed_x
    if ball_y_bottom >= HEIGHT:
        speed_y = -speed_y
    if ball_y_top <= 0:
        speed_y = -speed_y

    canvas.move('ball', speed_x, speed_y)
    canvas.after(30)
    canvas.update()
mainloop()