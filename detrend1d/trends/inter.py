
'''
Inter-cycle trends
'''

import numpy as np
from . _base import _Trend

__all__  = ['Linear', 'LinearFixedIntercept']





class Linear(_Trend):
	
	'''
	Model:   y(t) = a*t + b
	'''
	
	@staticmethod
	def _X(t):   # design matrix
		n      = t.size
		X      = np.zeros( (n, 2) )
		X[:,0] = t
		X[:,1] = 1
		return X

	def _init_beta(self):
		self.beta  = np.array([0, 0])  # slope, intercept
		self.fixed = np.array([False, False])

	# def apply(self, t, y):
	# 	a,b   = self.beta
	# 	dy  = (a * t) + b
	# 	return y + dy





class LinearFixedIntercept( Linear ):

	def __init__(self, intercept=0):
		self.intercept = float( intercept )
		super().__init__()
		

	def _init_beta(self):
		self.beta  = np.array([0, self.intercept])  # slope, intercept
		self.fixed = np.array([False, True])

	# @staticmethod
	# def _X(t):   # design matrix
	# 	n      = t.size
	# 	X      = np.zeros( (n, 1) )
	# 	X[:,0] = t
	# 	return X



