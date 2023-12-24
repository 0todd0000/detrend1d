
import numpy as np
from matplotlib import pyplot as plt
from . trends import Exponential, Linear, Polynomial2, Polynomial3





def str2trend(s, intercept=None):
    s  = str(s).lower()
    if s == 'exp':
        trend = Exponential( intercept )
    elif s == 'linear':
        trend = Linear( intercept )
    elif s == 'poly2':
        trend = Polynomial2( intercept )
    elif s == 'poly3':
        trend = Polynomial3( intercept )
    else:
        trendstrs = 'linear', 'exp', 'poly2', 'poly3'
        raise ValueError( f'Unknown trend: "{s}". Trend must be one of: {trendstrs}')
    return trend