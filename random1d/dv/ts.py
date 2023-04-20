
import numpy as np
import matplotlib.pyplot as plt
from .. util import around





class TimeSeries(object):
	def __init__(self, t=None, y=None):
		self._trend = None  # true trend used (if any)
		self.t      = []  if t is None else np.asarray(t)
		self.y      = []  if y is None else np.asarray(y)
		
	def __repr__(self):
		s   = f'{self.__class__.__name__}\n'
		s  += f'    n    = {self.n}\n'
		s  += f'    hz   = {self.hz}\n'
		s  += f'    durn = {self.durn}\n'
		return s
	
	@property
	def durn(self):
		return 0 if self.isempty else (self.t1 - self.t0)
	@property
	def dt(self):
		return 0 if self.isempty else np.diff(self.t).mean()
	@property
	def hz(self):
		return 0 if self.isempty else 1/self.dt
	@property
	def isempty(self):
		return len(self.t)==0
	@property
	def n(self):
		return 0 if self.isempty else self.t.size
	@property
	def t0(self):
		return 0 if self.isempty else self.t[0]
	@property
	def t1(self):
		return 0 if self.isempty else self.t[-1]

	
	def append(self, t, y=None, add_dt=True):
		if isinstance(t, TimeSeries):
			t,y = t.t, t.y
		t      = t - t[0]
		t      = self.t1 + t + self.dt if add_dt else t
		self.t = np.append(self.t, t)
		self.y = np.append(self.y, y)
		return t.size
	
	def interp_durn(self, durn):
		t   = np.linspace(0, durn, self.n)
		obj = TimeSeries(t, self.y)
		obj.__class__ = self.__class__
		return obj

	def interp_n(self, n):
		from scipy import interpolate
		ti   = np.linspace(self.t0, self.t1, n)
		f    = interpolate.interp1d(self.t, self.y)
		yi   = f(ti)
		obj = TimeSeries(ti, yi)
		obj.__class__ = self.__class__
		return obj

	def interp_hz(self, hz):
		from scipy import interpolate
		dt     = 1.0 / hz
		ti     = np.arange(self.t0, self.t1, dt)
		f      = interpolate.interp1d(self.t, self.y)
		yi     = f(ti)
		obj    = TimeSeries(ti, yi)
		obj.__class__ = self.__class__
		return obj
	
	def plot(self, ax=None, **kwargs):
		ax = plt.gca() if (ax is None) else ax
		ax.plot(self.t, self.y, **kwargs)

	def segment(self, b, as_timeseries=True):
		t,y   = self.t[b], self.y[b]
		ts    = TimeSeries(t, y)
		if not as_timeseries:
			ts.__class__ = self.__class__
		return ts
	
	def set_true_trend(self, trend):
		self._trend   = trend
	
	
	def split_at_time(self, t):
		i0            = self.t < t
		i1            = np.logical_not( i0 )
		t0,y0         = self.t[i0], self.y[i0]
		t1,y1         = self.t[i1], self.y[i1]
		ts0,ts1       = TimeSeries(t0, y0), TimeSeries(t1, y1)
		ts0.__class__ = self.__class__
		ts1.__class__ = self.__class__
		return ts0, ts1


	def write_csv(self, fpath, prec=None):
		t     = around(self.t, prec)
		y     = around(self.y, prec)
		if self._trend is None:
			with open(fpath, 'w') as f:
				f.write('t,y\n')
				for tt,yy in zip(t, y):
					f.write( f'{tt},{yy}\n' )
		else:
			yhat = around( self._trend.asarray(t), prec )
			with open(fpath, 'w') as f:
				f.write('t,y,trend\n')
				for tt,yy,yyh in zip(t, y, yhat):
					f.write( f'{tt},{yy},{yyh}\n' )
			




