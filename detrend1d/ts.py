
import numpy as np
import matplotlib.pyplot as plt






class TimeSeries(object):
	def __init__(self, t=None, y=None):
		self.t     = []  if t is None else t
		self.y     = []  if y is None else y
		
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
	
	def detrend(self, trend):
		trend.fit( self.t, self.y )
		return DetrendedTimeSeries( self.t, self.y, trend )

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

	def segment(self, b):
		t,y   = self.t[b], self.y[b]
		ts    = TimeSeries(t, y)
		ts.__class__ = self.__class__
		return ts
	
	def split_at_time(self, t):
		i0            = self.t < t
		i1            = np.logical_not( i0 )
		t0,y0         = self.t[i0], self.y[i0]
		t1,y1         = self.t[i1], self.y[i1]
		ts0,ts1       = TimeSeries(t0, y0), TimeSeries(t1, y1)
		ts0.__class__ = self.__class__
		ts1.__class__ = self.__class__
		return ts0, ts1


class NullTimeSeries(TimeSeries):
	def __init__(self, durn, hz, nullvalue=0 ):
		dt  = 1/hz
		t   = np.arange(0, durn+dt, dt)
		y   = nullvalue * np.ones( t.size )
		super().__init__(t, y)



class CyclicalTimeSeries(TimeSeries):
	def __init__(self, t=None, y=None, c=None, cf=None):
		super().__init__(t, y)
		self.c  = []  if c  is None else c   # cycle labels
		self.cf = []  if cf is None else cf  # full-cycle labels (e.g. GRF)
		
	def __repr__(self):
		s   = f'{self.__class__.__name__}\n'
		s  += f'    n       = {self.n}\n'
		s  += f'    hz      = {self.hz}\n'
		s  += f'    durn    = {self.durn}\n'
		s  += f'    ncycles = {self.ncycles}\n'
		return s

	@property
	def max_label(self):
		return 0 if self.isempty else int(max(self.c))
	@property
	def ncycles(self):
		return self.max_label
	@property
	def next_label(self):
		return self.max_label + 1
	
	# def _get_cycle(self, c, registered=False, time_zeroed=False):
	# 	ts  = self.segment( self.c == c )
	# 	if registered:
	# 		ts   = ts.interp_n(101)
	# 		ts.t = np.linspace(0, 101, 101)
	# 	if time_zeroed:
	# 		ts.t  = ts.t - ts.t[0]
	# 	return ts

	def _get_cycle(self, c, registered_n=None, time_zeroed=False, full_cycle=False):
		_c  = self.cf if full_cycle else self.c
		ts  = self.segment( _c == c )
		if registered_n is not None:
			n    = registered_n
			ts   = ts.interp_n(n)
			ts.t = np.linspace(0, n, n)
		if time_zeroed:
			ts.t  = ts.t - ts.t[0]
		return ts
	
	
	def append(self, t, y=None, add_dt=True):
		label   = self.next_label
		n       = super().append(t, y, add_dt)
		c       = [label] * n
		self.c  = np.append(self.c, c)
		self.cf = np.append(self.cf, c)
	
	def append_null(self, nts):
		label   = self.max_label
		super().append(nts, add_dt=True)
		self.c  = np.append(self.c, [0]*nts.n)
		self.cf = np.append(self.cf, [label]*nts.n)

	
	def as_cycle_list(self, registered_n=None):
		return [self._get_cycle(i+1, registered_n=registered_n, time_zeroed=True) for i in range(self.ncycles)]
	
	# def interp_hz(self, hz):
	# 	from scipy import interpolate
	# 	dt     = 1.0 / hz
	# 	ti     = np.arange(self.t0, self.t1, dt)
	# 	fy     = interpolate.interp1d(self.t, self.y)
	# 	fc     = interpolate.interp1d(self.t, self.c)
	# 	fcf    = interpolate.interp1d(self.t, self.cf)
	# 	yi     = fy(ti)
	# 	ci     = np.asarray(np.round( fc(ti) ), dtype=int)
	# 	cfi    = np.asarray(np.round( fcf(ti) ), dtype=int)
	# 	cts    = CyclicalTimeSeries(ti, yi, ci, cfi)
	# 	return cts

	
	def interp_hz(self, hz):
		from scipy import interpolate
		yi,ci,cfi = [], [], []
		for i in range(self.ncycles):
			ts    = self._get_cycle(i+1, registered_n=None, time_zeroed=True, full_cycle=True)
			tsi   = ts.interp_hz(hz)
			yi   += list(tsi.y)
			cfi  += [i+1] * yi.size
			

			n0 = (self.c == (i+1)).sum()
			n1 = (self.cf == (i+1)).sum()
			


		dt     = 1.0 / hz
		ti     = np.arange(self.t0, self.t1, dt)
		fy     = interpolate.interp1d(self.t, self.y)
		fc     = interpolate.interp1d(self.t, self.c)
		fcf    = interpolate.interp1d(self.t, self.cf)
		yi     = fy(ti)
		ci     = np.asarray(np.round( fc(ti) ), dtype=int)
		cfi    = np.asarray(np.round( fcf(ti) ), dtype=int)
		cts    = CyclicalTimeSeries(ti, yi, ci, cfi)
		return cts
	
	
	# def detrend(self, trend):
	# 	trend.fit( self.t, self.y )
	# 	return DetrendedTimeSeries( self.t, self.y, trend )

	def plot_cycles(self, ax=None, registered_n=None, cmap=None, colorbar=False):
		n      = self.ncycles
		if n == 0:
			return
		ax     = plt.gca() if (ax is None) else ax
		cmap   = plt.cm.jet if (cmap is None) else cmap
		colors = cmap( np.linspace(0, 1, n) )
		for i,color in enumerate(colors):
			ts = self._get_cycle(i+1, registered_n=registered_n, time_zeroed=True)
			ts.plot( ax=ax, color=color )
		if colorbar:
			norm   = plt.Normalize(vmin=0, vmax=n)
			sm     = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
			cb     = plt.colorbar(sm, ax=ax)
			cb.set_label('Cycle number')

	def split_at_time(self, t):
		i0            = self.t < t
		i1            = np.logical_not( i0 )
		t0,y0,c0,cf0  = self.t[i0], self.y[i0], self.c[i0], self.cf[i0]
		t1,y1,c1,cf1  = self.t[i1], self.y[i1], self.c[i1], self.cf[i1]
		cts0,cts1     = CyclicalTimeSeries(t0, y0, c0, cf1), CyclicalTimeSeries(t1, y1, c1, cf1)
		return cts0, cts1



class DetrendedTimeSeries(object):
	def __init__(self, t, y, trend):
		self.t     = t
		self.y0    = y
		self.trend = trend
		
	@property
	def y(self):
		return self.y0 - self.yhat

	@property
	def yhat(self):
		return self.trend.get_fitted()

	def plot(self, ax=None):
		ax = plt.gca() if (ax is None) else ax
		ax.plot(self.t, self.y)
		
	def plot_trend(self, ax=None):
		ax = plt.gca() if (ax is None) else ax
		ax.plot(self.t, self.yhat)