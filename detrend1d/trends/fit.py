
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
		self.constant = 0
		# self.fnX      = fnX   # function that generates design matrix
		# self.isfitted = False
		self.t        = None
		self.y        = None

	# @property
	# def Xi(self):  # design matrix pseudo-inverse
	# 	return np.linalg.pinv(self.X)
	# # @property
	# # def isempty(self):
	# # 	return self.beta is None
		
	@property
	def yhat(self):
		return self.X @ self.beta # + self.constant
	
	def _fit(self, y):
		# self._trend.lse()
		if self._trend.hasfixed:
			i0,i1 = self._trend.free, self._trend.fixed
			X0    = self.X[ : , i0 ]        # free-to-vary columns
			X1    = self.X[ : , i1 ]        # fixed columns
			b1    = self._trend.beta[ i1 ]  # fixed betas
			y1    = X1 @ b1
			print( y1 )
			b0    = np.linalg.pinv(X0) @ (y-y1)  # free-to-vary betas
			beta  = np.zeros( self.X.shape[1] )
			beta[i0]  = b0
			beta[i1]  = b1
		else:
			beta = np.linalg.pinv(self.X) @ y
		return beta

	
	def fit(self, t, y):
		self.t    = t
		self.y    = y
		self.X    = self._trend.get_design_matrix( t )
		self.beta = self._fit(y)
		# X,beta        = self._trend.lse(t, y)
		#
		# self.X        = X
		# self.beta     = beta
		# # self.t        = t
		# # self.y        = y
		# # self.isfitted = True
	
	def plot(self, ax=None, **kwargs):
		ax    = plt.gca() if (ax is None) else ax
		ax.plot(self.t, self.yhat, **kwargs)

	def plot_design(self, ax=None, **kwargs):
		ax    = plt.gca() if (ax is None) else ax
		ax.pcolor(self.X, **kwargs)

	# def plot(self, ax=None, **kwargs):
	# 	if self.isfitted:
	# 		ax    = plt.gca() if (ax is None) else ax
	# 		ax.plot(self.t, self.yhat, **kwargs)
	# 	else:
	# 		print('Trend not yet fitted.')
			
	# def plot_design(self, ax=None, **kwargs):
	# 	if self.isfitted:
	# 		ax    = plt.gca() if (ax is None) else ax
	# 		ax.pcolor(self.X, **kwargs)
	# 	else:
	# 		print('Trend not yet fitted.')
			
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


	def fit_registered(self, t, y):
		J,Q       = y.shape
		k         = self.constant
		beta      = []
		yhat      = []
		XX        = []
		for q in range(Q):
			tt,yy = t[:,q], y[:,q]
			X     = self.fnX(tt)
			b     = np.linalg.pinv( X ) @ (yy - k)
			yh    = (X @ b) + k
			XX.append( X )
			beta.append( b )
			yhat.append( yh )
		self.XX   = XX
		self.t    = t
		self.y    = y
		self.beta = np.asarray( beta ).T
		self.yhat = np.asarray( yhat ).T
			


	def fit(self, t, y, c):
		pass
		# uc    = np.unique*
		# ts                = np.vstack(  [ t[c==u]  for u in np.unique(c) ]  )
		# ys                = np.vstack(  [ y[c==u]  for u in np.unique(c) ]  )
		# XX                = np.array(   [ self.fnX(tt) for tt in ts.T ]  )
		# k                 = self.constant
		# beta              = np.array(  [np.linalg.pinv( X ) @ (yy - k)  for X,yy in zip(XX, ys.T)]  ).T
		# yhats             = np.array([(X @ b) + k   for X,b in zip(XX, beta.T)]).T
		# yhat              = np.zeros(y.size)
		# for u,yh in zip(np.unique(c), yhats):
		# 	yhat[c==u] = yh
		# # assemble results:
		# self.t            = t
		# self.y            = y
		# self.c            = c
		# self.ts           = ts
		# self.ys           = ys
		# self.XX           = XX
		# self.X            = XX.mean( axis=0 )
		# self.beta         = beta
		# self.yhat         = yhat
		# self.yhat_stacked = yhats
		# self.isfitted     = True

	
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