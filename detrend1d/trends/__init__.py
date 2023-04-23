
import numpy as np
from matplotlib import pyplot as plt
# from . import inter, intra
from . trends import Linear, LinearFixedIntercept





def str2trend(s):
	s = str(s).lower()
	if s == 'linear':
		trend = Linear()
	elif s == 'linear_fixed_intercept':
		trend = LinearFixedIntercept()
	else:
		trendstrs = 'linear', 'linear_fixed_intercept'
		raise ValueError( f'Unknown trend: "{s}". Trend must be one of: {trendstrs}')
	return trend