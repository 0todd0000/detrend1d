
import os,pathlib
import numpy as np
import matplotlib.pyplot as plt
import detrend1d as dtr


# set parameters:
subj       = 1
varnames   = ['RAnkAng_X', 'RKneeAng_X', 'RHipAng_X', 'LAnkAng_X', 'LKneeAng_X', 'LHipAng_X', 'RHipAng_Y', 'RHipAng_Z', 'LHipAng_Y', 'LHipAng_Z', 'RAnkAng_Y', 'RKneeAng_Y', 'LAnkAng_Y', 'LKneeAng_Y']
varname    = varnames[1]
fnameNPZ   = os.path.join(dtr.dirDATA, f's{subj:03}.npz')
with np.load(fnameNPZ) as z:
	cond   = z['cond']
	tsess  = z['tsess']
	tsteps = z['tsteps']
	sess   = z['sess']
	y      = z[varname]


md    = dtr.Metadata(cond, tsess, tsteps, sess)
print( md )


plt.close('all')
md.plot()
dir1 = os.path.dirname(__file__)
plt.show()
# plt.savefig( os.path.join( dir1, 'Figures', f's{subj}_metadata.pdf'  ) )
