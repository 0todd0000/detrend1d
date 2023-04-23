
import numpy as np
from matplotlib import pyplot as plt
from . trends import Exponential, Linear, LinearFixedIntercept, Polynomial2, Polynomial3





def str2trend(s):
	s = str(s).lower()
	if s in ['exp', 'exponenital']:
		trend = Exponential()
	elif s in ['lin', 'linear']:
		trend = Linear()
	elif s in ['linfi', 'linear_fixed_intercept']:
		trend = LinearFixedIntercept()
	elif s in ['poly', 'poly2', 'polynomial', 'polynomial2']:
		trend = Polynomial2()
	elif s in ['poly3', 'polynomial3']:
		trend = Polynomial3()
	else:
		trendstrs = 'linear', 'linear_fixed_intercept'
		raise ValueError( f'Unknown trend: "{s}". Trend must be one of: {trendstrs}')
	return trend