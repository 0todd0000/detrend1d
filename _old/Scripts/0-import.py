
import os
import numpy as np
import matplotlib.pyplot as plt
import detrend1d as dtr


def numbered_condition_labels_to_integers(slist):
	def _hasdigit(s):
		return np.any(  [ss.isdigit() for ss in s]  )
	codes = ['A', 'Afa', 'Afo', 'B']
	slist = [s[0] if _hasdigit(s) else s for s in slist]
	ilist = [codes.index(s)  for s in slist]
	return np.array( ilist, dtype=int )



# set parameters:
dir0       = '/Users/todd/Dropbox/SingleSubject SPM/Raw data/Indiv Data/'  # change this according to your PC
subj       = 3
varnames   = ['RAnkAng_X', 'RKneeAng_X', 'RHipAng_X', 'LAnkAng_X', 'LKneeAng_X', 'LHipAng_X', 'RHipAng_Y', 'RHipAng_Z', 'LHipAng_Y', 'LHipAng_Z', 'RAnkAng_Y', 'RKneeAng_Y', 'LAnkAng_Y', 'LKneeAng_Y']


# load metadata:
fnameMDATA = os.path.join(  dir0, f'TimeDataS{subj}.pickle' )
mdata      = np.load( fnameMDATA, allow_pickle=True )
cond       = mdata['CondOrder']
tsess      = mdata['Time of Sessions (sec)']
tsteps     = mdata['Step Times within sessions']
sess       = mdata['Session labels']


# load data:
fnameDATA  = os.path.join( dir0, 'Data Timing', f'S{subj}_Data.pkl' )
data       = np.load(fnameDATA, allow_pickle=True)


# # ----- TEMPORARAY DATA CHECK ----- 
# # check numbers of trials (for degbugging):
# for i,c in enumerate(cond):
# 	n0     = (sess==i).sum()  # number of trials according to 'Session labels'
# 	n1     = len( data[c]['Angles_Interp'].keys() )  # number of trials according to number of foulee keys
# 	print(c, n0, n1)
# 	if n0!=n1:
# 		raise ValueError( f'Unequal numbers of trials: {n0}, {n1}' )
#

# # # ----- TEMPORARAY DATA CHECK ----- 
# # assemble data for all conditions (single variable) (for degbugging):
# varname    = varnames[1]    # choose one variable from var_names
# nsess      = len(cond)
# n          = [(sess==i).sum()  for i in range(nsess)]  # number of trials per session
# y          = np.vstack([[np.asarray( data[c]['Angles_Interp'][f'Foulee_{i}'][varname] )  for i in range(n)]  for c,n in zip(cond,n)])
# print(y.shape)
# # plot:
# plt.close('all')
# ax = plt.axes()
# ax.plot(y.T)
# plt.show()


# assemble data for all conditions (single variable):
icond        = numbered_condition_labels_to_integers( cond )
sess         = np.asarray(sess, dtype=int)
d            = dict(cond=icond, tsess=tsess, tsteps=tsteps, sess=sess)
nsess        = len(cond)
n            = [(sess==i).sum()  for i in range(nsess)]  # number of trials per session
for vname in varnames:
	y        = np.vstack([[np.asarray( data[c]['Angles_Interp'][f'Foulee_{i}'][vname] )  for i in range(n)]  for c,n in zip(cond,n)])
	d[vname] = y
	print(y.shape)


# save:
fnameNPZ     = os.path.join(dtr.dirDATA, 's%03d.npz'%subj)
np.savez_compressed(fnameNPZ, **d)

