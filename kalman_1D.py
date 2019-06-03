import numpy as np
from CONSTANTS import STEP_SIZE

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

	def __init__(self, state_dim, observation_dim, delta_t, start_pos):
		self.state_dim = state_dim
		self.obs_dim   = observation_dim
		self.measurement_noise = 0.001
		# self.measurement_noise = 0
		self.process_noise = 1e-4
		# self.process_noise = 1
		
		'''custom matrices sphero'''
		self.A = np.matrix([[1, delta_t],		# 3. Transition/Dynamic matrix
							[0,		  1]])

		self.B = np.matrix([[0.5*delta_t**2],
							[       delta_t]])

		# self.B = np.matrix([[		0],
		# 					[delta_t]])

		self.H = np.matrix([[0, 0]])			# 4. Measurement matrix

		self.x = np.matrix([[start_pos],		# pos
							[0]]) 				# speed

		self.u = np.matrix([[0]]) 

		self.Q 		 	= np.matrix( np.eye(state_dim)*self.process_noise )			        			# 1. orig Process noise covariance
		self.R 			= np.matrix(np.eye(observation_dim)*self.measurement_noise)
		self.K		 	= np.matrix( np.zeros_like(self.H.T) )			            # 5. Kalman gain matrix
		self.P		 	= np.matrix( np.zeros_like(self.A) )			            # 6. State covariance, exact pos t=0 known

	def prediction_step(self, u):
		self.u = u

		# Make prediction
		self.x	 = self.A * self.x + self.B * self.u
		self.P	= self.A * self.P * self.A.T + self.Q

		return np.asarray(self.H*self.x)

	# def prediction_step_unfiltered(self):
	# 	self.

	def correction_step_vel(self, speed = 0):
		speed = np.matrix([speed])

		self.H = np.matrix([[0, 1]]) # measurement matrix for speed

		'''
		expected behaviour: position & speed correction are decoupled. 
		updating with a measurement from either should not change the prediction of the other
		behaviour: correction step with velocity also changes the position prediction
		'''
		# bug -----------------------------------------------------------------
		# Compute the optimal Kalman gain factor
		self.K = self.P * self.H.T * np.linalg.inv(self.H * self.P * self.H.T + self.R)

		self.K[0] = 0 						# brute bug fix
		# Correction based on observation
		self.x = self.x + self.K * (speed - self.H * self.x)
		self.P = self.P - self.K * self.H * self.P
		# bug -------------------------------------------------------------------

	def correction_step_pos(self, obs):
		self.H = np.matrix([[1, 0]])  # measurement matrix for position

		# Compute the optimal Kalman gain factor
		self.K = self.P * self.H.T * np.linalg.inv(self.H * self.P * self.H.T + self.R)

		# Correction based on observation
		self.x = self.x + self.K * (obs - self.H * self.x)
		self.P = self.P - self.K * self.H * self.P

	def predict(self):
		self.H = np.matrix([[1, 0]])
		return np.asarray(self.H*self.x)

"""testing kalman funtionality"""
if __name__ == "__main__":	
	# when you get a new observation 
	for i in range(0,30):
		A = np.matrix([ [5],
						[1] ])
		B = np.matrix([ [0],
						[5] ])
		test = B * A
		print(test)
