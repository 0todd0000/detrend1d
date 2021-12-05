
import numpy as np
import matplotlib.pyplot as plt



class SessionData(object):
	def __init__(self, t, y, cond):
		self.cond = int( cond )                     # condition label (integer)
		self.t    = None                            # time of individual observations
		self.y    = np.asarray(y, dtype=float)      # dependent variable value
		self._init_t(t)
		
		
		
	def _init_t(self, t):
		if isinstance(t, (int,float) ):
			self.t = t * np.ones(self.J)
		else:
			self.t = np.asarray(t, dtype=float)
		
	@property
	def J(self):
		return self.y.shape[0]
	@property
	def Q(self):
		return self.y.shape[1] if (self.ndim == 1) else None
	@property
	def dim(self):
		return self.y.ndim - 1
	@property
	def t0(self):        # initial time
		return self.t[0]
	@property
	def tminmax(self):
		return self.t.min(), self.t.max()
	@property
	def trange(self):
		return self.t.max() - self.t.min()
	

	def plot(self, ax=None, color='b', w=0.5, ms=3, lw=3):
		h  = self.plot_scatter( ax=ax, color=color, ms=ms )
		hm = self.plot_mean( ax=ax, w=0.5, color=color, lw=lw )[0]
		ax.set_xlabel('Time')
		ax.set_ylabel('Dependent variable value')
		return hm, h
	
	def plot_mean(self, ax=None, w=0.5, **kwdargs):
		ax    = plt.gca() if (ax is None) else ax
		ww    = w * self.trange if (self.trange > 0) else w
		x     = self.t.mean()
		x0,x1 = x - ww/2, x + ww/2
		return ax.plot( [x0,x1], [self.y.mean()]*2, '-', **kwdargs)

	def plot_scatter(self, ax=None, **kwdargs):
		ax  = plt.gca() if (ax is None) else ax
		return ax.plot( self.t, self.y, 'o', **kwdargs)




class MultiSessionData(object):
	def __init__(self, sessions ):
		self.sessions = list( sessions )

	@property
	def J(self):
		return sum(self.JJ)
	@property
	def JJ(self):
		return [s.J for s in self.sessions]



	@property
	def cond(self):
		return np.array([[s.cond]*s.J  for s in self.sessions]).flatten()

	@property
	def dim(self):
		return self.sessions[0].dim
	@property
	def ncond(self):
		return self.ucond.size
	@property
	def nsess(self):
		return len(self.sessions)


	@property
	def sess(self):        # initial time
		return np.array([ [i]*J  for i,J in enumerate(self.JJ) ]).flatten()
	@property
	def t(self):
		return np.array(  [s.t  for s in self.sessions]  ).flatten()
	@property
	def tminmax(self):
		return self.t.min(), self.t.max()


	@property
	def ucond(self):
		return np.unique( self.cond )

	@property
	def y(self):
		if self.dim==0:
			yy = np.array(  [s.y  for s in self.sessions]  ).flatten()
		else:
			yy = np.vstack(  [s.y  for s in self.sessions]  )
		return yy



	def plot(self, ax=None, w=0.5, ms=3, lw=3, condcolors=None):
		condcolors = plt.cm.jet( np.linspace(0, 1, self.ncond) )  if (condcolors is None) else condcolors
		h,hm       = [], []
		for ss in self.sessions:
			cind   = int( np.argwhere( self.ucond==ss.cond ) )
			cc     = condcolors[ cind ]
			hh     = ss.plot_scatter( ax=ax, color=cc, ms=ms )
			hhm    = ss.plot_mean( ax=ax, w=0.5, color=cc, lw=lw )[0]
			h     += hh
			hm.append( hhm )
		ax.set_xlabel('Time')
		ax.set_ylabel('Dependent variable value')
		return hm, h



		
