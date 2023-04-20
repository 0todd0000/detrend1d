
import numpy as np
from . ts import TimeSeries


class NullTimeSeries(TimeSeries):
	def __init__(self, durn, hz, nullvalue=0 ):
		dt  = 1/hz
		t   = np.arange(0, durn+dt, dt)
		y   = nullvalue * np.ones( t.size )
		super().__init__(t, y)
