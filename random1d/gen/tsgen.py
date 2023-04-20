




class RandomTimeSeriesGenerator(object):
	def __init__(self, datum, trend, rng):
		self.datum      = datum
		self.trend      = trend
		self.rng        = rng
		
	def generate(self):
		from .. dv import TimeSeries
		t,y0 = self.datum.t, self.datum.y
		y    = self.trend.apply(t, y0)    # apply trend
		y   += self.rng.generate( y.size )  # add noise
		ts   = TimeSeries(t, y)
		ts.set_true_trend( self.trend )
		return ts






