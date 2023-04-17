
'''
Inter-cycle trends
'''

import numpy as np
from matplotlib import pyplot as plt
from . fit import Fit



class _Trend(object):
	
	def __repr__(self):
		s  = f'{self.__class__.__name__}\n'
		s += f'    beta     = {self.beta_str}\n'
		s += f'    isfitted = {self.isfitted}\n'
		return s

	
	@property
	def beta_str(self):
		return str( self.beta )
	@property
	def design_matrix(self):  # fits (used only during fitting)
		return self._fit.X if self.isfitted else None
	@property
	def isfitted(self):
		return self._fit.isfitted
	@property
	def yhat(self):
		return self._fit.yhat

	def detrend(self, t, y):
		self.fit(t, y)
		return y - self.yhat

	def fit(self, t, y):
		self._fit.fit(t, y)
		self.beta = self._fit.beta

	def plot(self, ax=None, t0=0, t1=10, n=51, **kwargs):
		ax    = plt.gca() if (ax is None) else ax
		t     = np.linspace(t0, t1, n)
		y     = self.apply(t, np.zeros(n))
		ax.plot(t, y, **kwargs)

	def plot_design(self, ax=None, **kwargs):
		self._fit.plot_design( ax, **kwargs )

	def plot_fit(self, ax=None, **kwargs):
		self._fit.plot( ax, **kwargs )
		


class Linear(_Trend):
	
	'''
	Model:   y(t) = a*t + b
	'''
	
	def __init__(self, slope=None, intercept=None):
		self._fit = Fit(self._X) # fitted model parameters
		a         = None if (slope is None) else float(slope)
		b         = None if (intercept is None) else float(intercept)
		self.beta = np.array([a, b])

	@staticmethod
	def _X(t):   # design matrix
		n      = t.size
		X      = np.zeros( (n, 2) )
		X[:,0] = t
		X[:,1] = 1
		return X

	def apply(self, t, y):
		a,b   = self.beta
		dy  = (a * t) + b
		return y + dy





class LinearFixedIntercept( Linear ):

	def __init__(self, slope=None, intercept=None):
		self._fit = Fit(self._X) # fitted model parameters
		a         = None if (slope is None) else float(slope)
		b         = 0 if (intercept is None) else float(intercept)
		self.beta = np.array([a, b])
		self._fit.set_constant( b )

	@staticmethod
	def _X(t):   # design matrix
		n      = t.size
		X      = np.zeros( (n, 1) )
		X[:,0] = t
		return X



