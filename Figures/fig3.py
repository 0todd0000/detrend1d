
import os,pathlib
import numpy as np
import matplotlib.pyplot as plt
import detrend1d as dtr
plt.rcParams['font.family'] = 'Arial'


def _butter(data, cutoff, hz, order=5, padtype=None, padlen=None, btype='lowpass'):
    from scipy.signal import butter, filtfilt
    nyq  = 0.5 * hz
    cut  = cutoff / nyq
    b,a  = butter(order, cut, btype=btype)
    y    = np.asarray(data)
    if y.ndim==1:
        y    = filtfilt(b, a, y, padtype=padtype, padlen=padlen)
    else:
        y    = np.array([filtfilt(b, a, yy, padtype=padtype, padlen=padlen)   for yy in y.T]).T
    return y	


def _segment_single(y, b):
    nframes = y.shape[0]
    i0,i1   = np.argwhere( b ).ravel()[[0,-1]]
    # walk-back to start
    ii    = i0
    while (ii>=0) and (y[ii-1] < y[ii]):
        ii -= 1
    if i0==0:
        return None,None
    # walk-forward to end
    ii    = i1
    while (i1<nframes-1) and (y[ii+1] < y[ii]):
        ii += 1
    if i1>=nframes-1:
        return None,None
    return i0, i1
	

def _segment(f, fs, th=50):
    from scipy.ndimage import label
    fy,fys  = f[:,1], fs[:,1]
    L,n     = label( fys > th )
    c       = np.zeros( f.shape[0], dtype=int )
    ind     = []
    cn      = 0
    for i in range(n):
        b     = L==(i+1)
        i0,i1 = _segment_single( fy, b )
        if i0 is not None:
            cn += 1
            c[i0:i1+1] = cn
            ind.append( (i0,i1) )
    return c, np.array(ind)


def _process(y, hz=300, cutoff=20, th=30):
    t       = np.arange( y.shape[0] ) / hz
    ys      = _butter(y, cutoff, hz)
    c,ind   = _segment( y, ys, th=th )
    return t,ys,c
	
	

# load data:
dirREPO  = pathlib.Path( os.path.dirname(__file__) ).parent
speed    = 5
fpath    = os.path.join(dirREPO, 'Data', 'Fukuchi2018', f'WBDS04walkT{speed:02}grf.txt')
a       = np.loadtxt(fpath, delimiter='\t', skiprows=1)


# extract left-foot GRF and process:
grf     = a[:,[1,2,3]]  # left foot GRF
hz      = 300           # sampling rate
t,y,c   = _process( grf, hz=hz, cutoff=20, th=30 )  # see processing function details above
y       = y[:,[0,1]]


# plot:
plt.close('all')
fig,axs = plt.subplots( 1, 2, figsize=(7,3), tight_layout=True )
colors  = 'k', '0.6'

axs[0].plot(t, grf[:,0], color=colors[0], zorder=1, lw=2)
axs[0].plot(t, grf[:,1], color=colors[1], zorder=0)

for i in range(c.max()):
	yy = y[c==(i+1)]
	tt = np.arange( yy.shape[0] ) / hz
	axs[1].plot(tt, yy[:,0], color=colors[0], zorder=1, lw=0.5)
	axs[1].plot(tt, yy[:,1], color=colors[1], zorder=0, lw=0.5)

axs[1].axhline(0, color='k', ls=':')
axs[1].set_yticklabels([])

[ax.set_xlabel('Time (s)', size=11)  for ax in axs]
axs[0].set_ylabel('GRF (N)', size=11)
axs[0].legend(['Anterioposterior', 'Vertical'])
labels = 'Original Data', 'Processed (smoothed & segmented)'
[ax.text(0.03, 0.93, f'({chr(97+i)}) {s}', transform=ax.transAxes, size=11)  for i,(ax,s) in enumerate(zip(axs,labels))]
plt.setp(axs, ylim=(-150,850))
plt.show()







# # save:
# plt.savefig( os.path.join(os.path.dirname(__file__), 'pdf', 'fig3.pdf') )