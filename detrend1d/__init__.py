
__version__ = '0.3.0'  # 2023-04-20

from . import trends
from . import reg




def detrend(t, y, trend='linear', mean_corrected=True, intercept=None):
	import numpy as np
	from . fits import Fit
	trend = trends.str2trend( trend, intercept )
	fit   = Fit( trend )
	fit.fit(t, y)
	yd    = fit.get_detrended( mean_corrected )
	return yd, fit


def detrend_intracycle(t, y, c, trend='linear', regfn=None):
	from . fits import CyclicalFit
	trend   = trends.str2trend( trend )
	fit     = CyclicalFit( trend )
	fit.fit(t, y, c, regfn=regfn)
	yd      = fit.get_detrended()
	return yd, fit
	