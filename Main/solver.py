import numpy as np
import random

# motion model
import scipy.integrate
from numpy import exp
from kalman import Kalman

class Sphero:
    """Define physics of elastic collision."""
    
    def __init__(self, mass, radius, position, velocity):
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
        # TODO: move this to sim intialisation
        self.acceleration = np.array([5, 5])    # constant acceleration

        self.vafter = np.copy(velocity) # temporary storage for velocity direction change if a collision would occur
        self.acc_after = np.copy(self.acceleration) # temporary storage for acceleration in case of collision

        self.collision_list_hor = []
        self.collision_list_vert = []

        '''kalman'''
        self.kalman_instance = Kalman(3, 1)

        # TODO: complete
        """motion model = [acc_x, acc_y] : virt sensor + gaussian noise --> position [x, y]"""
        self.speed_sensor_x_estimate = np.array(position[0]) # estimate based on speed
        # self.acc_sensor_x_estimate = np.array(position[0]) # estimate based on acceleration

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
        """Compute position of next step based on velocity + noise"""
        mu, sigma = 0, 0.5 # mean and standard deviation
        gauss_noise = np.random.normal(mu, sigma)
        # gauss_noise = np.array( [np.random.normal(mu, sigma), np.random.normal(mu, sigma)] )
        """velocity sensor x pos motion model"""
        # self.speed_sensor_x_estimate += step * (self.velocity[0]+gauss_noise) #once integrated error
        self.speed_sensor_x_estimate += step * (self.velocity[0]) +gauss_noise  #not integrated error
        # self.speed_sensor_x_estimate += step * (self.velocity[0])             #no error
        """acceleration sensor based x pos motion model"""
        # self.speed_sensor_x_estimate += step * (self.velocity[0]+gauss_noise) #once integrated error
        self.speed_sensor_x_estimate += step * (self.velocity[0]) +gauss_noise  #not integrated error
        # self.speed_sensor_x_estimate += step * (self.velocity[0])             #no error

        """TODO: acc sensor based x pos motion model"""
        # self.acc_sensor_x_estimate += step * self.velocity[0] + 0.5*self.acceleration**2

        '''kalman'''
        k = Kalman(3, 1)
        someNewPoint = np.r_[self.speed_sensor_x_estimate]
        # someNewPoint = self.speed_sensor_x_estimate
        # print("someNewPoint: {0}".format(someNewPoint))
        k.update(someNewPoint)
        # and when you want to make a new prediction
        self.predicted_position = k.predict()
        error = self.predicted_position - self.position[0]

        print("""
        speed sensor est pos:  {0}
        actual pos:            {1}
        predictedlocation :    {2}
        error:                 {3}
        """.format(self.speed_sensor_x_estimate, self.position[0], self.predicted_position, error))

    def compute_energy(self, ball_list):
        """Compute kinetic energy."""
        return self.mass / 2. * np.linalg.norm(self.velocity)**2

    def collision_event(self):
        someNewPoint = np.r_[self.position[0]]
        self.kalman_instance.update(someNewPoint)

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

        """OUTER WALL x collision"""
        if abs(pos[0])-r < projx or abs(size-pos[0])-r < projx:
            print("x collision")
            self.vafter *= 0
            self.acc_after[0] *= -1

            collision_coords = np.array(pos)
            self.collision_list_vert.append(collision_coords)

            self.collision_event()
            
        """OUTER WALL y collision"""
        if abs(pos[1])-r < projy or abs(size-pos[1])-r < projy:
            print("y collision")
            self.vafter *= 0
            self.acc_after[1] *= -1

            collision_coords = np.array(pos)
            self.collision_list_hor.append(collision_coords)

            self.collision_event()

        for wall in wall_list:
            """INNER WALL left or right collision"""
            if (abs(wall.position[0]-pos[0])-r < projx and pos[1]+r > wall.position[1] and pos[1]-r < wall.position[3]) or (abs(-wall.position[2]+pos[0])-r < projx and pos[1]+r > wall.position[1] and pos[1]-r < wall.position[3]):
                print("x collision")
                # self.vafter[0] *= -1.
                self.vafter *= 0
                self.acc_after[0] *= -1

                collision_coords = np.array(pos)
                self.collision_list_vert.append(collision_coords)

                self.collision_event()

            """INNER WALL bottom or top collision"""
            if abs(wall.position[3] - pos[1])-r < projy and pos[0]+r > wall.position[0] and pos[0]-r < wall.position[2] or \
            abs(wall.position[1] - pos[1]-r) < projy and pos[0]+r > wall.position[0] and pos[0]-r < wall.position[2]:
                print("y collision")
                # self.vafter[1] *= -1.
                self.vafter *= 0
                self.acc_after[1] *= -1.

                collision_coords = np.array(pos)
                self.collision_list_hor.append(collision_coords)

                self.collision_event()

    def logger(self, step_count):
        if step_count % 50 == 0:

            self.predicted_position = self.kalman_instance.predict()
            print ('''
            step:               {0}
            predicted position: {1}
            actual position:    {2}
            '''.format(step_count, self.predicted_position, self.position))


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
        # sphero.update_motion_model(step) #motion model with kalman filtering

    '''log sphero info'''
    sphero_list[0].logger(step_count)

