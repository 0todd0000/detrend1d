
'''
Trend definitions
'''

import numpy as np
from . _base import _Trend

__all__  = ['Exponential', 'Linear', 'Polynomial2', 'Polynomial3']



class Exponential(_Trend):
	'''
	Model:   y(t) = a + b*t + c*exp(t)
	'''
	@staticmethod
	def _X(t):   # design matrix
		n      = t.size
		X      = np.zeros( (n, 3) )
		X[:,0] = 1
		X[:,1] = t
		X[:,2] = np.exp(t)
		return X

	def _init_beta(self):
		self.beta        = np.array([0, 0, 0])
		self.beta_labels = 'Intercept', 'Slope', 'Exponential'
		self.fixed       = np.array([False, False, False])


class Linear(_Trend):
	'''
	Model:   y(t) = a + b*t
	'''
	@staticmethod
	def _X(t):   # design matrix
		n      = t.size
		X      = np.zeros( (n, 2) )
		X[:,0] = 1
		X[:,1] = t
		return X

	def _init_beta(self):
		self.beta        = np.array([0, 0])
		self.beta_labels = 'Intercept', 'Slope'
		self.fixed       = np.array([False, False])


class Polynomial2(_Trend):
	'''
	Model:   y(t) = a + b*t * c*t**2
	'''
	@staticmethod
	def _X(t):   # design matrix
		n      = t.size
		X      = np.zeros( (n, 3) )
		X[:,0] = 1
		X[:,1] = t
		X[:,2] = t**2
		return X

	def _init_beta(self):
		self.beta        = np.array([0, 0, 0])
		self.beta_labels = 'Intercept', 'x', 'x2'
		self.fixed       = np.array([False, False, False])


class Polynomial3(_Trend):
	'''
	Model:   y(t) = a + b*t + c*t**2 + d*t**3
	'''
	@staticmethod
	def _X(t):   # design matrix
		n      = t.size
		X      = np.zeros( (n, 4) )
		X[:,0] = 1
		X[:,1] = t
		X[:,2] = t**2
		X[:,3] = t**3
		return X

	def _init_beta(self):
		self.beta        = np.array([0, 0, 0, 0])
		self.beta_labels = 'Intercept', 'x', 'x2', 'x3'
		self.fixed       = np.array([False, False, False,False])



