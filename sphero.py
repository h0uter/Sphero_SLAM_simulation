# Describes a Sphero agent which can move through the world and collide with walls

class Sphero:
  def __init__(self):
    # self.name = "Bolt"
    self.x_left = 225
    self.y_top = 225
    self.x_right = 275
    self.y_bottom = 275

  def draw(self,canvas):
    return canvas.create_oval(self.x_left, self.y_top, self.x_right, self.y_bottom, fill="blue", tag='ball')