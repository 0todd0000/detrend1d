
import numpy as np
import matplotlib.pyplot as plt



class Metadata(object):
	
	_cond_labels      = ['A', 'Afa', 'Afo', 'B']
	_cond_colors      = ['0.7', 'b', 'c', 'r']
	
	def __init__(self, cond, tsess, tsteps, sess):
		self.scond    = cond    # (nsess,)  condition integer labels
		self._tsess   = tsess   # (nsess,)  condition starting times
		self._tsteps  = tsteps  # (nsteps,) step times (within-session)
		self._sess    = np.asarray(sess, dtype=int)   # (nsteps,) session integer labels

	def __repr__(self):
		s  = 'Metadata\n'
		s += '    nsess    = %d\n'  %self.nsess
		s += '    nsteps   = %d\n'  %self.nsteps
		s += '\n'
		s += '--Sessions:\n'
		s += '    scondstr  = %s\n'  %str(self.scondstr)
		s += '    scond     = %s\n'  %str(self.scond)
		s += '    snsteps   = %s\n'  %str(self.snsteps)
		s += '    st        = %s\n'  %str(self.st)
		return s

	# ----- main counts -----
	
	@property
	def n(self):   # number of observations
		return self._tsteps.size
	@property
	def nsess(self):   # number of sessions
		return len( self.scond )
	@property
	def nsteps(self):   # number of observations
		return self.n

	# ----- experiment properties -----
	
	@property
	def cond(self):      # (nsteps,) condition integer labels  (reduced labels)
		c  = np.zeros( self.nsteps, dtype=int )
		for ii,cc in enumerate(self.scond):
			c[ self._sess == ii ] = cc 
		return c

	def condstr(self):   # (nsteps,) condition string labels
		return np.hstack( [[s]*n for s,n in zip(self.scondstr,self.snsteps)] )


	# ----- session properties -----

	@property
	def scondstr(self):  # (nsess,) condition string labels by session (non-numbered)
		return [self._cond_labels[i]  for i in self.scond]

	@property
	def sess(self):
		return self._sess

	@property
	def snsteps(self):   # (nsess,) number of observations by session
		return np.array(   [(self._sess==i).sum()  for i in self.scond]   )

	@property
	def st(self):        # (nsess,) session starting times
		return self._tsess



	@property
	def t(self):    # (nsteps,) step times (seconds)
		return self.ts + self._tsteps
	
	@property
	def tr(self):   # (nsteps,) step times relative to session start (seconds)
		return self._tsteps

	@property
	def ts(self):   # (nsteps,) session starting times
		return np.hstack(  [[t]*(self._sess==i).sum()   for i,t in enumerate(self._tsess)]  )


	# ----- methods -----
	
	def plot_session_start_times(self, ax=None):
		ax      = plt.gca() if (ax is None) else ax
		x       = np.arange(self.nsess)
		ax.plot( x, self.st, '-', color='0.7', ms=6 )
		ax.set_xticks( x )
		ax.set_xticklabels( self.scondstr )
		for i,(s,c) in enumerate( zip(self._cond_labels, self._cond_colors) ):
			b   = self.scond == i
			ax.plot( x[b], self.st[b], 'o', ms=9, label=s, color=c)
		# ax.plot( x[i1], self.st[i1], 'o', ms=9, label='B')
		ax.legend()
		ax.set_xlabel('Session')
		ax.set_ylabel('Start time (s)')
		
	def plot_duration_between_session_starts(self, ax=None):
		ax      = plt.gca() if (ax is None) else ax
		x       = np.arange(self.nsess)
		dt      = np.array([np.nan] + np.diff(self.st).tolist()) / 60
		ax.plot( x, dt, '-', color='0.7', ms=6 )
		ax.set_xticks( x )
		ax.set_xticklabels( self.scondstr )
		[ax.plot( xx, ddt, 'o', ms=9, color=self._cond_colors[c])[0]  for xx,ddt,c in zip(x, dt, self.scond)]
		ax.axhline( dt[1:].mean(), color='0.7', ls='--', label='Mean' )
		ax.set_xlim( -0.2, 6.2 )
		ax.legend()
		ax.set_xlabel('Session')
		ax.set_ylabel('Duration between session starts (min)')

	def plot_step_times(self, ax=None):
		ax      = plt.gca() if (ax is None) else ax
		ax.plot( self.ts / 60, color='0.7', label='Session start' )
		ax.plot( self.t / 60, color='b', label='Step' )
		ax.set_xlabel('Step')
		ax.set_ylabel('Time (min)')
		ax.legend()

	def plot_within_session_step_times(self, ax=None):
		ax      = plt.gca() if (ax is None) else ax
		for i,c in enumerate( self._cond_colors ):
			ax.plot( np.diff( self.tr[self.sess==i] ), color=c, lw=0.8 )
			
		# colors  = ['k', 'k', 'k', 'k', '0.7', '0.7', 'r']
		# for i,col in enumerate(colors):
		# 	ax3.plot( np.diff( self.tr[self.cond==i] ), color=col, lw=0.8 )
		ax.set_xlabel('Within-session step')
		ax.set_ylabel('Cycle duration (s)')
		
	
	
	def plot(self):
		fig,axs = plt.subplots(2, 2, figsize=(8,6))
		ax0,ax1,ax2,ax3 = axs.ravel()
		self.plot_session_start_times( ax=ax0 )
		self.plot_step_times( ax=ax1 )
		self.plot_duration_between_session_starts( ax=ax2 )
		self.plot_within_session_step_times( ax=ax3 )
		plt.tight_layout()

