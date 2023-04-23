
__version__ = '0.3.0'  # 2023-04-20

from . import trends
from . import reg




def detrend(t, y, trend='linear'):
	import numpy as np
	trend   = trends.str2trend( trend )
	_hasnan = np.any( np.isnan(y) )
	if _hasnan:
		i   = np.logical_not( np.isnan(y) )
		t,y = t[i], y[i]
	fit   = trend.fit(t, y)
	yd    = fit.get_detrended()
	if _hasnan:
		_yd   = yd
		yd    = np.array( [np.nan] * i.size )
		yd[i] = _yd
	return yd, fit
	
	
	
def detrend_intracycle(t, y, c, trend, regfn=None):
	pass