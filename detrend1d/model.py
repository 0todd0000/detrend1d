
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
from . data import SessionData, MultiSessionData



class MultiSessionExperimentModel(object):
	def __init__(self, ms, deg=1):
		assert isinstance(deg, int), '"deg" must be an integer'
		assert deg>=0, '"deg" must be 0 or greater'
		self.deg   = deg       # polynomial (fit) degree
		self.ms    = ms        # MultiSessionData object
		self.polyc = None      # polynomial coefficients (np.poly1d object)
		self._fit()

	def _fit(self):
		x,y        = self.ms.t, self.ms.y
		self.polyc = np.polyfit(x, y, deg=self.deg)
		

	# # MultiSessionData properties:
	# @property
	# def J(self):   # sample size (total)
	# 	return self.ms.J
	# @property
	# def t(self):   # sample size (total)
	# 	return self.ms.t
	# @property
	# def t(self):   # sample size (total)
	# 	return self.ms.t
	# @property
	# def ucond(self):   # unique conditions (integers)
	# 	return self.ucond
	# @property
	# def y(self):    # data
	# 	pass

	@property
	def yd(self):   # detrended data
		return self.ms.y - self.yhat
	
	@property
	def yhat(self): # fits
		poly   = np.poly1d( self.polyc )
		yhat   = poly( self.ms.t )
		return yhat
		

	def get_design_matrix(self):
		J,C        = self.ms.J, self.ms.ncond
		if self.deg == 0:
			X      = np.zeros( (J,C) )
			for i,u in enumerate( self.ms.ucond ):
				X[:,i] = self.ms.cond == u
		else:
			X      = np.zeros( (J,C+1) )
			X[:,0] = self.yhat
			for i,u in enumerate( self.ms.ucond ):
				X[:,i+1] = self.ms.cond == u
		return X

	def get_detrended_multisessiondata(self):
		msd    = deepcopy( self.ms )
		yd     = self.yd  # detrended data (all sessions, flattened)
		for i,ss in enumerate(msd.sessions):
			ss.y  = yd[ msd.sess==i ]
		return msd


	def plot(self, ax=None, **kwargs):
		ax    = plt.gca() if (ax is None) else ax
		if self.deg in [0, 1]:
			t0,t1  = self.ms.tminmax
			poly   = np.poly1d( self.polyc )
			y0,y1  = poly( [t0,t1] )
			h      = ax.plot( [t0,t1], [y0,y1], **kwargs)[0]
		else:
			t0,t1  = self.ms.tminmax
			t      = np.linspace(t0, t1, 51)
			poly   = np.poly1d( self.polyc )
			y      = poly(t)
			h      = ax.plot( t, y, **kwargs )[0]
		return h



