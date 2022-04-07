
import os
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import spm1d
import detrend1d as dtr




# create generator:
np.random.seed(0)
n          = 150    # number of observations per session
cond       = [0, 0, 1, 0, 2, 0, 3, 0]   # conditions
nsess      = len(cond)
# mu         = np.linspace(20, 25, 7)  + [0,0,0,0,0,0,0]# within-session means
mu         = np.zeros(nsess)  # true within-session means
sigma      = np.ones(nsess)   # within-session SDs
dt         = 0.7     # within-session step duration mean
dts        = 0.01    # within-session step duration SD
sdt        = 9 * 60  # between-session duration (mean; start-to-start) (s)
sdts       = 10      # between-session duration (standard deviation) (s)
a          = np.zeros(nsess)  # within-session linear trend (slope)
b          = np.zeros(nsess)  # within-session linear trend (intercept)
exp_model  = dict(n=n, cond=cond, mu=mu, sigma=sigma, dt=dt, dts=dts, sdt=sdt, sdts=sdts, a=a, b=b)
egen       = dtr.rand.ExperimentDatasetGenerator0D( **exp_model )
# t,y,s,c    = egen.generate( as_object=False )
dset       = egen.generate( as_object=True )
print( dset.md )



# plt.close('all')
# plt.figure()
# plt.get_current_fig_manager().window.move(0, 0)
# dset.plot()
# plt.show()
#

md = dset.md

plt.close('all')
plt.figure()
plt.get_current_fig_manager().window.move(0, 0)
dset.md.plot()
plt.show()


