# describes the collision process
import world as w

# here we can plugin the SLAM algorithm
def collision_check(sphero):
    if sphero.x_right >= w.WIDTH:
        print ("collision right")
        sphero.speed_x = -sphero.speed_x
    if sphero.x_left <= 0:
        print ("collision left")
        sphero.speed_x = -sphero.speed_x
    if sphero.y_bottom >= w.HEIGHT:
        print ("collision botom")
        sphero.speed_y = -sphero.speed_y
    if sphero.y_top <= 0:
        print ("collision top")
        sphero.speed_y = -sphero.speed_y