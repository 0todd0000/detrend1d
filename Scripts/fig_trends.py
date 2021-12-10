
import numpy as np
from matplotlib import pyplot as plt
import spm1d
import detrend1d



def create_dataset(seed=0, mu=[0,0,0,0], cond=[0,0,1,1,], J=20):
	np.random.seed(seed)
	t0     = [0, 3, 6, 9]     # starting times (min)
	d      = [1, 1, 1, 1]     # session durations
	sess   = []
	for tt0,dd,condd,muu in zip( t0, d, cond, mu ):
		t  = np.linspace(tt0, tt0+dd, J)
		y  = muu + np.random.randn(J)
		s  = detrend1d.SessionData( t, y, condd )
		sess.append( s )
	return detrend1d.MultiSessionData( sess )


ms0    = create_dataset( seed=0, mu=[0,0,-2,-2] )
ms1    = create_dataset( seed=16, mu=[0,0,0,0.1], cond=[0,0,0,1] )






plt.close('all')
fig,AX = plt.subplots( 1, 2, figsize=(8,3) )
plt.get_current_fig_manager().window.move(0, 0)
ax0,ax1 = AX.flatten()
colors   = 'b', 'r'
# labels   = ['TIME=No, Yes COND=yes']

# hm,h     = ms0.plot(ax=ax0, w=0.5, lw=5, ms=1, condcolors=colors)
# model    = detrend1d.Model( ms0, deg=1 )
# model.plot( ax=ax0, color='k' )
# ax0.legend([hm[0], hm[2]], ['Cond A Mean', 'Cond B Mean'])




for ax,ms in zip(AX.ravel(), [ms0,ms1]):
	hm,h     = ms.plot(ax=ax, w=0.5, lw=5, ms=1, condcolors=colors)
	model    = detrend1d.Model( ms, deg=1 )
	model.plot( ax=ax, color='k' )
	if ax==ax0:
		ax.legend([hm[0], hm[2]], ['Cond A Mean', 'Cond B Mean'])
plt.tight_layout()
plt.show()



















# ### plot:
# plt.close('all')
# plt.get_current_fig_manager().window.move(0, 0)
# ax       = plt.axes()
# hm,h     = ms.plot(ax=ax, w=0.5, lw=5, condcolors=['b', 'r'])
# ax.legend([hm[0], hm[2]], ['Cond A Mean', 'Cond B Mean'])
# plt.show()



# spmA0  = run_test(yA, cond, detrend=False)
# spmA1  = run_test(yA, cond, detrend=True)
# print(spmA0.p, spmA1.p)
#
#
#
#
# # Case 2:  no true trend, true condition effect
# np.random.seed(1)
# mu     = [0]*2 + [-1.5]*2
# yB     = np.array([muu + np.random.randn(J)   for muu in mu])
# spmB0  = run_test(yB, cond, detrend=False)
# spmB1  = run_test(yB, cond, detrend=True)
# print(spmB0.p, spmB1.p)






# plt.close('all')
# fig,AX = plt.subplots( 2, 2, figsize=(8,6) )
# plt.get_current_fig_manager().window.move(0, 0)
# ax0,ax1,ax2,ax3 = AX.flatten()
# colors = 'b', 'b', 'r', 'r'
# for qq,yy,cc in zip(q, yA, colors):
# 	ax0.plot([qq]*J, yy, 'o', color=cc)
# # for qq,yy,cc in zip(q, yB, colors):
# # 	ax1.plot([qq]*J, yy, 'o', color=cc)
# # ax0.set_xticks(q)
# # ax0.set_xticklabels([f'Sess{s}'  for s in [1,2,3,4]])
# plt.tight_layout()
# plt.show()







# plt.savefig(  os.path.join(dir0, 'Figures', 'fig_stats.pdf')  )


