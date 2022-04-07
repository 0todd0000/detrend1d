
import numpy as np
import matplotlib.pyplot as plt



# class Dataset0D(object):
# 	def __init__(self, t, sess, cond):
# 		self.cond_labels  =


class _RandomNumberGenerator(object):
	
	@staticmethod
	def _generate_time_vector(n, t0, dt, dts):
		dx  = dt + dts * np.random.randn(n-1)
		t   = t0 + np.array( [0] + np.cumsum(dx).tolist() )
		return t

	@staticmethod
	def _asvector(x, n, dtype=float):
		if np.isscalar(x):
			x  = np.asarray( [x]*n , dtype=dtype )
		else:
			x  = np.asarray( x, dtype=dtype )
		return x


class SessionGenerator0D(_RandomNumberGenerator):
	def __init__(self, n=50, mu=20, sigma=1, t0=0, dt=0.7, dts=0.01, a=0.1, b=0):
		self.n        = int( n )           # sample size
		self.mu       = float( mu )        # true mean
		self.sigma    = float( sigma )     # true standard deviation
		self.t0       = float( t0 )        # starting time
		self.dt       = float( dt )        # inter-observation duration (mean)
		self.dts      = float( dts )       # inter-observation duration (standard deviation)
		self.a        = float( a )         # linear trend slope (per second)
		self.b        = float( b )         # linear trend intercept


	def _generate_dv(self, t):
		t     = t - self.t0
		y     = self.a * t + self.b          # linear trend
		t0,t1 = t.min(), t.max()
		t2    = t0 + 0.5 * (t1-t0)
		dy    = self.a * t2 + self.b
		y    -= dy                                     # subtract midpoint
		y    += self.sigma * np.random.randn(self.n)   # linear trend plus noise
		y    += self.mu                                # plus offset
		return y

	# def _generate_time_vector(self, n):
	# 	return
	# 	dt = self.dt['mu'] + self.dt['sigma'] * np.random.randn(n-1)
	# 	t  = np.array( [0] + np.cumsum(dt).tolist() )
	# 	return t
	
	def generate(self, as_object=False):
		t  = self._generate_time_vector(self.n, self.t0, self.dt, self.dts)
		y  = self._generate_dv(t)
		return t,y



class ExperimentDatasetGenerator0D(_RandomNumberGenerator):
	def __init__(self, n=50, cond=[0,0,1,0,2,0,3], mu=20, sigma=1, dt=0.7, dts=0.01, sdt=700, sdts=10,  a=0.1, b=0):
		# experiment-level parameters:
		self.ns       = len(cond)
		self.cond     = self._asvector( cond,  self.ns, int )    # session conditions
		self.sdt      = float( sdt )
		self.sdts     = float( sdts )
		# session-level parameters:
		self.n        = self._asvector( n,     self.ns, int )    # sample size
		self.mu       = self._asvector( mu,    self.ns, float )
		self.sigma    = self._asvector( sigma, self.ns, float )
		self.dt       = self._asvector( dt,    self.ns, float )
		self.dts      = self._asvector( dts,   self.ns, float )
		self.a        = self._asvector( a,     self.ns, float )
		self.b        = self._asvector( b,     self.ns, float )

	def generate(self, as_object=False):
		ts            = self._generate_time_vector(self.ns, 0, self.sdt, self.sdts)
		t,y,s,c       = [], [], [], []
		for i,(n,mu,sigma,t0,dt,dts,a,b,cond) in enumerate(zip(self.n, self.mu, self.sigma, ts, self.dt, self.dts, self.a, self.b, self.cond)):
			smodel    = dict(n=n, mu=mu, sigma=sigma, t0=t0, dt=dt, dts=dts, a=a, b=b)
			sgen      = SessionGenerator0D( **smodel )
			tt,yy     = sgen.generate()
			t.append( tt )
			y.append( yy )
			s.append( [i]*n )
			c.append( [cond]*n )
		t,y,s,c       = [np.hstack(x)  for x in [t,y,s,c]]
		if as_object:
			from . cls import Dataset0D
			from . metadata import Metadata
			# from . import util
			# cond      = util.as_cond_counted( self.cond, asstr=True )
			tsess     = np.array([t[s==ss][0]  for ss in range(self.ns)])
			tsteps    = np.array(t)
			tstepsr   = np.hstack([tsteps[s==i] - t0    for i,t0 in enumerate(tsess)])
			sess      = np.array(s)
			md        = Metadata(self.cond, tsess, tstepsr, sess)
			return Dataset0D( y, md )
		else:
			return t,y,s,c


# class DatasetGenerator0D(_RandomNumberGenerator):
# 	def __init__(self, cond=[0, 0, 1, 0, 2, 0, 3]):   # 0=A, 1=Afa, 2=Afo, 3=B
# 		self.cond        = cond
# 		self.dt_obs      = dict(mu=0.7, sigma=0.01)     # inter-observation duration (seconds) (true mean+SD)
# 		self.dt_sess     = dict(mu=700, sigma=20)       # inter-session (start-to-start) duration (seconds) (true mean+SD)
# 		self.trend_wsess = [dict(a=0, b=0)]*self.nsess  # within-session trends
# 		self.trend_bsess = dict(a=0, b=0)               # between-session trend
# 		self.dmu         = np.zeros( self.nsess )   #[dict(mu=0, sigma=0)]*nsess  # offsets from inter-session trend
# 		self._sgens      = None
# 		self._init_session_generators()
#
#
# 	def _init_session_generators(self):
# 		# create time
# 		t0   = self._generate_time_vector(self.nsess, self.dt_sess)
# 		mus  = self._generate_session_mus()
# 		# self._sgens      = [SessionGenerator0D(mu, sigma, t0=0, dt=self.dt_obs, trend=trend)  for trend in self.trend_wsess]
#
# 		# self._mu_sess = np.zeros( self.nsess )   # true pre-offset means for each session
# 		# self.dmu_sess = np.zeros( self.nsess )   # true mean offsets for each session
# 		# self.sd       = 1                        # SD of observations
#
# 	# def _generate_session_time_vector(self):
# 	# 	mu,s  = self.dt_sess['mu'], self.dt_sess['sigma']
# 	# 	t0    = 0
#
#
# 	@property
# 	def mu(self):
# 		return self._mu + self.dmu
#
# 	@property
# 	def nsess(self):
# 		return len( self.cond )
#
#
# 	# def _generate_observation_times(self):
# 	# 	pass
#
# 	def generate(self, n=5):
# 		y     = np.hstack( [m + self.sd * np.random.randn(n)   for m in self.mu] )
# 		cond  = np.hstack( [[cc]*n   for cc in self.cond] )
# 		t     = np.hstack( [[tt]*n   for tt in np.linspace(0, 1, self.nsess)] )
# 		return t,y,cond
#
# 	def set_condition_order(self, cond):
# 		self.cond  = cond
#
# 	def set_linear_trend(self, scale=1):
# 		self._mu   = scale * np.linspace(0, 1, self.nsess)
#
# 	def set_interobservation_duration(self, x, s=None):
# 		self.durn0   = x
# 		self.durn0sd = 0 if (s is None) else s
#
# 	def set_intersession_duration(self, x, s=None):
# 		self.durn1   = x
# 		self.durn1sd = 0 if (s is None) else s
#
# 	def set_trend_offsets(self, x):
# 		self.dmu   = x
#
# 	def set_sd(self, x):
# 		self.sd   = float(x)
#



#
# class DatasetGenerator0D(object):
# 	def __init__(self):
# 		self.cond     = [0, 0, 1, 0, 2, 0, 3]  # 0=A, 1=Afa, 2=Afo, 3=B
# 		self.durn0    = 0.8   # mean inter-observation duration (seconds)
# 		self.durn1    = 300   # mean inter-session duration (seconds)
# 		self.durn0sd  = 0     # SD of durn0
# 		self.durn1sd  = 0     # SD of durn1
# 		self._mu_sess = np.zeros( self.nsess )   # true pre-offset means for each session
# 		self.dmu_sess = np.zeros( self.nsess )   # true mean offsets for each session
# 		self.sd       = 1                        # SD of observations
#
# 	@property
# 	def mu(self):
# 		return self._mu + self.dmu
#
# 	@property
# 	def nsess(self):
# 		return len( self.cond )
#
# 	def generate(self, n=5):
# 		y     = np.hstack( [m + self.sd * np.random.randn(n)   for m in self.mu] )
# 		cond  = np.hstack( [[cc]*n   for cc in self.cond] )
# 		t     = np.hstack( [[tt]*n   for tt in np.linspace(0, 1, self.nsess)] )
# 		return t,y,cond
#
# 	def set_condition_order(self, cond):
# 		self.cond  = cond
#
# 	def set_linear_trend(self, scale=1):
# 		self._mu   = scale * np.linspace(0, 1, self.nsess)
#
# 	def set_interobservation_duration(self, x, s=None):
# 		self.durn0   = x
# 		self.durn0sd = 0 if (s is None) else s
#
# 	def set_intersession_duration(self, x, s=None):
# 		self.durn1   = x
# 		self.durn1sd = 0 if (s is None) else s
#
# 	def set_trend_offsets(self, x):
# 		self.dmu   = x
#
# 	def set_sd(self, x):
# 		self.sd   = float(x)

