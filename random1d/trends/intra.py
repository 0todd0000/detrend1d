

'''
Intra-cycle trends
'''

import numpy as np
from matplotlib import pyplot as plt
from . inter import _Trend
# from . fit import CyclicalFit

__all__ = ['TrendIntraCycleLinear']


class TrendIntraCycleLinear(_Trend):
	'''
	Model:   y(t) = a*t + b
	'''
	
	label         = 'trend_intra'

	def __init__(self, slope=None, intercept=None):
		# self._fit = CyclicalFit(self._X) # fitted model parameters
		a         = None if (slope is None) else np.array(slope)
		b         = None if (intercept is None) else np.array(intercept)
		self.beta = np.vstack( [a, b] )

	# @staticmethod
	# def _X(t):   # design matrix
	# 	n      = t.size
	# 	X      = np.zeros( (n, 2) )
	# 	X[:,0] = t
	# 	X[:,1] = 1
	# 	return X

	@property
	def beta_str(self):
		return f'{self.beta.shape} array'
	@property
	def intercept(self):
		return self.beta[1]
	@property
	def slope(self):
		return self.beta[0]

	# @property
	# def Q(self):
	# 	return self.beta.shape[1]

	# def apply(self, y, t=None):
	# 	t  = np.arange(y.size) if (t is None) else t
	# 	v  = self.slope * t + self.intercept
	# 	return y + v

	def apply(self, t, y):
		from .. util import interp1d
		a     = interp1d(self.beta[0], y.size)
		b     = interp1d(self.beta[1], y.size)
		dy    = (a * t) + b
		return y + dy

	def asarray(self, t, c):
		yhat   = np.zeros(t.size)
		for u in np.unique(c):
			if u==0:
				continue
			i  = c==u
			tt = t[i]
			yh = self.apply(tt, np.zeros(tt.size))
			yhat[i] = yh
		return yhat

	# def fit(self, t, y, c):
	# 	self._fit.fit(t, y, c)
	# 	self.beta = self._fit.beta
	
	
	# def plot(self, ax=None, t0=0, t1=10, n=51):
	# 	ax    = plt.gca() if (ax is None) else ax
	# 	t     = np.linspace(t0, t1, n)
	# 	y     = self.apply(t, np.zeros(n))
	# 	ax.plot(t, y)


# class Linear(object):
# 	'''
# 	Model:   y(t) = a*t + b
# 	'''
#
# 	def __init__(self, slope=None, intercept=None):
# 		self.a  = None if (slope is None) else np.asarray(slope)
# 		self.b  = None if (intercept is None) else np.asarray(intercept)
#
# 	@property
# 	def isscalar(self):
# 		return self.a.size == 1
# 	@property
# 	def Q(self):
# 		return self.a.size
#
# 	# def apply(self, y, t=None):
# 	# 	t  = np.arange(y.size) if (t is None) else t
# 	# 	v  = self.slope * t + self.intercept
# 	# 	return y + v
#
# 	def apply(self, t, y):
# 		if self.isscalar or (self.Q == y.size):
# 			a,b   = self.a, self.b
# 		else:
# 			from .. util import interp1d
# 			a     = interp1d(self.a, y.size)
# 			b     = interp1d(self.b, y.size)
# 		dy  = (a * t) + b
# 		return y + dy
#
# 	def fit(self, t, y, c):
# 		yy  = np.vstack(  [ y[c==u]  for u in np.unique(c) ]  )
#
#
#
# 	def plot(self, ax=None, t0=0, t1=10, n=51):
# 		ax    = plt.gca() if (ax is None) else ax
# 		t     = np.linspace(t0, t1, n)
# 		y     = self.apply(t, np.zeros(n))
# 		ax.plot(t, y)


