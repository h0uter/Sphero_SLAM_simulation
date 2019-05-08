from math import cos, pi, fabs, tan
global pose, control, constraints, loop, radius, wall_width, world_size, flag, lw



minimum_correspondence_likelihood = 1e-3
xstddev = 0.001
ystddev = 0.001
measurement_stddev = 0.001
control_speed_factor = 0.01
control_head_factor = 0.01
number_of_particles = 1
robot_width = 2
sample_time = 0.01

""" de verschillende waarden in pose worden onafhankelijk van elkaar gebruikt
In formules zie je dan    Xsp -> Pose[0],  Ysp -> Pose[1],  Angle -> Pose [2]
Hieruit kan je aannemen dat waarde:
0 -> X
1 -> Y
2 -> Angle
"""
pose = [100,150,pi/4]  
control = [100,0]
loop = 0

radius = 10
flag = 0