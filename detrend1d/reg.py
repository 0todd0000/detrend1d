
'''
Registration functions
'''


import numpy as np


def interp_n(y, n=101):
	from scipy import interpolate
	t    = np.linspace(0, 1, y.size)
	ti   = np.linspace(0, 1, n)
	f    = interpolate.interp1d(t, y)
	return f(ti)


def register_linear_n(t, y, c, n=101):
	'''
	Linear registration to n nodes
	'''
	ti = [interp_n(t[c==u]) for u in range(1, c.max()+1)]
	yi = [interp_n(y[c==u]) for u in range(1, c.max()+1)]
	return np.array(ti), np.array(yi)
