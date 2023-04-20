
'''
Inter-cycle trends
'''

import numpy as np
from matplotlib import pyplot as plt
from . _base import _Trend
# from . fit import Fit

__all__ = ['TrendLinear']



class TrendLinear(_Trend):
	
	'''
	Model:   y(t) = a*t + b
	'''
	
	label         = 'trend_inter'
	
	def __init__(self, slope=None, intercept=None):
		a         = float( slope )
		b         = float( intercept )
		self.beta = np.array([a, b])

	def apply(self, t, y):
		a,b   = self.beta
		dy  = (a * t) + b
		return y + dy





# class TrendLinearWithFixedIntercept( Linear ):
#
# 	def __init__(self, slope=None, intercept=None):
# 		# self._fit = Fit(self._X) # fitted model parameters
# 		a         = None if (slope is None) else float(slope)
# 		b         = 0 if (intercept is None) else float(intercept)
# 		self.beta = np.array([a, b])
# 		self._fit.set_constant( b )
#
# 	@staticmethod
# 	def _X(t):   # design matrix
# 		n      = t.size
# 		X      = np.zeros( (n, 1) )
# 		X[:,0] = t
# 		return X


