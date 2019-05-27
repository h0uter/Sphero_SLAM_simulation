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
		# self.measurement_noise = 1
		self.process_noise = 1e-4
		# self.process_noise = 1
		
		'''custom matrices sphero'''
		self.A = np.matrix([[1, delta_t],
							[0,		  1]])
		

		self.B = np.matrix([[0.5*delta_t**2],
							[       delta_t]])

		# self.H = np.matrix([[1, 0],
		# 					[0, 1] ])
		self.H = np.matrix([[0, 0]])

		self.x = np.matrix([[start_pos],	# pos
							[0]]) 			# speed

		self.u = np.matrix([[0]]) 

		# self.Q 		 = np.matrix( np.eye(state_dim)*1e-4 )			        # 1. orig Process noise covariance
		self.Q 		 	= np.matrix( np.eye(state_dim)*self.process_noise )			        			# 1. orig Process noise covariance
		# self.Q 		 = np.matrix( np.eye(state_dim)*0 )			                # 1. 0 Process noise covariance, acc sensor noise
		# 2. orig Observation noise/measurement noise covariance
		self.R 			= np.matrix(np.eye(observation_dim)*self.measurement_noise)
		# self.R		 = np.matrix( np.eye(observation_dim) )			        # 2. 0 Observation noise/measurement noise covariance, noise gps
		# self.A		 = np.matrix( np.eye(state_dim) )			                # 3. Transition/Dynamic matrix
		# self.H		 = np.matrix( np.zeros((observation_dim, state_dim)) )      # 4. Measurement matrix
		self.K		 	= np.matrix( np.zeros_like(self.H.T) )			            # 5. Kalman gain matrix
		self.P		 	= np.matrix( np.zeros_like(self.A) )			            # 6. State covariance, exact pos t=0 known
		# self.x		 = np.matrix( np.zeros((state_dim, 1)) )		            # 7. The actual state of the system
		print('====== P: ', self.P)

	def prediction_step(self, u):
		self.u = u
		# Make prediction
		self.x	= self.A * self.x + self.B * self.u
		print('+++++ P: ', self.P)
		print('+++++ Q: ', self.Q)
		self.P	= self.A * self.P * self.A.T + self.Q

		return np.asarray(self.H*self.x)

	# def correction_step_vel_pos(self, obs, position_fix_axis='x'):
	# 	if obs.ndim == 1:
	# 		obs = np.matrix(obs).T

	# 	self.R = np.matrix(np.eye(self.obs_dim)*self.measurement_noise)
	# 	self.H = np.matrix([[1, 0],
    #                   		[0, 1]])
		
	# 	# Compute the optimal Kalman gain factor
	# 	self.K = self.P * self.H.T * np.linalg.inv(self.H * self.P * self.H.T + self.R)
		
	# 	# Correction based on observation
	# 	self.x = self.x + self.K * ( obs - self.H * self.x )
	# 	self.P = self.P - self.K * self.H * self.P

	def correction_step_vel(self):
		speed = np.matrix([0])

		# self.R = np.matrix(np.eye(1)*self.measurement_noise)
		self.H = np.matrix([[0, 1]])

		print('P: ', self.P)
		print('H.T: ', self.H.T)
		print('R: ', self.R)
		print('state before: ', self.x)
		print('woop: ', np.linalg.inv(self.H * self.P * self.H.T + self.R))
		print('doop: ', self.P * self.H.T)
		# -----------------------------------------------------------------
		print('+++++++++++++++++++++++++++++++++++++++++++++++++++')
		print('K before: ', self.K)

		# Compute the optimal Kalman gain factor
		self.K = self.P * self.H.T * np.linalg.inv(self.H * self.P * self.H.T + self.R)

		self.K[0] = 0
		# Correction based on observation
		self.x = self.x + self.K * (speed - self.H * self.x)
		self.P = self.P - self.K * self.H * self.P
		print('+++++++++++++++++++++++++++++++++++++++++++++++++++')

		# --------------------------------
		print('state after: ', self.x)

	def correction_step_pos(self, obs):
		# self.R = np.matrix(np.eye(1)*self.measurement_noise)
		self.H = np.matrix([[1, 0]])

		print('P: ', self.P)
		print('H.T: ', self.H.T)
		print('R: ', self.R)
		print('x before: ', self.x)
		print('woop: ', np.linalg.inv(self.H * self.P * self.H.T + self.R))

		# Compute the optimal Kalman gain factor
		self.K = self.P * self.H.T * np.linalg.inv(self.H * self.P * self.H.T + self.R)
		print('K: ', self.K)

		# Correction based on observation
		self.x = self.x + self.K * (obs - self.H * self.x)
		self.P = self.P - self.K * self.H * self.P
		print('x after: ', self.x)

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
