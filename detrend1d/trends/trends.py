
'''
Inter-cycle trends
'''

import numpy as np
from . _base import _Trend

__all__  = ['Linear', 'LinearFixedIntercept']



# class Compound(object):
# 	def __init__(self, inter=None, intra=None):
# 		self.trend0  = inter
# 		self.trend1  = intra
#
# 	def apply(self, t, y):
# 		y1 = self.trend0.apply(t, y)
# 		return self.trend1.apply(t, y1)
#
# 	def plot(self, ax=None, t0=0, t1=10, n=51):
# 		ax    = plt.gca() if (ax is None) else ax
# 		t     = np.linspace(t0, t1, n)
# 		y     = self.apply(t, np.zeros(n))
# 		ax.plot(t, y)



class Linear(_Trend):
	
	'''
	Model:   y(t) = a*t + b
	'''
	
	@staticmethod
	def _X(t):   # design matrix
		n      = t.size
		X      = np.zeros( (n, 2) )
		X[:,0] = 1
		X[:,1] = t
		return X

	def _init_beta(self):
		self.beta        = np.array([0, 0])
		self.beta_labels = 'Intercept', 'Slope'
		self.fixed       = np.array([False, False])
		





class LinearFixedIntercept( Linear ):

	'''
	Model:   y(t) = a*t + b;  b fixed
	'''

	def __init__(self, intercept=0):
		self.intercept = float( intercept )
		super().__init__()

	def _init_beta(self):
		self.beta        = np.array([self.intercept, 0])
		self.beta_labels = 'Intercept', 'Slope'
		self.fixed       = np.array([False, True])
		
		



