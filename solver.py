from CONSTANTS import STEP_SIZE
import numpy as np
import random

# motion model
import scipy.integrate
from numpy import exp
# from kalman import Kalman
from kalman_1D import Kalman

class Sphero:
    """Define physics of elastic collision."""
    
    def __init__(self, mass, radius, position, velocity, acceleration):
        """Initialize a Sphero object
        
        mass the mass of sphero
        radius the radius of sphero
        position the position vector of sphero
        velocity the velocity vector of sphero
        acceleration vector of the sphero
        """
        self.mass = mass 
        self.radius = radius
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.acceleration = np.array(acceleration)    # constant acceleration

        self.vafter = np.copy(velocity) # temporary storage for velocity direction change if a collision would occur
        self.acc_after = np.copy(self.acceleration) # temporary storage for acceleration in case of collision

        self.collision_list_hor = []
        self.collision_list_vert = []
        # TODO: last collision information, along which axis?: collision with y axis happens along the x axis
        # 
        # self.last_collision_info = {}

        '''per Sphero kalman filter state_dim: pos, vel | obs_dim: pos, vel'''
        # self.kalman_instance = Kalman(6, 2, STEP_SIZE)
        self.kalman_instance_x = Kalman(2, 1, STEP_SIZE)

    def compute_step(self, step):
        """Compute position & velocity of next step: v[n+1] = v[n] + a*step"""
        """Compute position & velocity of next step: pos[n+1] =pos[n] + v*step"""

        """Euler method: integrate by multiplying with sufficiently small steps"""
        self.velocity += self.acceleration*step # Euler method for integration

        self.position += self.velocity*step     # orig: velocity, position

    def new_direction(self):
        """Store velocity & acceleration direction change of next step."""
        self.velocity = self.vafter 
        self.acceleration = self.acc_after

    # TODO: not used atm 
    def update_motion_model(self, step):
        """motion model: x_n+1 = x_n + ∫∫(virt acc sensor + gaussian noise) --> position [x, y]"""

        # mu, sigma = 0, 0.5 # mean and standard deviation
        # gauss_noise = np.random.normal(mu, sigma)
        # gauss_noise = np.array( [np.random.normal(mu, sigma), np.random.normal(mu, sigma)] )
        self.acc_sensor = self.acceleration # + gauss_noise

        '''kalman'''
        acceleration = np.matrix([
            [self.acceleration[0]],
            [self.acceleration[1]] ])
        
        # print ('self.acceleration: ', self.acceleration)
        # print ('acceleration: ', acceleration)

        # self.kalman_instance.prediction_step(acceleration)
        self.kalman_instance_x.prediction_step(self.acceleration[0])

    # TODO: position_fix_axis
    def collision_event(self, position_fix_axis):

        # someNewPoint = np.matrix([
		# 	[self.position[0]],
		# 	[self.position[1]]])
        # if position_fix_axis == 'x':
        #     someNewPoint = self.position[0]
        # if position_fix_axis == 'y':
        #     someNewPoint = self.position[1]

        z = np.matrix([ [self.position[0]], [0] ])
        # z = self.position[0]
        # self.kalman_instance.correction_step(someNewPoint, position_fix_axis)
        self.kalman_instance_x.correction_step(z)

    def compute_energy(self, ball_list):
        """Compute kinetic energy."""
        return self.mass / 2. * np.linalg.norm(self.velocity)**2

    # TODO: ACCEL fix
    def compute_s2s_collision(self, other_sphero, step):
        """Compute velocity after collision with another ball."""
        m1, m2 = self.mass, other_sphero.mass
        r1, r2 = self.radius, other_sphero.radius
        v1, v2 = self.velocity, other_sphero.velocity
        x1, x2 = self.position, other_sphero.position
        di = x2-x1
        norm = np.linalg.norm(di)
        if norm-r1-r2 < step*abs(np.dot(v1-v2, di))/norm:
            self.vafter = v1 - 2. * m2/(m1+m2) * np.dot(v1-v2, di) / (np.linalg.norm(di)**2.) * di

    def compute_wall_collision(self, wall_list, step, size):
        """
        Compute velocity after hitting an edge.

        step the computation step, 
        size the medium size"""
        # TODO: make this the collision pos instead of the sphero pos

        r, v, pos = self.radius, self.velocity, self.position
        """"make a projection of your next step on the axis -> check if you're gonna cross over this boundary the next step"""
        projx = step*abs(np.dot(v,np.array([1.,0.])))
        projy = step*abs(np.dot(v,np.array([0.,1.])))

        """OUTER WALL along x-axis collision"""
        if abs(pos[0])-r < projx or abs(size-pos[0])-r < projx:
            print("x collision")
            self.vafter *= 0
            self.acc_after[0] *= -1

            collision_coords = np.array(pos)
            self.collision_list_vert.append(collision_coords)
            # TODO: give x to collision_event
            self.collision_event('x')
            
        """OUTER WALL along y-axis collision"""
        if abs(pos[1])-r < projy or abs(size-pos[1])-r < projy:
            print("y collision")
            self.vafter *= 0
            self.acc_after[1] *= -1

            collision_coords = np.array(pos)
            self.collision_list_hor.append(collision_coords)

            self.collision_event('y')

        for wall in wall_list:
            """INNER WALL left or right collision"""
            if (abs(wall.position[0]-pos[0])-r < projx and pos[1]+r > wall.position[1] and pos[1]-r < wall.position[3]) or (abs(-wall.position[2]+pos[0])-r < projx and pos[1]+r > wall.position[1] and pos[1]-r < wall.position[3]):
                print("along x-axis collision")
                # self.vafter[0] *= -1.
                self.vafter *= 0
                self.acc_after[0] *= -1

                collision_coords = np.array(pos)
                self.collision_list_vert.append(collision_coords)

                self.collision_event('x')

            """INNER WALL bottom or top collision"""
            if abs(wall.position[3] - pos[1])-r < projy and pos[0]+r > wall.position[0] and pos[0]-r < wall.position[2] or \
            abs(wall.position[1] - pos[1]-r) < projy and pos[0]+r > wall.position[0] and pos[0]-r < wall.position[2]:
                print("along y-axis collision")
                # self.vafter[1] *= -1.
                self.vafter *= 0
                self.acc_after[1] *= -1.

                collision_coords = np.array(pos)
                self.collision_list_hor.append(collision_coords)

                self.collision_event('y')

    def logger(self, step_count):
        if step_count % 150 == 0:
            # self.predicted_position = self.kalman_instance.predict()
            self.predicted_position = [0, 0]
            self.predicted_position[0] = self.kalman_instance_x.predict()

            error = [
                self.position[0] - self.predicted_position[0],
                # self.position[1] - self.predicted_position[1],
            ]
            print ('''
            step:               {0}
                                  x             y
            predicted position: [{1} {2}]
            actual position:    {3}
            error:              {4}
            '''.format(
                step_count, 
                self.predicted_position[0], 
                self.predicted_position[1], 
                self.position,
                error))


class Wall:
    """Wall definition"""
    def __init__(self, position):
        """ Initialize a Wall object (rectangle)"""
        """ position = [x1, y1, x2, y2] """
        self.position = position

# TODO: merge compute_step & solve_step
def solve_step(sphero_list, wall_list, step, size, step_count):
    """Solve a step for every sphero."""

    """Detect edge-hitting and collision of every sphero""" 
    for sphero1 in sphero_list:
        sphero1.compute_wall_collision(wall_list, step, size)
        for sphero2 in sphero_list:
            if sphero1 is not sphero2:
                sphero1.compute_s2s_collision(sphero2,step)
                
    """Compute position of every sphero"""
    for sphero in sphero_list:
        sphero.new_direction()
        sphero.compute_step(step)
        sphero.update_motion_model(step_count) #motion model with kalman filtering

    '''log sphero info'''
    sphero_list[0].logger(step_count)
