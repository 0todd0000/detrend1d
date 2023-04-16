

import numpy as np

class _LinearTrend(object):
	def __init__(self):
		self._n    = None       # number of time series nodes (used only during fitting)
		self._t    = None       # time vector (used only during fitting)
		self.beta  = None
		self.isfit = False

	@property
	def _Xi(self):  # pseudo-inverse of design matrix (used only during fitting)
		return np.linalg.pinv(self._X)
	
	@property
	def _yhat(self):  # fits (used only during fitting)
		return self._X @ self.beta

	def apply(self, y, t=None):
		t  = np.arange(y.size) if (t is None) else t
		v  = self.slope * t + self.intercept
		return y + v

	def get_fitted(self):
		return self._yhat
	
	def fit(self, t, y):
		self._n    = t.size
		self._t    = t
		self.beta  = self._Xi @ y
		self.isfit = True
	
	
	def plot(self, ax=None, trange=None, n=51):
		ax    = plt.gca() if (ax is None) else ax
		t0,t1 = (0,1) if (trange is None) else (0,1)
		t     = np.linspace(t0, t1, n)
		y0    = np.zeros(n)
		y     = self.apply(y0, t=t)
		ax.plot(t, y)


class Linear( _LinearTrend ):
	def __init__(self, slope=1, intercept=0):
		super().__init__()
		self.beta  = np.array([intercept, slope])

	@property
	def _X(self):   # design matrix (used only during fitting)
		n      = self._n
		X      = np.zeros( (n, 2) )
		X[:,0] = 1
		X[:,1] = self._t
		return X

	@property
	def intercept(self):
		return self.beta[0]
	@property
	def slope(self):
		return self.beta[1]
	
	


class LinearWithFixedIntercept( _LinearTrend ):
	def __init__(self, slope=1, intercept=0):
		super().__init__()
		self.beta      = np.array([slope])
		self.intercept = intercept
		# self.beta  = np.array([intercept, slope])
		# self._beta = 

	@property
	def _X(self):   # design matrix (used only during fitting)
		n      = self._n
		X      = np.zeros( (n, 1) )
		X[:,0] = self._t
		return X
	
	@property
	def _yhat(self):  # fits (used only during fitting)
		return self.intercept + (self._X @ self.beta)
	
	@property
	def slope(self):
		return self.beta[0]
	
	
	def fit(self, t, y):
		self._n    = t.size
		self._t    = t
		# ahat       = np.linalg.pinv(self.X[i]) @ y[i]
		b          = self.intercept
		self.beta  = self._Xi @ (y - b)
		# _ahat      = float( self._Xi @ (y - b) )
		# self.beta  = np.array( [ _ahat , b ] )
		self.isfit = True
		
	
# class LinearWithFixedIntercept( _LinearTrend ):
# 	def __init__(self, slope=1, intercept=0):
# 		super().__init__()
# 		self.beta  = np.array([intercept, slope])
#
# 	@property
# 	def _X(self):   # design matrix (used only during fitting)
# 		n      = self._n
# 		X      = np.zeros( (n, 1) )
# 		X[:,0] = self._t
# 		return X
#
#
# 	@property
# 	def _yhat(self):  # fits (used only during fitting)
# 		return self.beta[0] + self._X @ [self.beta[1]]
#
#
# 	def fit(self, t, y):
# 		self._n    = t.size
# 		self._t    = t
# 		b          = self.intercept
# 		_ahat      = float( self._Xi @ (y + b) )
# 		self.beta  = np.array( [ _ahat , b ] )
# 		self.isfit = True