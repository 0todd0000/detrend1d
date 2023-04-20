
from .. import TimeSeries, CyclicalTimeSeries, NullTimeSeries



class RandomCyclicalTimeSeriesGenerator(object):
	def __init__(self, datum, trend, rng, cd=None, icd=None):
		'''
		cd  : cycle duration --- RandomDuration( mean=1, sd=0 )
		icd : intercycle duration --- RandomDuration( mean=0.3, sd=0 )
		'''
		self.cd         = None
		self.cts        = None
		self.datum      = datum
		self.icd        = None
		# self.fullcycle  = False
		self.rng        = rng
		self.trend      = trend
		self._init_durn_models( cd, icd )

	def __init_durn_model(self, x, default=1):
		from .. import RandomDuration
		if x is None:
			model = RandomDuration( default, 0 )
		elif isinstance(x, (int,float)):
			model = RandomDuration( x, 0 )
		elif isinstance(x, RandomDuration):
			model = x
		return model
	
	def _init_durn_models(self, cd, icd):
		self.cd      = self.__init_durn_model( cd,  default=self.datum.durn )
		self.icd     = self.__init_durn_model( icd, default=0 )
		
	@property
	def append_enabled(self):
		return self.cts is not None
	
	def enable_append(self, b=True):
		if b:
			self.cts  = CyclicalTimeSeries()
		else:
			self.cts  = None
	
	def generate_single_cycle(self):
		cdurn   = self.cd.value   # current cycle duration
		icdurn  = self.icd.value  # current inter-cycle duration
		datum   = self.datum if (cdurn == self.datum.durn) else self.datum.interp_durn( cdurn )
		t       = datum.t
		if self.append_enabled and not self.cts.isempty:
			t  += self.cts.t[-1]
		y       = self.trend.apply(t, datum.y) # apply trend
		y      += self.rng.generate( y.size )       # add noise
		ts      = TimeSeries(t, y)
		if self.append_enabled:
			if (icdurn>0) and not self.cts.isempty:
				nts    = NullTimeSeries( icdurn, hz=self.cts.hz )
				self.cts.append_null( nts )
			self.cts.append( ts )
		return ts

	def generate(self, durn=10, hz=100, crop=True):
		self.reset()
		self.enable_append(True)
		self.generate_single_cycle()
		while self.cts.t1 < durn:
			self.generate_single_cycle()
		if hz is not None:
			self.cts   = self.cts.interp_hz( hz )
		if crop:
			self.cts,_ = self.cts.split_at_time( durn )
		return self.cts

	def reset(self):
		self.ts = None




