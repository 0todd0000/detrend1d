




def detrend(t, y, trend):
	fit = trend.fit(t, y)
	yd  = fit.get_detrended()
	return yd, fit
	
	
	
def detrend_intracycle(t, y, c, trend, regfn=None):
	pass