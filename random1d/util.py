
import numpy as np



def around(x, prec=None):
	if prec is not None:
		x = np.around(x, prec)
	return x


def interp1d(y, n=101, **kwargs):
	from scipy import interpolate
	Q    = y.size if (y.ndim==1) else y.shape[1]
	q0   = np.linspace(0, 1, Q)
	qi   = np.linspace(0, 1, n)
	f    = interpolate.interp1d(q0, y, **kwargs)
	yi   = f(qi)
	return yi