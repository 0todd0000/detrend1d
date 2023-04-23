
__version__ = '0.3.0'  # 2023-04-20

from . import trends
from . import reg




def detrend(t, y, trend='linear'):
	trend = trends.str2trend( trend )
	fit   = trend.fit(t, y)
	yd    = fit.get_detrended()
	return yd, fit
	
	
	
def detrend_intracycle(t, y, c, trend, regfn=None):
	pass