import numpy.random as rd
import numpy as np
from display import *
from solver import *

# can generate a list of different sizes balls if needed
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
    size = 500.
    step = 0.01
    spheros = [solver.Sphero(20., 15., [300.,400.], [-8.,-8.]), solver.Sphero(20., 15., [40.,40.], [6.,5.]), solver.Sphero(20., 15., [40.,120.], [10.,15.])]
    walls = [Wall([100,0,110,300]), Wall([400,0,410,300]), Wall([250, int(size-300), 260, int(size)])]

    Display(spheros, walls, step, size)