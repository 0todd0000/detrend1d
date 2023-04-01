

import numpy as np



class Linear(object):
	def __init__(self, slope=1, intercept=0):
		self.a               = slope
		self.b               = intercept
		
		
	def apply(self, y, t=None):
		t  = np.arange(y.size) if (t is None) else t
		v  = self.a * t + self.b
		return y + v
