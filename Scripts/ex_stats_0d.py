
import numpy as np
from matplotlib import pyplot as plt
import spm1d
import detrend1d


# create and model multi-session data (multiple models):
np.random.seed(1)
J0,J1,J2 = 20, 20, 20
s0       = detrend1d.rand.session(J0, t01=(0,1), mu=0, sigma=1, cond=0)
s1       = detrend1d.rand.session(J1, t01=(5,6), mu=-2, sigma=1, cond=1)
s2       = detrend1d.rand.session(J2, t01=(8,9), mu=-3, sigma=1, cond=1)
ms       = detrend1d.MultiSessionData( [s0, s1, s2] )
model0   = detrend1d.Model( ms, deg=0 )
model1   = detrend1d.Model( ms, deg=1 )
model2   = detrend1d.Model( ms, deg=2 )
X0       = model0.get_design_matrix()
X1       = model1.get_design_matrix()
X2       = model2.get_design_matrix()
### stats:
alpha    = 0.05
y        = np.array([ms.y]).T
c0       = [-1, 1]
c1       = [0, -1, 1]
c2       = [0, -1, 1]
spm0     = spm1d.stats.glm(y, X0, c0).inference( alpha )
spm1     = spm1d.stats.glm(y, X1, c1).inference( alpha )
spm2     = spm1d.stats.glm(y, X2, c2).inference( alpha )

print( 't = %.3f, p = %.3f' %(spm0.z, spm0.p) )
print( 't = %.3f, p = %.3f' %(spm1.z, spm1.p) )
print( 't = %.3f, p = %.3f' %(spm2.z, spm2.p) )








# ### plot:
# plt.close('all')
# fig,AX = plt.subplots( 2, 2, figsize=(8,6) )
# plt.get_current_fig_manager().window.move(0, 0)
# ax0,ax1,ax2,ax3 = AX.flatten()
# ### plot trends:
# ms.plot(ax=ax0, w=0.5, lw=5, condcolors=['b', 'r'])
# h0       = model0.plot( ax=ax0, color='k', lw=2, zorder=-1)
# h1       = model1.plot( ax=ax0, color='c', lw=2, zorder=-1)
# h2       = model2.plot( ax=ax0, color='g', lw=2, zorder=-1)
# ax0.legend([h0,h1,h2], ['Model 0', 'Model 1', 'Model 2'])
# ### plot detrended data:
# msd0     = model0.get_detrended_multisessiondata()
# msd1     = model1.get_detrended_multisessiondata()
# msd2     = model2.get_detrended_multisessiondata()
# msd0.plot(ax=ax1, w=0.5, lw=5, condcolors=['b', 'r'])
# msd1.plot(ax=ax2, w=0.5, lw=5, condcolors=['b', 'r'])
# msd2.plot(ax=ax3, w=0.5, lw=5, condcolors=['b', 'r'])
# ax0.set_title('Original data')
# [ax.set_title(f'Detrended data (Model {i})')   for i,ax in enumerate([ax1,ax2,ax3])]
# [ax.axhline(0, color='k', ls=':')   for ax in [ax1,ax2,ax3]]
# plt.tight_layout()
# plt.show()








# , trendline=dict(deg=1, color='c', lw=2)








# X = e.get_design_matrix(detrend=False, deg=1)




#
#
# # Case 1:  true trend, no true condition effect
# np.random.seed(1)
# J      = 50
# mu     = 2 * np.array([0, -1.3, -2.8, -3.3])
# y      = np.array([muu + np.random.randn(J)   for muu in mu])
# cond   = np.array([[0, 1, 0, 1]] * J).T
# q      = np.array(  [np.linspace(0, 1, 4).tolist()]*J ).T
# spm0   = run_test(q, y, cond, detrend=False)
# spm1   = run_test(q, y, cond, detrend=True)
# print(spm0.p, spm1.p)
#
#
#
#
# plt.close('all')
# fig,AX = plt.subplots( 2, 2, figsize=(8,6) )
# plt.get_current_fig_manager().window.move(0, 0)
# ax0,ax1,ax2,ax3 = AX.flatten()
# colors = 'b', 'r'
# for qq,yy,cn in zip(q, y, cond[:,0]):
# 	cc = colors[ cn ]
# 	ax0.plot(qq, yy, 'o', color=cc, ms=3)
# 	ax0.plot(qq[0], yy.mean(), 'o', color=cc, ms=8, zorder=10)
#
# # ax0.plot( q[:,1], y.mean(axis=1), 'co')
# plot_trendline(q.flatten(), y.flatten(), ax=ax0)
#
# ax0.axhline( y[cond==0].mean(), color=colors[0] )
# ax0.axhline( y[cond==1].mean(), color=colors[1] )
#
# ax0.set_xticks(q[:,1])
# ax0.set_xticklabels([f'Sess{s}'  for s in [1,2,3,4]])
# plt.tight_layout()
# plt.show()







# plt.savefig(  os.path.join(dir0, 'Figures', 'fig_stats.pdf')  )

