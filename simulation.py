import numpy.random as rd
import numpy as np
from display import Display
from solver import Sphero, Wall
from CONSTANTS import *

"""can generate a list of different sizes balls if needed"""
def init_list(N):
    balls = []
    r = 10.
    v = 10.
    x = 400./float(N+1)
    for i in range(N):
        m = r*(1.-0.05*i)
        vv = [-1.*v, 1.*v]
        vx = [float(i+1)*x, float(i+1)*x]
        balls.append(Sphero(m, m, vx, vv, [5., 5.]))
    return balls

if __name__ == "__main__":
    """parameters to run the simulation with"""       
    # step = 0.005

    '''Many spheros demo'''
    # spheros = [ Sphero(m, r, START_POS_BALL_0, [-10.,-10.], ACCELERATION), 
    #             Sphero(m, r, startposition_ball1, [10.,10.], ACCELERATION), 
    #             Sphero(m, r, startposition_ball2, [10.,15.], ACCELERATION)]
    # walls = [Wall([100,0,110,300]), Wall([400,0,410,300]), Wall([250, int(MAP_SIZE-300), 260, int(MAP_SIZE)])]

    '''tunnel test'''
    # walls = [Wall([0,100,int(MAP_SIZE),120]), Wall([0,380,int(MAP_SIZE),400])]
    # spheros = [Sphero(m, r, START_POS_BALL_0, [0., 0.], ACCELERATION)]

    d = 20 # wall diameter
    t = 0.5*d
    '''RESULTS'''
    spheros = [Sphero(m, r, START_POS_BALL_0, [0., 0.], ACCELERATION)]
    '''1. No walls'''
    # walls = []
    '''2. Vertical wals'''
    walls = [ Wall([100,0,110,350]), Wall([250, int(MAP_SIZE-350), 260, int(MAP_SIZE)]), Wall([400,0,410,350]) ]
    '''1. Maze'''
    # walls = [
    #     Wall([200, 0, 200+d, 200]),         # A
    #     Wall([100+t, 100, 200, 100+d]),     # B
    #     Wall([100, 200, 100+d, 400]),       # C
    #     Wall([100+t, 300, 400, 300+d]),     # D
    #     Wall([300, 200, 300+d, 300]),       # E
    #     Wall([300, 100, 400, 100+d]),       # F
    #     Wall([0, 400-d, 100, 400]),         # G
    #     Wall([400, 100+d, 400+d, 200+d]),     # H
    #     Wall([400+d, 200, 500, 200+d]),       # I
    #     Wall([400, 300+d, 400+d, 400]),       # J
    #     Wall([200+d, 400, 300, 400+d]),       # K
    #     Wall([200, 400, 200+d, 500]),       # L
    # ]

    """run the simulation with given params"""
    Display(spheros, walls, STEP_SIZE, MAP_SIZE)
