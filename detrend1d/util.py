
import numpy as np




def interp1d(y, n=101, **kwargs):
	from scipy import interpolate
	Q    = y.size if (y.ndim==1) else y.shape[1]
	q0   = np.linspace(0, 1, Q)
	qi   = np.linspace(0, 1, n)
	f    = interpolate.interp1d(q0, y, **kwargs)
	yi   = f(qi)
	return yi