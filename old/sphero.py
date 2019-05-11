# Describes a Sphero agent which can move through the world and collide with walls
import numpy as np

class Sphero:
  def __init__(self, x=250, y=250, r=50):
    
    self.x_left = x-r
    self.y_top = y-r
    self.x_right = x+r
    self.y_bottom = y+r
    
    self.center_x = x
    self.center_y = y

    self.speed_x = 13
    self.speed_y = 9

  def draw(self, canvas):
    return canvas.create_oval(self.x_left, self.y_top, self.x_right, self.y_bottom, fill="blue", tag='ball')
    # return canvas.create_oval(x-r, y-r, x+r, y+r, fill="blue", tag='ball')

  def move(self):
    self.x_left += self.speed_x
    self.x_right += self.speed_x
    self.y_top += self.speed_y
    self.y_bottom += self.speed_y