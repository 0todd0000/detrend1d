
'''
Inter-cycle trends
'''

import numpy as np
from matplotlib import pyplot as plt
from . fit import Fit





class Linear(object):
	
	'''
	Model:   y(t) = a*t + b
	'''
	
	def __init__(self, slope=None, intercept=None):
		self._fit   = Fit(self._X) # fitted model parameters
		self.a     = None if (slope is None) else np.asarray(slope)
		self.b     = None if (intercept is None) else np.asarray(intercept)
		
	
	def __repr__(self):
		s  = f'{self.__class__.__name__}\n'
		s += f'    a        = {self.a}\n'
		s += f'    b        = {self.b}\n'
		s += f'    isfitted = {self.isfitted}\n'
		return s
	
	@staticmethod
	def _X(t):   # design matrix
		n      = t.size
		X      = np.zeros( (n, 2) )
		X[:,0] = t
		X[:,1] = 1
		return X

	@property
	def design_matrix(self):  # fits (used only during fitting)
		return self._fit.X if self.isfitted else None
	@property
	def isfitted(self):
		return self._fit.isfitted
	@property
	def yhat(self):
		return self._fit.yhat

	
	def apply(self, t, y):
		a,b   = self.a, self.b
		dy  = (a * t) + b
		return y + dy
		

	def detrend(self, t, y):
		self.fit(t, y)
		return y - self.yhat

	
	
	def fit(self, t, y):
		self._fit.fit(t, y)
		self.a = self._fit.beta[0]
		self.b = self._fit.beta[1]
	
	
	def plot(self, ax=None, t0=0, t1=10, n=51):
		ax    = plt.gca() if (ax is None) else ax
		t     = np.linspace(t0, t1, n)
		y     = self.apply(t, np.zeros(n))
		ax.plot(t, y)
		

	def plot_design(self, ax=None, **kwargs):
		self._fit.plot_design( ax, **kwargs )

	def plot_fit(self, ax=None, **kwargs):
		self._fit.plot( ax, **kwargs )



class LinearFixedIntercept( Linear ):

	def __init__(self, slope=None, intercept=None):
		self._fit  = Fit(self._X) # fitted model parameters
		self.a     = None if (slope is None) else np.asarray(slope)
		self.b     = 0 if (intercept is None) else np.asarray(intercept)
		self._fit.set_constant( self.b )
	# def __init__(self, slope=1, intercept=0):
	# 	super().__init__()
	# 	self.beta      = np.array([slope])
	# 	self.intercept = intercept
	# 	# self.beta  = np.array([intercept, slope])
	# 	# self._beta =


	@staticmethod
	def _X(t):   # design matrix
		n      = t.size
		X      = np.zeros( (n, 1) )
		X[:,0] = t
		return X


	def fit(self, t, y):
		self._fit.fit(t, y)
		self.a = self._fit.beta[0]



	# @property
	# def _X(self):   # design matrix (used only during fitting)
	# 	n      = self._n
	# 	X      = np.zeros( (n, 1) )
	# 	X[:,0] = self._t
	# 	return X
	#
	# @property
	# def _yhat(self):  # fits (used only during fitting)
	# 	return self.intercept + (self._X @ self.beta)
	#
	# @property
	# def slope(self):
	# 	return self.beta[0]
	#
	#
	# def fit(self, t, y):
	# 	self._n    = t.size
	# 	self._t    = t
	# 	# ahat       = np.linalg.pinv(self.X[i]) @ y[i]
	# 	b          = self.intercept
	# 	self.beta  = self._Xi @ (y - b)
	# 	# _ahat      = float( self._Xi @ (y - b) )
	# 	# self.beta  = np.array( [ _ahat , b ] )
	# 	self.isfit = True
	#


		
		

		
# class Compound(object):
# 	def __init__(self, inter=None, intra=None):
# 		self.trend0  = inter
# 		self.trend1  = intra
#
# 	def apply(self, t, y):
# 		y1 = self.trend0.apply(t, y)
# 		return self.trend1.apply(t, y1)
#
# 	def plot(self, ax=None, t0=0, t1=10, n=51):
# 		ax    = plt.gca() if (ax is None) else ax
# 		t     = np.linspace(t0, t1, n)
# 		y     = self.apply(t, np.zeros(n))
# 		ax.plot(t, y)