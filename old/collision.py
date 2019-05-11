# describes the collision process
import world as w

# here we can plugin the SLAM algorithm
def collision_check(sphero):
    if sphero.x_right >= w.WIDTH:
        print ("collision at [{0}, {1}]".format(sphero.x_right, sphero.center_y))
        save_collision(sphero.x_right, sphero.center_y)
        sphero.speed_x = -sphero.speed_x
    if sphero.x_left <= 0:
        print ("collision at [{0}, {1}]".format(sphero.x_left, sphero.center_y))
        save_collision(sphero.x_right, sphero.center_y)
        sphero.speed_x = -sphero.speed_x
    if sphero.y_bottom >= w.HEIGHT:
        #TODO: log coordinates of the wall
        print ("collision at [{0}, {1}]".format(sphero.center_x, sphero.y_bottom))
        save_collision(sphero.center_x, sphero.y_bottom)
        sphero.speed_y = -sphero.speed_y
    if sphero.y_top <= 0:
        print ("collision at [{0}, {1}]".format(sphero.center_x, sphero.y_top))
        save_collision(sphero.center_x, sphero.y_top)
        sphero.speed_y = -sphero.speed_y

# TODO: function that saves a list of all collisions so they can be drawn later
def save_collision(x,y):
    global collision_list
    try: 
      collision_list
    except NameError: 
      collision_list = []
      
    collision_list.append([x,y])
    print (collision_list)