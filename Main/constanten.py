"""parameters to run the simulation with"""       
size = 500.

"sphero params for many spheros"
m = 20.
r = 10.
startposition_ball1 =[20.,250.]
startposition_ball2 =[200.,130.]
startposition_ball3 =[40.,120.]
# step = 0.09
# spheros = [ Sphero(m, r, startposition_ball1, [-10.,-10.]), 
#             Sphero(m, r, startposition_ball2, [10.,10.]), 
#             Sphero(m, r, startposition_ball3, [10.,15.])]
# walls = [Wall([100,0,110,300]), Wall([400,0,410,300]), Wall([250, int(size-300), 260, int(size)])]


"1d filtering"
step = 0.05
