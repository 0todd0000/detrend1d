
__version__ = '0.4.0'  # 2023-12-23

from . import trends
from . import reg




def detrend_trial_level(t, y, trend='linear', mean_corrected=False, intercept=None):
    import numpy as np
    from . fits import Fit
    trend = trends.str2trend( trend, intercept )
    fit   = Fit( trend )
    fit.fit(t, y)
    yd    = fit.get_detrended( mean_corrected )
    return yd, fit


def detrend_cycle_level(t, y, c, trend='linear', regfn=None):
    from . fits import CyclicalFit
    trend   = trends.str2trend( trend )
    fit     = CyclicalFit( trend )
    fit.fit(t, y, c, regfn=regfn)
    yd      = fit.get_detrended()
    return yd, fit


detrend = detrend_trial_level