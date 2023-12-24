
import os
import numpy as np
import matplotlib.pyplot as plt
import detrend1d as dtr
plt.rcParams['font.family'] = 'Arial'




# create dataset:
np.random.seed(1)
n       = 101
t       = np.linspace(0, 30, n) # time
y_orig  = np.random.randn( n )  # original (random) dataset
b0,b1   = 0, 0.234             # intercept, slope
y_trend = b0 + b1*t            # true trend
y       = y_orig + y_trend     # observed data
yd,fit  = dtr.detrend(t, y, trend='linear')



# plot:
plt.close('all')
fig,axs  = plt.subplots(1, 2, figsize=(8,3), tight_layout=True)
ax0,ax1  = axs
c0,c1    = '0.4', '0.0'

ax0.plot(t, y, lw=2, color=c0, label='Observed data')
fit.plot(ax=ax0, color=c1, lw=5, ls='-', label='Estimated linear trend')
ax0.axhline(0, color='k', ls=':')
ax0.legend( loc='upper right', fontsize=9, bbox_to_anchor=(0.99, 0.45) )

ax1.plot(t, yd, ls='-', lw=2, color=c0, label='Detrended data')
ax1.axhline(0, color='k', ls=':')

[ax.set_xlabel('Time (s)', size=11)  for ax in axs]
ax0.set_ylabel('Dependent variable value', size=11)

labels = '(a) Example data with a linear trend', '(b) Detrended'
[ax.text(0.03, 0.92, s, size=11, transform=ax.transAxes) for ax,s in zip(axs, labels)]

plt.show()



# save:
plt.savefig( os.path.join(os.path.dirname(__file__), 'pdf', 'fig1.pdf') )