import numpy as np
import random

class Sphero:
    """Define physics of elastic collision."""
    
    def __init__(self, mass, radius, position, velocity):
        """Initialize a Sphero object
        
        mass the mass of sphero
        radius the radius of sphero
        position the position vector of sphero
        velocity the velocity vector of sphero
        """
        self.mass = mass
        self.radius = radius
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.vafter = np.copy(velocity) # temporary storage for velocity of next step
        self.collision_list_hor = []
        self.collision_list_vert = []
 

        """motion model = [x,y] : 'gps' position + accumulation of translation errors occuring at each collision"""
        # TODO: use motion_model to draw map
        self.motion_model = self.position

    def compute_step(self, step):
        """Compute position of next step."""
        self.position += step * self.velocity
        
    def new_velocity(self):
        """Store velocity of next step."""
        self.velocity = self.vafter
        
    def computeEnergy(self, ball_list):
        """Compute kinetic energy."""
        return self.mass / 2. * np.linalg.norm(self.velocity)**2

    # TODO: make sphero's re or de-accelerate to their maximum velocity after collision
    def compute_collision(self, other_sphero, step):
        """Compute velocity after collision with another ball."""
        m1, m2 = self.mass, other_sphero.mass
        r1, r2 = self.radius, other_sphero.radius
        v1, v2 = self.velocity, other_sphero.velocity
        x1, x2 = self.position, other_sphero.position
        di = x2-x1
        norm = np.linalg.norm(di)
        if norm-r1-r2 < step*abs(np.dot(v1-v2, di))/norm:
            self.vafter = v1 - 2. * m2/(m1+m2) * np.dot(v1-v2, di) / (np.linalg.norm(di)**2.) * di

    # def collision_error(self, motion_model):
    #     """adds a random translation error to the motion model on each collision"""
    #     # TODO: requirements: 
    #     # error 5 in x direction only
    #     # error should be very distinct
    #     max_err = 10
    #     motion_model = [motion_model[0]+random.randint(-max_err, max_err), motion_model[1]+random.randint(-max_err, max_err)]

    def compute_refl(self, wall_list, step, size):
        """Compute velocity after hitting an edge.

        step the computation step
        size the medium size
        """
        r, v, pos = self.radius, self.velocity, self.position
        """"make a projection of your next step on the axis -> check if you're gonna cross over this boundary the next step"""
        projx = step*abs(np.dot(v,np.array([1.,0.])))
        projy = step*abs(np.dot(v,np.array([0.,1.])))

        # TODO: implement collision error
        """OUTER WALL x collision"""
        if abs(pos[0])-r < projx or abs(size-pos[0])-r < projx:
            self.vafter[0] *= -1
            # TODO: make this the collision pos instead of the sphero pos
            collision_coords = np.array(pos)
            self.collision_list_vert.append(collision_coords)
            # print (self.collision_list_vert[-1])
            # print (projx)
            print("x collision")
            
        """OUTER WALL y collision"""
        if abs(pos[1])-r < projy or abs(size-pos[1])-r < projy:
            self.vafter[1] *= -1.
            collision_coords = np.array(pos)
            # print(projy)
            self.collision_list_hor.append(collision_coords)
            # print (self.collision_list_hor[-1])
            print("y collision")

        for wall in wall_list:
            """INNER WALL left or right collision"""
            if (abs(wall.position[0]-pos[0])-r < projx and pos[1]+r > wall.position[1] and pos[1]-r < wall.position[3]) or (abs(-wall.position[2]+pos[0])-r < projx and pos[1]+r > wall.position[1] and pos[1]-r < wall.position[3]):
                self.vafter[0] *= -1
                # TODO: make this the collision pos instead of the sphero pos
                collision_coords = np.array(pos)
                self.collision_list_vert.append(collision_coords)
                # print("projx: {}".format(projx))
                # print (self.collision_list_vert[-1])
                print("x collision")

            """INNER WALL bottom or top collision"""
            # abs(bottom_y_wall - y_sphero) - radius < projection on x axis iff (x_sphero+r > left_wall) & (x_sphero +r < right_wall)
            # if abs(wall.position[3] - pos[1])-r < projy and pos[0]+r > wall.position[0] and pos[0]-r < wall.position[2]:
            if abs(wall.position[3] - pos[1])-r < projy and pos[0]+r > wall.position[0] and pos[0]-r < wall.position[2] or \
                abs(wall.position[1] - pos[1]-r) < projy and pos[0]+r > wall.position[0] and pos[0]-r < wall.position[2]:
                print("y collision")
                print("vel: {0}, vel_after: {1}".format(self.velocity, self.vafter))
                self.vafter[1] *= -1.
                collision_coords = np.array(pos)
                self.collision_list_hor.append(collision_coords)
                # print("projy: {}".format(projy))
                # print (self.collision_list_hor[-1])
                print("vel: {0}, vel_after: {1}".format(self.velocity, self.vafter))


class Wall:
    """Wall definition"""
    def __init__(self, position):
        """Initialize a Wall object (rectangle)
        
        position = [x1, y1, x2, y2]
        """
        self.position = position        


def solve_step(sphero_list, wall_list, step, size):
    """Solve a step for every sphero."""

    """Detect edge-hitting and collision of every sphero""" 
    for sphero1 in sphero_list:
        sphero1.compute_refl(wall_list, step, size)
        # sphero1.compute_inner_wall_refl(step, wall_list)
        for sphero2 in sphero_list:
            if sphero1 is not sphero2:
                sphero1.compute_collision(sphero2,step)
                
    """Compute position of every sphero"""
    for sphero in sphero_list:
        sphero.new_velocity()
        sphero.compute_step(step)