import numpy as np

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
        self.collision_list = []

    def compute_step(self, step):
        """Compute position of next step."""
        self.position += step * self.velocity
        
    def new_velocity(self):
        """Store velocity of next step."""
        self.velocity = self.vafter
        
    def computeEnergy(self, ball_list):
        """Compute kinetic energy."""
        return self.mass / 2. * np.linalg.norm(self.velocity)**2

    # TODO: make sphero's re-accelerate to their maximum velocity after collision
    def compute_coll(self, ball, step):
        """Compute velocity after collision with another ball."""
        m1, m2 = self.mass, ball.mass
        r1, r2 = self.radius, ball.radius
        v1, v2 = self.velocity, ball.velocity
        x1, x2 = self.position, ball.position
        di = x2-x1
        norm = np.linalg.norm(di)
        if norm-r1-r2 < step*abs(np.dot(v1-v2, di))/norm:
            self.vafter = v1 - 2. * m2/(m1+m2) * np.dot(v1-v2, di) / (np.linalg.norm(di)**2.) * di

    def compute_refl(self, step, size):
        """Compute velocity after hitting an edge.

        step the computation step
        size the medium size
        """
        r, v, pos = self.radius, self.velocity, self.position
        projx = step*abs(np.dot(v,np.array([1.,0.])))
        projy = step*abs(np.dot(v,np.array([0.,1.])))

        # TODO: generallize this for any wall not just edges
        # x collision
        if abs(pos[0])-r < projx or abs(size-pos[0])-r < projx:
            self.vafter[0] *= -1
            # TODO: make this the collision pos instead of the sphero pos
            collision_coords = np.array(pos)
            self.collision_list.append(collision_coords)
            print (self.collision_list[-1])
            
        # y collision
        if abs(pos[1])-r < projy or abs(size-pos[1])-r < projy:
            self.vafter[1] *= -1.
            collision_coords = np.array(pos)
            self.collision_list.append(collision_coords)
            print (self.collision_list[-1])


def solve_step(sphero_list, step, size):
    """Solve a step for every sphero."""
    
    # Detect edge-hitting and collision of every ball
    for sphero1 in sphero_list:
        sphero1.compute_refl(step,size)
        for sphero2 in sphero_list:
            if sphero1 is not sphero2:
                sphero1.compute_coll(sphero2,step)
                
    # Compute position of every ball  
    for sphero in sphero_list:
        sphero.new_velocity()
        sphero.compute_step(step)

        
