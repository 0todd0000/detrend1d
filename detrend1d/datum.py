
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from rft1d import randn1d



class Datum(object):
	def __init__(self, t, y):
		self.t               = t
		self.y               = y

	def plot(self, ax=None):
		ax = plt.gca() if (ax is None) else ax
		ax.plot(self.t, self.y)

	
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