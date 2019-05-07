# describes the collision process
import world as w

def collision_check(sphero):
    if sphero.x_right >= w.WIDTH:
        sphero.speed_x = -sphero.speed_x
    if sphero.x_left <= 0:
        sphero.speed_x = -sphero.speed_x
    if sphero.y_bottom >= w.HEIGHT:
        sphero.speed_y = -sphero.speed_y
    if sphero.y_top <= 0:
        sphero.speed_y = -sphero.speed_y