
'''
Fit class defintion
'''

import numpy as np
from matplotlib import pyplot as plt



class Fit(object):
	def __init__(self, fnX):
		self.X        = None
		self.beta     = None
		self.constant = 0
		self.fnX      = fnX   # function that generates design matrix
		self.isfitted = False
		self.t        = None
		self.y        = None

	@property
	def Xi(self):  # design matrix pseudo-inverse
		return np.linalg.pinv(self.X)
	@property
	def isempty(self):
		return self.beta is None
		
	@property
	def yhat(self):
		return self.X @ self.beta + self.constant
	
	def fit(self, t, y):
		self.X        = self.fnX( t )
		self.beta     = self.Xi @ (y - self.constant)
		self.t        = t
		self.y        = y
		self.isfitted = True
		
	def plot(self, ax=None, **kwargs):
		if self.isfitted:
			ax    = plt.gca() if (ax is None) else ax
			ax.plot(self.t, self.yhat, **kwargs)
		else:
			print('Trend not yet fitted.')
			
	def plot_design(self, ax=None, **kwargs):
		if self.isfitted:
			ax    = plt.gca() if (ax is None) else ax
			ax.pcolor(self.X, **kwargs)
		else:
			print('Trend not yet fitted.')
			
	def set_constant(self, x):
		self.constant  = x