
'''
Cyclical fit class defintion
'''


import numpy as np
from matplotlib import pyplot as plt
from . fit import Fit



class CyclicalFit(Fit):
	def __init__(self, trend):
		super().__init__(trend)
		# new attributes:
		self.XX       = None  # design matrices at each time point
		self.regfn    = None  # registration function
		self.c        = None  # cycle labels
		self.tr       = None  # registered time vectors
		self.yr       = None  # registered DV
		self.yhatr    = None  # fits (registered)

	@property
	def uc(self):
		u = np.unique(c)
		if u[0]==0:
			u = u[1:]
		return u

	def _fit_cyclical(self):
		J,Q       = self.yr.shape
		r         = self.yr - self.yr.mean(axis=0)
		XX        = []
		beta      = []
		yhat      = []
		for q in range(Q):
			tt,yy = self.tr[:,q], r[:,q]
			X     = self._trend.get_design_matrix( tt )
			b     = self._fit(X, yy)
			yh    = X @ b
			XX.append( X )
			beta.append( b )
			yhat.append( yh )
		XX        = np.array( XX )
		beta      = np.asarray( beta ).T
		yhatr     = np.asarray( yhat ).T
		yhat      = self._unregister(yhatr)
		return XX, beta, yhatr, yhat

	def _register(self):
		tr,yr = self.regfn( self.t, self.y, self.c )
		return tr,yr
	
	def _unregister(self, yhatr):
		from scipy import interpolate
		yhat        = np.zeros( self.y.size )
		for i,(ttr,yyr) in enumerate( zip(self.tr, yhatr) ):
			b       = self.c==(i+1)
			f       = interpolate.interp1d(ttr, yyr)
			yhat[b] = f( self.t[b] )
		return yhat

	def fit(self, t, y, c, regfn=None):
		self.t     = t
		self.y     = y
		self.c     = c
		self.regfn = regfn
		_results   = self._register()
		self.tr    = _results[0]
		self.yr    = _results[1]
		_results   = self._fit_cyclical()
		self.XX    = _results[0]
		self.beta  = _results[1]
		self.yhatr = _results[2]
		self.yhat  = _results[3]
		self.X     = self.XX.mean(axis=0)
	
	def get_detrended_registered(self):
		return self.yr - self.yhatr
	
