

import numpy as np
from scipy import interpolate
from rft1d import randn1d



class Datum(object):
	def __init__(self, t, y):
		self.t               = t
		self.y               = y
		# self.durn_var        = None
		# self.intercycle_durn = None
		self.trend           = None

	
	def generate_single_cycle(self, cycledurn_sd=None, t0=0):
		if cycledurn_sd is None:
			t,y      = self.t, self.y
		else:
			cdurn0   = self.t[-1]
			dt       = self.t[1] - self.t[0]
			cdurn    = cdurn0 + cycledurn_sd * np.random.randn()
			n        = round(cdurn / dt)
			ti       = np.linspace( 0, self.t[-1], n )
			f        = interpolate.interp1d(self.t, self.y)
			y        = f(ti)
			t        = t0 + np.linspace( 0, cdurn, n )
		return t,y
	
	def generate_session_datum(self, durn=10, hz=100, cycledurn_sd=None, intercycle_durn=None):
		t,y = self.t, self.y
		dt  = t[1] - t[0]
		c   = [0]*t.size
		i   = 0
		while t[-1] < durn:
			if cycledurn_sd is None:
				tt = self.t + t[-1] + dt
				yy = self.y
			else:
				t0       = t[-1] + dt
				tt,yy    = self.generate_single_cycle( cycledurn_sd, t0 )
			t  = np.hstack( [t, tt] )
			y  = np.hstack( [y, yy] )
			i += 1
			c += [i] * tt.size
		b      = t <= durn
		t,c,y  = t[b], np.array(c)[b], y[b]
		if self.trend is not None:
			y  = self.trend.apply(y, t=t)
		return t,c,y


	def set_trend(self, trend):
		self.trend   = trend
	
	
