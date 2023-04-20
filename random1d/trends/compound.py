
'''
Compound trends
'''

import numpy as np
from matplotlib import pyplot as plt
from . _base import _Trend


class TrendCompound(_Trend):
	
	iscompound       = True
	
	def __init__(self, inter=None, intra=None):
		self.trend0  = inter
		self.trend1  = intra
		
	@property
	def beta(self):
		return [self.trend0.beta, self.trend1.beta]
	
	def apply(self, t, y):
		y1 = self.trend0.apply(t, y)
		return self.trend1.apply(t, y1)

	def asarray(self, t, c):
		yhat0 = self.trend0.asarray(t)
		yhat1 = self.trend1.asarray(t, c)
		return yhat0, yhat1

	def plot(self, ax=None, t0=0, t1=10, n=51):
		ax    = plt.gca() if (ax is None) else ax
		t     = np.linspace(t0, t1, n)
		y     = self.apply(t, np.zeros(n))
		ax.plot(t, y)	

