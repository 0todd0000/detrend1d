
import os
import numpy as np
from . ts import TimeSeries

__all__ = ['Datum',
           'DatumNull',
           'DatumPataky2008WalkingVerticalGroundReactionForce',
           'DatumSchwartz2008WalkingKneeFlexion']


class Datum(TimeSeries):
	def set_durn(self, x):
		obj = self.interp_durn(x)
		super().__init__(obj.t, obj.y)

class DatumNull(Datum):
	def __init__(self, t):
		t  = np.asarray(t, dtype=float)
		y  = np.zeros( t.size )
		super().__init__(t=t, y=y)
		
	def set_durn(self, x):
		t  = np.linspace(self.t0, self.t1, x)
		return NullDatum( t )

	
class _ExperimentalDatum( Datum ):
	
	fname     = None
	fullcycle = False
	
	def __init__(self):
		t,y          = np.loadtxt( self.fpath, delimiter=',', skiprows=1 ).T
		super().__init__( t, y )

	@property
	def fpath(self):
		from .. import dirCSV
		return os.path.join( dirCSV, self.fname )



class DatumSchwartz2008WalkingKneeFlexion( _ExperimentalDatum ):
	fname     = 'kneeflex.csv'
	fullcycle = True
	

	
class DatumPataky2008WalkingVerticalGroundReactionForce( _ExperimentalDatum ):
	fname     = 'vgrf.csv'
	fullcycle = False