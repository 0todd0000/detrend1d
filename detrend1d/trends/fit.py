
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
	# @property
	# def isempty(self):
	# 	return self.beta is None
		
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
		
		


class CyclicalFit(object):
	def __init__(self, fnX):
		self.XX       = None  # design matrices at each time point
		self.X        = None  # mean design matrix (over time)
		self.beta     = None
		self.constant = 0
		self.fnX      = fnX   # function that generates design matrix
		self.isfitted = False
		self.t        = None
		self.y        = None


	@property
	def _yhat(self):
		k = self.constant
		return [X @ b + k   for X,b in zip(self.XX, self.beta.T)]
	@property
	def yhat(self):
		return np.hstack( self._yhat )
	@property
	def yhat_stacked(self):
		return np.array( self._yhat )

	
	def fit(self, t, y, c):
		ts            = np.vstack(  [ t[c==u]  for u in np.unique(c) ]  )
		ys            = np.vstack(  [ y[c==u]  for u in np.unique(c) ]  )
		XX            = np.array(   [ self.fnX(tt) for tt in ts.T ]  )
		k             = self.constant
		self.beta     = np.array(  [np.linalg.pinv( X ) @ (yy - k)  for X,yy in zip(XX, ys.T)]  ).T
		# self.beta     = np.array(  [np.linalg.pinv( make_X(tt) ) @ (yy-k)   for tt,yy in zip(ts.T, ys.T)]  ).T
		self.X        = XX.mean( axis=0 )
		self.t        = t
		self.y        = y
		self.c        = c
		self.XX       = XX
		self.tt       = ts
		self.yy       = ys
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