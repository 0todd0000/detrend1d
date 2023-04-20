
import numpy as np
from matplotlib import pyplot as plt
from . ts import TimeSeries
from .. util import around


class CyclicalTimeSeries(TimeSeries):
	def __init__(self, t=None, y=None, c=None, cf=None):
		super().__init__(t, y)
		self.c  = []  if c  is None else np.asarray(c)   # cycle labels
		self.cf = []  if cf is None else np.asarray(cf)  # full-cycle labels (e.g. GRF)
		
	def __repr__(self):
		s   = f'{self.__class__.__name__}\n'
		s  += f'    n       = {self.n}\n'
		s  += f'    hz      = {self.hz}\n'
		s  += f'    durn    = {self.durn}\n'
		s  += f'    ncycles = {self.ncycles}\n'
		return s

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
	
	def as_timeseries(self):
		return TimeSeries(self.t, self.y)
	
	def interp_hz(self, hz):
		from scipy import interpolate
		from scipy.ndimage import label
		dt     = 1.0 / hz
		ti     = np.arange(self.t0, self.t1, dt)
		yi     = interpolate.interp1d(self.t, self.y)(ti)
		cfi    = interpolate.interp1d(self.t, self.cf)(ti)
		cfi    = np.asarray(np.round(cfi), dtype=int)
		if self.hasnull:
			bi = interpolate.interp1d(self.t, self.c>0)(ti)
			ci = label( bi )[0]
		else:
			ci = cfi
		return CyclicalTimeSeries(ti, yi, ci, cfi)

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
		cts0,cts1     = CyclicalTimeSeries(t0, y0, c0, cf0), CyclicalTimeSeries(t1, y1, c1, cf1)
		return cts0, cts1



	def write_csv(self, fpath, prec=None):
		t     = around(self.t, prec)
		y     = around(self.y, prec)
		c     = self.c
		cf    = self.cf
		if self._trend.iscompound:
			yh0,yh1 = around( self._trend.asarray(t, c), prec )
			with open(fpath, 'w') as f:
				f.write('t,y,c,cf,trend_inter,trend_intra\n')
				for tt,yy,cc,ccf,yyh0,yyh1 in zip(t, y, c, cf, yh0, yh1):
					f.write( f'{tt},{yy},{cc},{ccf},{yyh0},{yyh1}\n' )
		else:
			yhat   = around( self._trend.asarray(t, c), prec )
			tlabel = self._trend.label
			with open(fpath, 'w') as f:
				f.write( f't,y,c,cf,{tlabel}\n')
				for tt,yy,cc,ccf,yyh in zip(t, y, c, cf, yhat):
					f.write( f'{tt},{yy},{cc},{ccf},{yyh}\n' )
				
				