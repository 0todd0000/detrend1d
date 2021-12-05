
import numpy as np
from matplotlib import pyplot as plt
import detrend1d



# create and plot single session data:
np.random.seed(1)
J        = 20
mu,sigma = 0, 1
cond     = 0
t0       = 0
t        = np.linspace(t0, t0+1, J)
y        = mu + sigma * np.random.randn(J)
s        = detrend1d.SessionData( t, y, cond )
### plot:
plt.close('all')
plt.figure()
plt.get_current_fig_manager().window.move(0, 0)
ax       = plt.axes()
hm,h     = s.plot(ax=ax, w=0.5, lw=5)
ax.legend([hm,h[0]], ['Session Mean', 'Session Observation'])
plt.tight_layout()
plt.show()




# create and plot single session data (using the "rand" module):
np.random.seed(1)
s0       = detrend1d.rand.session(20, t01=(0,1), mu=0, sigma=1, cond=0)
s1       = detrend1d.rand.session(20, t01=(5,6), mu=3, sigma=1, cond=1)
### plot:
# plt.close('all')
plt.figure()
plt.get_current_fig_manager().window.move(0, 0)
ax       = plt.axes()
hm0,_    = s0.plot(ax=ax, w=0.5, lw=5, color='b')
hm1,_    = s1.plot(ax=ax, w=0.5, lw=5, color='r')
ax.legend([hm0,hm1], ['Session 0 Mean', 'Session 1 Mean'])
plt.show()





# create and plot multi-session data:
np.random.seed(1)
s0       = detrend1d.rand.session(20, t01=(0,1), mu=0, sigma=1, cond=0)
s1       = detrend1d.rand.session(20, t01=(5,6), mu=-2, sigma=1, cond=1)
ms       = detrend1d.MultiSessionData( [s0, s1] )
### plot:
# plt.close('all')
plt.figure()
plt.get_current_fig_manager().window.move(0, 0)
ax       = plt.axes()
hm,h     = ms.plot(ax=ax, w=0.5, lw=5, condcolors=['b', 'r'])
ax.legend(hm, ['Session 0 Mean', 'Session 1 Mean'])
plt.show()





