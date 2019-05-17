import numpy.random as rd
import numpy as np
from display import Display
from solver import Sphero, Wall
from constanten import *


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
        balls.append(Sphero(m, m, vx, vv))
    return balls


if __name__ == "__main__":


    """1D filter test"""

    spheros = [Sphero(m, r, startposition_ball1 , [1.,0.])]
    # walls = [Wall([300,0,310,300])]
    walls = []

    """run the simulation with given params"""
    Display(spheros, walls, step, size)
