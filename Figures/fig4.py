
import os,pathlib
import numpy as np
import matplotlib.pyplot as plt
import spm1d
import detrend1d as dtr
plt.rcParams['font.family'] = 'Arial'



def _detrend_cycle_level(t, y, c):
    yd,fit = dtr.detrend_cycle_level(t, y, c, trend='linear')
    yr     = fit.get_detrended_registered()
    yr     = yr + fit.yr.mean() - yr.mean()
    return yr

def _detrend_trial_level(t, y, c):
    yd,fit = dtr.detrend_trial_level(t, y, trend='linear')
    yd     = np.array(   [dtr.reg.interp_n(yd[c==u], 101)   for u in np.unique(c)]   )
    yd     = yd + y.mean() - yd.mean()
    return yd

def _get_registered(t, y, c):
    yd,fit = dtr.detrend_cycle_level(t, y, c, trend='linear')
    return fit.yr

def _remove_noncycles(t, y, c):
    i      = c>0
    return t[i],y[i],c[i]




# load data:
dirREPO  = pathlib.Path( os.path.dirname(__file__) ).parent
fpath0   = os.path.join(dirREPO, 'Data', 'Fukuchi2018', 'ex_processing0.csv')
fpath1   = os.path.join(dirREPO, 'Data', 'Fukuchi2018', 'ex_processing1.csv')
c0,y0    = np.loadtxt(fpath0, delimiter=',', skiprows=1).T
c1,y1    = np.loadtxt(fpath1, delimiter=',', skiprows=1).T



# process:
hz             = 300
t0,t1          = np.arange(y0.shape[0])/hz, np.arange(y1.shape[0])/hz

_t0,_y0,_c0    = _remove_noncycles(t0, y0, c0)
_t1,_y1,_c1    = _remove_noncycles(t1, y1, c1)
yd0,fit0       = dtr.detrend_trial_level(_t0, _y0, trend='linear')
yd,fit         = dtr.detrend_cycle_level(_t0, _y0, _c0, trend='linear')

y0r,y1r        = _get_registered(_t0, _y0, _c0), _get_registered(_t1, _y1, _c1)
y0i,y1i        = _detrend_trial_level(_t0, _y0, _c0), _detrend_trial_level(_t1, _y1, _c1)
y0I,y1I        = _detrend_cycle_level(_t0, _y0, _c0), _detrend_cycle_level(_t1, _y1, _c1)#

n              = 10  # analyze only first 10 cycles
y0r,y1r        = y0r[:n],y1r[:n]
y0i,y1i        = y0i[:n],y1i[:n]
y0I,y1I        = y0I[:n],y1I[:n]



# stats:
spm1           = spm1d.stats.ttest2(y1i, y0i).inference(0.05)
spm2           = spm1d.stats.ttest2(y1I, y0I).inference(0.05)






# plot:

plt.close('all')
fig       = plt.figure( figsize=(8,13) )
axx,axy   = [0.11, 0.565], [0.81] + list(np.linspace(0.58, 0.035, 4))
axw,axh   = 0.42, 0.17
axs       = np.array([[plt.axes([xx,yy,axw,axh])  for xx in axx]  for yy in axy])


ax  = axs[0,0]
h0 = ax.plot(t0, y0, color='0.7')[0]
h1 = ax.plot(fit0.t, fit0.yhat, 'k--', lw=3)[0]
ax.legend([h0,h1], ['Data', 'Trend'], loc='center' )
axs[0,0].set_ylabel('Vertical GRF (N)')



ax = axs[0,1]
h0 = ax.plot(t0, y0, color='0.7')[0]

inds = [fit.beta[0].argmax(), fit.beta[0].argmin()]
inds = [fit.beta[1].argmax(), fit.beta[1].argmin()]
for ind in inds:
    _y = fit.ym[ind] + fit.yhatr[:,ind]
    h1 = ax.plot(fit.tr[:,ind], _y, '--', color='k', lw=3)[0]
    h2 = ax.axhline(_y[0], color='k', ls=':')
ax.axhline(0, color='k', ls=':')
ax.legend([h0,h1,h2], ['Data', 'Trend','Reference'], loc='lower left' )

[ax.set_xlabel('Time  (s)')  for ax in axs[0]]



ax  = axs[1,0]
b,a = fit0.beta
ax.axhline( a, color='k', lw=5 )


ax  = axs[1,1]
b,a = fit.beta
ax.plot( a, color='k', lw=5 )
ax.axhline(0, color='k', ls=':')




axs[1,0].set_ylabel('Slope  (N/s)')
plt.setp(axs[1], xlim=(0,100), ylim=(-2.4,2.4))



axs[2,0].plot(y0i.T, '0.7')
axs[2,1].plot(y0I.T, '0.7')
# axs[2,0].set_ylabel('Detrended')
axs[2,0].set_ylabel('Vertical GRF (N)')
plt.setp(axs[2], xlim=(0,100))



ax = axs[3,0]
h0 = ax.plot(y0i.T, '0.7', lw=1)[0]
h1 = ax.plot(y1i.T, 'k', lw=1, ls='--')[0]
ax.legend([h0,h1],['Speed 1', 'Speed 2'])
axs[3,0].set_ylabel('Vertical GRF (N)')



ax = axs[3,1]
h0 = ax.plot(y0I.T, '0.7', lw=1)[0]
h1 = ax.plot(y1I.T, 'k', lw=1, ls='--')[0]
ax.legend([h0,h1],['Speed 1', 'Speed 2'])
plt.setp(axs[3], xlim=(0,100))




spm1.plot( ax=axs[4,0] )
spm2.plot( ax=axs[4,1] )
plt.setp(axs[4], ylim=(-4.3, 4.3))
axs[4,0].set_ylabel('t-value', size=12)
axs[4,0].text(50, 3, r'$p > 0.05$')
axs[4,0].text(50, 3.8, r'$p < 0.05$')
axs[4,0].text(22, -3.5, r'$p > 0.05$')
axs[4,0].text(22, -4.2, r'$p < 0.05$')
[ax.set_xlabel('Stance time  (%)')  for ax in axs[4]]


clabels = 'Trial-level detrending', 'Cycle-level detrending'
rlabels = 'Filtered data', 'Estimated trends', 'Detrended', 'Detrended (two speeds)', 'Two-speed comparison'
[ax.set_title(s, size=14)  for ax,s in zip(axs[0], clabels)]
[ax.text(-0.25, 0.5, s, size=14, rotation=90, color='0.2', va='center', transform=ax.transAxes)  for ax,s in zip(axs[:,0], rlabels)]

[ax.set_ylim(-20, 780)  for ax in axs[[0,2,3]].ravel()]
[ax.set_xticklabels([])  for ax in axs[1:4].ravel()]
[ax.set_yticklabels([])  for ax in axs[:,1]]
[ax.set_ylabel(None)  for ax in axs[:,1]]


[ax.text(0.02, 0.94, f'({chr(97+i)})', transform=ax.transAxes) for i,ax in enumerate(axs.ravel())]


plt.show()


# save:
plt.savefig( os.path.join(os.path.dirname(__file__), 'pdf', 'fig4.pdf') )