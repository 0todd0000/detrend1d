
'''
Cyclical fit class defintion
'''


import numpy as np
from matplotlib import pyplot as plt




class CyclicalFit(object):
	def __init__(self, trend):
		self._trend   = trend
		self.X        = None
		self.beta     = None
		self.t        = None
		self.y        = None
		self.yhat     = None
		# new attributes:
		self.XX       = None  # design matrices at each time point
		self.regfn    = None
		self.c        = None
		self.tr       = None  # registered time vectors
		self.yr       = None  # registered DV
		self.yhatr    = None  # fits (registered)
		
		

	@property
	def uc(self):
		u = np.unique(c)
		if u[0]==0:
			u = u[1:]
		return u

	def _fit(self, X, y):
		if self._trend.hasfixed:
			i0,i1 = self._trend.free, self._trend.fixed
			X0    = X[ : , i0 ]        # free-to-vary columns
			X1    = X[ : , i1 ]        # fixed columns
			b1    = self._trend.beta[ i1 ]  # fixed betas
			y1    = X1 @ b1                 # constants
			b0    = np.linalg.pinv(X0) @ (y-y1)  # free-to-vary betas
			beta  = np.zeros( X.shape[1] )  # all parameters
			beta[i0]  = b0
			beta[i1]  = b1
		else:
			beta  = np.linalg.pinv(X) @ y
		return beta


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
			# b     = np.linalg.pinv( X ) @ yy
			yh    = X @ b
			XX.append( X )
			beta.append( b )
			yhat.append( yh )
		beta      = np.asarray( beta ).T
		yhatr     = np.asarray( yhat ).T
		yhat      = self._unregister(yhatr)
		return XX, beta, yhatr, yhat

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
		tr,yr      = self.regfn( self.t, self.y, self.c )
		self.tr    = tr
		self.yr    = yr
		_results   = self._fit_cyclical()
		self.XX    = _results[0]
		self.beta  = _results[1]
		self.yhatr = _results[2]
		self.yhat  = _results[3]
		# print( beta.shape, yhatr.shape, yhat.shape )
		
		# self.X    = self._trend.get_design_matrix( t )
		# self.beta = self._fit(y)
		# self.yhat = self.X @ self.beta
		# self._trend.set_beta( self.beta )
	
	def get_detrended(self):
		return self.y - self.yhat
	
	def get_detrended_registered(self):
		return self.yr - self.yhatr
	
	def plot(self, ax=None, **kwargs):
		ax    = plt.gca() if (ax is None) else ax
		ax.plot(self.t, self.yhat, **kwargs)

	def plot_design(self, ax=None, **kwargs):
		ax    = plt.gca() if (ax is None) else ax
		ax.pcolor(self.X, **kwargs)






	# def fit_registered(self, t, y):
	# 	J,Q       = y.shape
	# 	k         = self.constant
	# 	beta      = []
	# 	yhat      = []
	# 	XX        = []
	# 	for q in range(Q):
	# 		tt,yy = t[:,q], y[:,q]
	# 		X     = self.fnX(tt)
	# 		b     = np.linalg.pinv( X ) @ (yy - k)
	# 		yh    = (X @ b) + k
	# 		XX.append( X )
	# 		beta.append( b )
	# 		yhat.append( yh )
	# 	self.XX   = XX
	# 	self.t    = t
	# 	self.y    = y
	# 	self.beta = np.asarray( beta ).T
	# 	self.yhat = np.asarray( yhat ).T
	#
	#
	#
	# def fit(self, t, y, c):
	# 	pass
	# 	# uc    = np.unique*
	# 	# ts                = np.vstack(  [ t[c==u]  for u in np.unique(c) ]  )
	# 	# ys                = np.vstack(  [ y[c==u]  for u in np.unique(c) ]  )
	# 	# XX                = np.array(   [ self.fnX(tt) for tt in ts.T ]  )
	# 	# k                 = self.constant
	# 	# beta              = np.array(  [np.linalg.pinv( X ) @ (yy - k)  for X,yy in zip(XX, ys.T)]  ).T
	# 	# yhats             = np.array([(X @ b) + k   for X,b in zip(XX, beta.T)]).T
	# 	# yhat              = np.zeros(y.size)
	# 	# for u,yh in zip(np.unique(c), yhats):
	# 	# 	yhat[c==u] = yh
	# 	# # assemble results:
	# 	# self.t            = t
	# 	# self.y            = y
	# 	# self.c            = c
	# 	# self.ts           = ts
	# 	# self.ys           = ys
	# 	# self.XX           = XX
	# 	# self.X            = XX.mean( axis=0 )
	# 	# self.beta         = beta
	# 	# self.yhat         = yhat
	# 	# self.yhat_stacked = yhats
	# 	# self.isfitted     = True
	#
	#
	# def plot(self, ax=None, **kwargs):
	# 	if self.isfitted:
	# 		ax    = plt.gca() if (ax is None) else ax
	# 		ax.plot(self.t, self.yhat, **kwargs)
	# 	else:
	# 		print('Trend not yet fitted.')
	#
	# def plot_design(self, ax=None, **kwargs):
	# 	if self.isfitted:
	# 		ax    = plt.gca() if (ax is None) else ax
	# 		ax.pcolor(self.X, **kwargs)
	# 	else:
	# 		print('Trend not yet fitted.')
	#
	# def set_constant(self, x):
	# 	self.constant  = x