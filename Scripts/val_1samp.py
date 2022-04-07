
import os
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import spm1d
import detrend1d as dtr
# import singlesubject as ss




# create generator:
n          = 50    # number of observations per session
cond       = [0, 0, 1, 0, 2, 0, 3, 0]   # conditions
# cond       = [1, 2, 0, 0, 3, 0, 0]   # conditions
# cond       = [0, 1, 0, 2, 3, 0, 0]   # conditions
nsess      = len(cond)
mu         = np.linspace(0, 10, nsess)  # true within-session means
# mu         = np.zeros(nsess)  # true within-session means
sigma      = np.ones(nsess)   # within-session SDs
dt         = 0.7     # within-session step duration mean
dts        = 0.01    # within-session step duration SD
sdt        = 360     # between-session duration (mean; start-to-start) (s)
sdts       = 10      # between-session duration (standard deviation) (s)
a          = np.zeros(nsess)  # within-session linear trend (slope)
b          = np.zeros(nsess)  # within-session linear trend (intercept)
exp_model  = dict(n=n, cond=cond, mu=mu, sigma=sigma, dt=dt, dts=dts, sdt=sdt, sdts=sdts, a=a, b=b)
egen       = dtr.rand.ExperimentDatasetGenerator0D( **exp_model )
# t,y,s,c    = egen.generate( as_object=False )
# dset       = egen.generate( as_object=True )
# print( dset.md )


# run simulation:
np.random.seed(10)
niter      = 1000
nrej       = 0
tstat      = []
for i in range(niter):
	dataset  = egen.generate( as_object=True )
	y,md     = dataset.dv, dataset.metadata
	yd = y
	model    = dtr.models.LinearDriftOverTimeModel( md, onlyA=False )
	yd       = model.detrend(y)
	y0,y3    = yd[ md.cond==0 ], yd[ md.cond==3 ]
	mmu      = y0.mean()
	# spmi     = spm1d.stats.ttest( y3-mmu ) #.inference(0.05)
	spmi     = spm1d.stats.ttest2( y3, y0, equal_var=True ) #.inference(0.05)
	# nrej    += int(spmi.h0reject)
	tstat.append( spmi.z )
t          = np.array(tstat)

# survival functions:
heights      = np.linspace(0, 3, 21)
# df           = n-1
df           = 5*n-2
sf           = np.array(  [ (t>h).mean()  for h in heights]  )
sfe          = stats.t.sf(heights, df)



plt.close('all')
ax = plt.axes()
ax.plot(heights, sf, 'o', label='Simulated')
ax.plot(heights, sfe, '-', label='Theoretical')
ax.set_xlabel('$u$', size=20)
ax.set_ylabel('$P (t > u)$', size=20)
ax.legend()
plt.show()








