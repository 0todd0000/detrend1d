

import numpy as np
import matplotlib.pyplot as plt
from . ts import TimeSeries




class CyclicalTimeSeries(TimeSeries):
	def __init__(self, t=None, y=None, c=None):
		super().__init__(t, y)
		self.c  = np.asarray(c, dtype=int)   # cycle labels
		self.cf = None
		self._init_cf()
		
	def __repr__(self):
		s   = f'{self.__class__.__name__}\n'
		s  += f'    n       = {self.n}\n'
		s  += f'    hz      = {self.hz}\n'
		s  += f'    durn    = {self.durn}\n'
		s  += f'    ncycles = {self.ncycles}\n'
		return s

	def _init_cf(self):
		cf      = self.c.copy()
		if 0 in self.c:
			from scipy.ndimage import label
			b      = self.c==0
			L,n    = label(b)
			L      = L-1 if (self.c[0]==0) else L
			cf     = self.c.copy()
			cf[b]  = L[b]
		self.cf = cf

	@property
	def hasnull(self):
		return not np.all( self.c==self.cf )
	@property
	def max_label(self):
		return 0 if self.isempty else int(max(self.c))
	@property
	def ncycles(self):
		return self.max_label
	@property
	def next_label(self):
		return self.max_label + 1
	
	def _get_cycle(self, c, registered_n=None, time_zeroed=False, full_cycle=False, as_timeseries=True):
		_c  = self.cf if full_cycle else self.c
		ts  = self.segment( _c == c, as_timeseries=as_timeseries )
		if registered_n is not None:
			n    = registered_n
			ts   = ts.interp_n(n)
			# ts.t = np.linspace(0, n, n)
		if time_zeroed:
			ts.t  = ts.t - ts.t[0]
		return ts
	
	
	def as_cycle_list(self, registered_n=None):
		return [self._get_cycle(i+1, registered_n=registered_n, time_zeroed=True) for i in range(self.ncycles)]
	
	def as_registered_arrays(self, n=101):
		t,y  = [],[]
		for i in range(self.ncycles):
			ts = self._get_cycle(i+1, registered_n=n, time_zeroed=False)
			t.append( ts.t )
			y.append( ts.y )
		return np.vstack(t), np.vstack(y)

	def as_registered_cyclicaltimeseries(self, n=101):
		t,y,c  = [],[],[]
		for i in range(self.ncycles):
			ts = self._get_cycle(i+1, registered_n=n, time_zeroed=False)
			t.append( ts.t )
			y.append( ts.y )
			c.append( [i+1]*ts.t.size )
		return CyclicalTimeSeries( np.hstack(t), np.hstack(y), np.hstack(c) )

	def as_timeseries(self):
		return TimeSeries(self.t, self.y)
	

	
	def detrend(self, trend):
		pass
		# from . dts import DetrendedCyclicalTimeSeries
		# trend.fit( self.t, self.y )
		# return DetrendedTimeSeries( self.t, self.y, trend )

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


	def segment(self, b, as_timeseries=True):
		t,y   = self.t[b], self.y[b]
		ts    = TimeSeries(t, y)
		if not as_timeseries:
			ts.__class__ = self.__class__
		return ts

