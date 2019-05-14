import numpy.random as rd
import numpy as np
from display import *
from solver import *

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

"""parameters to run the simulation with"""       

if __name__ == "__main__":
    m = 20.
    r = 10.
    size = 500.
    step = 0.07
    startposition_ball1 =[140.,320.]
    startposition_ball2 =[200.,130.]
    startposition_ball3 =[40.,120.]

    

    spheros = [ solver.Sphero(m, r, startposition_ball1, [-10.,-10.]), 
                solver.Sphero(m, r, startposition_ball2, [10.,10.]), 
                solver.Sphero(m, r, startposition_ball3, [10.,15.])]

    walls = [Wall([100,0,110,300]), Wall([400,0,410,300]), Wall([250, int(size-300), 260, int(size)])]
    

    Display(spheros, walls, step, size)