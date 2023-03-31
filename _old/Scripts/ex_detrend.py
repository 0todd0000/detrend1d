
import os
import numpy as np
import matplotlib.pyplot as plt
import detrend1d as dtr


dvnames    = ['RAnkAng_X', 'RKneeAng_X', 'RHipAng_X',
           'LAnkAng_X', 'LKneeAng_X', 'LHipAng_X',
           'RHipAng_Y', 'RHipAng_Z', 'LHipAng_Y', 'LHipAng_Z',
           'RAnkAng_Y', 'RKneeAng_Y', 'LAnkAng_Y', 'LKneeAng_Y']




def load_data(fpathNPZ, dvname=None):
	with np.load(fpathNPZ) as z:
		cond   = z['cond']
		tsteps = z['tsteps']
		sess   = z['sess']
		tsess  = z['tsess']
		dv     = None if (dvname is None) else z[dvname]
	md         = dtr.Metadata(cond, tsess, tsteps, sess, cond_labels=['A', 'Afa', 'Afo', 'B'])
	return md, dv



# load data:
fpathNPZ   = os.path.join( dtr.dirDATA , 's003.npz' )
md,y       = load_data( fpathNPZ, dvname=dvnames[0] )



# create detrending models and detrend data:
model0     = dtr.models.LinearDriftOverObservationsModel( md, onlyA=True )
model1     = dtr.models.LinearDriftOverTimeModel( md, onlyA=True )
yd0        = model0.detrend( y )
yd1        = model1.detrend( y )
ydd        = yd1 - yd0


# plot:
plt.close('all')
fig,axs     = plt.subplots( 2, 2, figsize=(9,6) )
labels      = 'Original', 'Detrended (Observations)', 'Detrended (Time)', 'Detrended difference'
for ax,yy,ss in zip( axs.ravel() , [y,yd0,yd1,ydd], labels ):
	ax.plot(yy.T, lw=0.2)
	ax.set_title(ss)
plt.tight_layout()
plt.show()