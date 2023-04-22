
'''
Fit class defintion
'''

import numpy as np
from matplotlib import pyplot as plt



class Fit(object):
	def __init__(self, trend):
		self._trend   = trend
		self.X        = None
		self.beta     = None
		self.t        = None
		self.y        = None
		self.yhat     = None

	# @property
	# def yhat(self):
	# 	return self.X @ self.beta # + self.constant
	
	def _fit(self, y):
		if self._trend.hasfixed:
			i0,i1 = self._trend.free, self._trend.fixed
			X0    = self.X[ : , i0 ]        # free-to-vary columns
			X1    = self.X[ : , i1 ]        # fixed columns
			b1    = self._trend.beta[ i1 ]  # fixed betas
			y1    = X1 @ b1                 # constants
			b0    = np.linalg.pinv(X0) @ (y-y1)  # free-to-vary betas
			beta  = np.zeros( self.X.shape[1] )  # all parameters
			beta[i0]  = b0
			beta[i1]  = b1
		else:
			beta  = np.linalg.pinv(self.X) @ y
		return beta

	
	def fit(self, t, y):
		self.t    = t
		self.y    = y
		self.X    = self._trend.get_design_matrix( t )
		self.beta = self._fit(y)
		self.yhat = self.X @ self.beta
		self._trend.set_beta( self.beta )
	
	def get_detrended(self):
		return self.y - self.yhat
	
	def plot(self, ax=None, **kwargs):
		ax    = plt.gca() if (ax is None) else ax
		ax.plot(self.t, self.yhat, **kwargs)

	def plot_design(self, ax=None, **kwargs):
		ax    = plt.gca() if (ax is None) else ax
		ax.pcolor(self.X, **kwargs)

	# def set_constant(self, x):
	# 	self.constant  = x
	#
	#
