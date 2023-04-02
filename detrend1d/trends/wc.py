
'''
Within-cycle non-constant trends
'''


import numpy as np



class Linear(object):
	pass
	# def __init__(self, slope0=-1, slope1=1, intercept0=0, intercept1=0):
	# 	self.a0              = slope0
	# 	self.a1              = slope1
	# 	self.b0              = intercept0
	# 	self.b1              = intercept1
	#
	#
	# def apply(self, y, cycle, t=None):
	# 	t  = np.arange(y.size) if (t is None) else t
	# 	y1 =
	# 	for u in np.sort( np.unique(cycle) ):
	# 		i  = cycle==u
	# 		n  = i.sum()
	# 		a  = np.linspace(self.a0, self.a1, n)
	# 		b  = np.linspace(self.b0, self.b1, n)
	# 		vv = a * t[i] + b
	# 		yy = y[i] + vv
	#
	#
	# 	v  = self.a * t + self.b
	# 	return y + v
	#
	#
	# # def apply(self, y, t=None):
	# # 	t  = np.arange(y.size) if (t is None) else t
	# # 	v  = self.a * t + self.b
	# # 	return y + v