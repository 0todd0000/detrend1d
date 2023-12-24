
import os,pathlib
import numpy as np
import matplotlib.pyplot as plt
import detrend1d as dtr
plt.rcParams['font.family'] = 'Arial'



# load data:
dirREPO  = pathlib.Path( os.path.dirname(__file__) ).parent
fpath    = os.path.join(dirREPO, 'Data', 'knee_flexion.csv')
t,y,c    = np.loadtxt(fpath, delimiter=',', skiprows=1).T
yd0,fit0 = dtr.detrend(t, y, trend='linear', mean_corrected=True)
yd,fit   = dtr.detrend_cycle_level(t, y, c, trend='linear')
ncycles  = int( c.max() )
cmap     = plt.cm.binary
colors   = cmap( np.linspace(0, 1, ncycles+2) )[2:]



# plot:
plt.close('all')
fig,axs     = plt.subplots( 2, 2, figsize=(10,8), tight_layout=True )
ax0,ax1,ax2,ax3 = axs.ravel()

h0     = ax0.plot(t, y, '-', color='0.5', label='Data')[0]
inds   = [fit.z.argmax(), fit.z.argmin()]
for ind in inds:
    h1 = ax0.plot(fit.tr[:,ind], fit.ym[ind] + fit.yhatr[:,ind], 'o-', color='0.0', label='Trend')[0]
ax0.legend([h0,h1], ['Data', 'Trend'], loc='lower left')

b,a    = fit.beta
ax1.plot( a, color='k', lw=5, label='Slope (deg/s)' )
ax1.plot( b, color='0.6', lw=1, label='Intercept (deg)' )
ax1.legend()


for i,color in enumerate(colors):
    tt,yyd0,yyd = t[c==(i+1)], yd0[c==(i+1)], yd[c==(i+1)]
    yyd0r,yydr = [dtr.reg.interp_n(x, 101)  for x in (yyd0,yyd)]
    ax2.plot(yyd0r, color=color)
    ax3.plot(yydr, color=color)

# add colorbar
norm   = plt.Normalize(vmin=0, vmax=ncycles)
sm     = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
cax    = plt.axes([0.15,0.11, 0.26, 0.02])
cb     = plt.colorbar(sm, ax=ax1, cax=cax, orientation='horizontal')
cax.text(0.1, 0.25, 'Cycle number', color='k', size=9)
plt.setp(cax.get_xticklabels(), size=7)


labels = 'Cycle points from panel (a)', None
for ax in [ax1,ax2,ax3]:
    for ind,label in zip(inds,labels):
        ax.axvline(ind, color='k', ls='--', label=label)
ax1.legend()

[ax.axhline(0, color='k', ls=':')  for ax in axs.ravel()]

[ax.set_xlabel(s, size=12)  for ax,s in zip(axs.ravel(), ['Time (s)'] + ['Cycle time (%)']*3) ]
[ax.set_ylabel('Simulated knee flexion angle (deg)', size=12)  for ax in [ax0,ax2,ax3]]
ax1.set_ylabel('Fitted parameter value')
labels = 'Dataset with cycle-level trend', 'Fitted parameters', 'Detrended (trial-level)', 'Detrended (cycle-level)'
[ax.text(0.03, 0.93, f'({chr(97+i)}) {s}', transform=ax.transAxes, size=11, bbox=dict(color='w'))  for i,(ax,s) in enumerate(zip(axs.ravel(),labels))]
plt.setp([ax0,ax2,ax3], ylim=(-20, 80))
ax1.set_ylim(-9, 9)
plt.show()







# # save:
# plt.savefig( os.path.join(os.path.dirname(__file__), 'pdf', 'fig2.pdf') )