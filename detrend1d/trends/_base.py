
'''
Inter-cycle trends
'''

import numpy as np
from matplotlib import pyplot as plt



class _Trend(object):
	
	def __init__(self):
		self.beta     = None
		self.fixed    = None
		self._init_beta()

	def __repr__(self):
		s  = f'{self.__class__.__name__}\n'
		s += f'    beta     = {self.beta_str}\n'
		return s

	@staticmethod
	def _X(t):   # design matrix (abstract method)
		pass

	def _init_beta(self):  # initialize model parameters (abstract method)
		pass
	
	@property
	def beta_str(self):
		return str( self.beta )
		
	@property
	def free(self):   # design matrix (abstract method)
		return np.logical_not( self.fixed )

	@property
	def hasfixed(self):   # design matrix (abstract method)
		return np.any( self.fixed )

	def apply(self, t, y):
		return (self._X(t) @ self.beta) + y

	# def fit(self, t, y):
	# 	from .. fits import Fit
	# 	fit   = Fit( self )
	# 	fit.fit( t, y )
	# 	# self.set_beta( fit.beta )
	# 	return fit
	#
	# # def lse(self, t, y):
	# # 	X  = self._X(t)
	# #
	
	
	def get_design_matrix(self, t):
		return self._X(t)
	
	def plot(self, ax=None, t0=0, t1=10, n=51, y0=None, **kwargs):
		ax    = plt.gca() if (ax is None) else ax
		t     = np.linspace(t0, t1, n)
		y0    = np.zeros(n) if (y0 is None) else y0
		y     = self.apply(t, y0)
		ax.plot(t, y, **kwargs)

	def set_beta(self, b):
		self.beta  = np.asarray(b)





