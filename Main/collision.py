import numpy.random as rd
import numpy as np
from display import *
from solver import *

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
    # balls = init_list(10)
    # size = 400.
    # step = 0.02
    # Display(balls, step, size)

    spheros = [solver.Sphero(20., 20., [40.,40.], [6.,5.])]
    size = 300.
    step = 0.01
    Display(spheros, step, size)