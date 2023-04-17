

'''
Intra-cycle trends
'''

import numpy as np
from matplotlib import pyplot as plt



class Linear(object):
	'''
	Model:   y(t) = a*t + b
	'''

	def __init__(self, slope=None, intercept=None):
		self.a  = None if (slope is None) else np.asarray(slope)
		self.b  = None if (intercept is None) else np.asarray(intercept)

	@property
	def isscalar(self):
		return self.a.size == 1
	@property
	def Q(self):
		return self.a.size

	# def apply(self, y, t=None):
	# 	t  = np.arange(y.size) if (t is None) else t
	# 	v  = self.slope * t + self.intercept
	# 	return y + v

	def apply(self, t, y):
		if self.isscalar or (self.Q == y.size):
			a,b   = self.a, self.b
		else:
			from .. util import interp1d
			a     = interp1d(self.a, y.size)
			b     = interp1d(self.b, y.size)
		dy  = (a * t) + b
		return y + dy

	def plot(self, ax=None, t0=0, t1=10, n=51):
		ax    = plt.gca() if (ax is None) else ax
		t     = np.linspace(t0, t1, n)
		y     = self.apply(t, np.zeros(n))
		ax.plot(t, y)
