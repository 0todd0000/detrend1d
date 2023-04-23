
'''
Fit class defintion
'''

import numpy as np
from matplotlib import pyplot as plt



class Fit(object):
	def __init__(self, trend):
		self._msk     = None   # mask (if DV contains any np.nan)
		self._trend   = trend
		self.X        = None
		self.beta     = None
		self.t        = None
		self.y        = None
		self.yhat     = None

	def _fit(self, X, y):
		if self._trend.hasfixed:
			i0,i1 = self._trend.free, self._trend.fixed
			X0    = X[ : , i0 ]             # free-to-vary columns
			X1    = X[ : , i1 ]             # fixed columns
			b1    = self._trend.beta[ i1 ]  # fixed betas
			y1    = X1 @ b1                 # constants
			b0    = np.linalg.pinv(X0) @ (y-y1)  # free-to-vary betas
			beta  = np.zeros( X.shape[1] )  # all parameters
			beta[i0]  = b0
			beta[i1]  = b1
		else:
			beta  = np.linalg.pinv(X) @ y
		return beta

	def _mask(self):
		nan      = np.isnan( self.y )
		if np.any( nan ):
			i    = np.logical_not( nan )
			self.t    = self.t[i]
			self.y    = self.y[i]
			self._msk = i

	def _unmask(self):
		if self._msk is not None:
			i         = self._msk
			n         = i.size
			nan       = np.array( [np.nan] * n )
			t,y,yhat  = nan, nan.copy(), nan.copy()
			t[i]      = self.t
			y[i]      = self.y
			yhat[i]   = self.yhat
			self.t    = t
			self.y    = y
			self.yhat = yhat

	def fit(self, t, y):
		self.t     = t
		self.y     = y
		self._mask()
		self.X     = self._trend.get_design_matrix( self.t )
		self.beta  = self._fit(self.X, self.y)
		self.yhat  = self.X @ self.beta
		self._unmask()
	
	def get_detrended(self, mean_corrected=True):
		yd  = self.y - self.yhat
		if mean_corrected:
			yd += np.nanmean( self.y )
		return yd
	
	def plot(self, ax=None, **kwargs):
		ax    = plt.gca() if (ax is None) else ax
		ax.plot(self.t, self.yhat, **kwargs)

	def plot_design(self, ax=None, **kwargs):
		ax    = plt.gca() if (ax is None) else ax
		ax.pcolor(self.X, **kwargs)

