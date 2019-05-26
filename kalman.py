from CONSTANTS import STEP_SIZE
import numpy as np

class Kalman:
	"""
	USAGE:
	
	# e.g., tracking an (x,y) point over time
	k = Kalman(state_dim = 6, obs_dim = 2)
	
	# when you get a new observation — 
	someNewPoint = np.r_[1,2]
	k.update(someNewPoint)
	
	# and when you want to make a new prediction
	predicted_location = k.predict()
	
	
	NOTE: 
	Setting state_dim to 3*obs_dim automatically implements a simple
	acceleration-based model, i.e.
	x(t+1) = x(t) + v(t) + a(t)/2
	
	You're free to implement whichever model you like by setting state_dim
	to what you need, and then directly modifying the "A" matrix.
	The text that helped me most with understanding Kalman filters is here:
	http://www.njfunk.com/research/courses/652-probability-report.pdf
	"""

	def __init__(self, state_dim, observation_dim, delta_t):
		self.state_dim = state_dim
		self.obs_dim   = observation_dim
		
		'''custom matrices sphero'''
		self.A = np.matrix([[1, 0, delta_t, 	  0],
							[0, 1, 		 0, delta_t],
							[0, 0, 		 1, 	  0],
							[0, 0, 		 0, 	  1]])

		self.B = np.matrix([[0.5*delta_t**2,              0],
							[             0, 0.5*delta_t**2],
							[       delta_t,              0],
							[             0,        delta_t]])

		self.H = np.matrix([[1, 0, 0, 0],
							[0, 1, 0, 0]])

		self.x = np.matrix([[0],
							[0],
							[0],
							[0]]) 

		self.u = np.matrix([[0],
							[0]]) 

		# self.Q 		 = np.matrix( np.eye(state_dim)*1e-4 )			        # 1. orig Process noise covariance
		self.Q 		 = np.matrix( np.eye(4)*1e-4 )			        # 1. orig Process noise covariance
		# self.Q 		 = np.matrix( np.eye(state_dim)*0 )			                # 1. 0 Process noise covariance, acc sensor noise
		self.R		 = np.matrix( np.eye(observation_dim)*0.01 )			# 2. orig Observation noise/measurement noise covariance
		# self.R		 = np.matrix( np.eye(observation_dim) )			        # 2. 0 Observation noise/measurement noise covariance, noise gps
		# self.A		 = np.matrix( np.eye(state_dim) )			                # 3. Transition/Dynamic matrix
		# self.H		 = np.matrix( np.zeros((observation_dim, state_dim)) )      # 4. Measurement matrix
		self.K		 = np.matrix( np.zeros_like(self.H.T) )			            # 5. Kalman gain matrix
		self.P		 = np.matrix( np.zeros_like(self.A) )			            # 6. State covariance, exact pos t=0 known
		# self.x		 = np.matrix( np.zeros((state_dim, 1)) )		            # 7. The actual state of the system

	def prediction_step(self, u):
		self.u = u
		# Make prediction
		self.x	= self.A * self.x + self.B * self.u
		self.P	= self.A * self.P * self.A.T + self.Q

		return np.asarray(self.H*self.x)

	def correction_step(self, obs):
		if obs.ndim == 1:
			obs = np.matrix(obs).T
		
		# Compute the optimal Kalman gain factor
		self.K = self.P * self.H.T * np.linalg.inv(self.H * self.P * self.H.T + self.R)
		
		# Correction based on observation
		self.x = self.x + self.K * ( obs - self.H * self.x )
		self.P = self.P - self.K * self.H * self.P

	def predict(self):
		return np.asarray(self.H*self.x)

"""testing kalman funtionality"""
if __name__ == "__main__":
	# e.g., tracking an (x,y) point over time
	k = Kalman(6, 2, STEP_SIZE)
	# k = Kalman(6, 2)
	predicted_path = []
	mu, sigma = 0, 0.5 # mean and standard deviation
	print('B: ', k.B)
	print('Q: ', k.Q)
	
	# when you get a new observation 
	for i in range(0,30):
		print('x: ', k.x)
		gauss_noise = np.random.normal(mu, sigma)
		# someNewPoint = np.matrix([i, i*2])
		someNewPoint = np.matrix([
			[i],
			[i*2]])
		# print('someNewPoint: ', someNewPoint)
		print('A*x: ', k.A*k.x)
		print('B*u: ', k.B*k.u)
		predicted_location = k.prediction_step(someNewPoint)
		# print('predicted_location: ', predicted_location)