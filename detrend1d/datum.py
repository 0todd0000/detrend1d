
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from . ts import TimeSeries


class Datum(TimeSeries):
	def set_durn(self, x):
		obj = self.interp_durn(x)
		super().__init__(obj.t, obj.y)

	
class _ExperimentalDatum( Datum ):
	
	fname     = None
	fullcycle = False
	
	def __init__(self):
		self.dirCSV  = os.path.join(  os.path.dirname(__file__), 'csv' )
		t,y          = np.loadtxt( self.fpath, delimiter=',', skiprows=1 ).T
		super().__init__( t, y )

	@property
	def fpath(self):
		return os.path.join( self.dirCSV, self.fname )



class Schwartz2008WalkingKneeFlexionDatum( _ExperimentalDatum ):
	fname     = 'kneeflex.csv'
	fullcycle = True
	

	
class Pataky2008WalkingVerticalGroundReactionForceDatum( _ExperimentalDatum ):
	fname     = 'vgrf.csv'
	fullcycle = False