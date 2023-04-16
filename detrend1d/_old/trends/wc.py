
'''
Within-cycle non-constant trends
'''


import numpy as np




class Linear(object):
	def __init__(self, slope=None, intercept=None):
		self.a  = slope
		self.b  = intercept
		
	@property
	def Q(self):
		return self.a.size
	
	def apply(self, y0, t0):
		Q0   = y0.size
		if self.Q == Q0:
			a0,b0 = self.a, self.b
		else:
			from .. util import interp1d
			a0    = interp1d(self.a, Q0)
			b0    = interp1d(self.b, Q0)
		v0  = (a0 * t0) + b0
		return y0 + v0