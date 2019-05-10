# Describes a Sphero agent which can move through the world and collide with walls
import numpy as np

class Sphero:
  def __init__(self):
    
    self.x_left = 225
    self.y_top = 225
    self.x_right = 275
    self.y_bottom = 275
    
    self.center_x = self.x_right - 25
    self.center_y = self.y_bottom - 25

    self.speed_x = 13
    self.speed_y = 9

    # TODO: position & velocity propperty
    # Create a vector as a column
    # velocity = np.array([[self.speed_x],
    #                     [self.speed_y]])

    # d = {'x': self.speed_x, 'y': self.speed_x}

  def draw(self,canvas):
    return canvas.create_oval(self.x_left, self.y_top, self.x_right, self.y_bottom, fill="blue", tag='ball')

  def move(self):
    self.x_left += self.speed_x
    self.x_right += self.speed_x
    self.y_top += self.speed_y
    self.y_bottom += self.speed_y