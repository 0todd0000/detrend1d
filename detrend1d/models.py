
import numpy as np
import matplotlib.pyplot as plt
import spm1d








class _Model(object):
	
	def __init__(self, metadata, onlyA=False):
		self.md    = metadata
		self.onlyA = bool(onlyA)
		self.beta  = None   # fitted parameters
	
	@property
	def X(self):   # design matrix (abstract, to be implemented in subclasses)
		pass

	@property
	def isfit(self):   # number of observations
		return self.beta is not None

	@property
	def n(self):   # number of observations
		return self.md.nsteps

	@property
	def yhat(self):
		return self.X @ self.beta

	def detrend(self, y):
		self.fit( y )
		self.yd    = y - self.yhat
		return self.yd

	def fit(self, y):
		if self.onlyA:
			i     = self.md.cond==0
			beta  = np.linalg.pinv(self.X[i]) @ y[i]
		else:
			beta  = np.linalg.pinv(self.X) @ y
		self.beta = beta
		self.y    = y

	# def fit(self, y):
	# 	self.beta  = np.linalg.pinv(self.X) @ y
	# 	self.y     = y
		
	def plot(self):
		fig,axs = plt.subplots( 1, 3, figsize=(8,3), gridspec_kw=dict(width_ratios=[1, 3, 3]) )
		# colors  = ['0.7', 'b', 'c', 'r']
		ax0,ax1,ax2 = axs.ravel()
		
		ax0.imshow( self.X, cmap='gray', aspect='auto', interpolation='nearest' )
		
		if self.isfit:
			t  = self.md.t
			ax1.plot(t, self.y, '.', label='Observations')
			if self.onlyA:
				i     = self.md.cond==0
				ax1.plot(t[i], self.yhat[i], '.-', label='Fits')
			else:
				ax1.plot(t, self.yhat, '.-', label='Fits')
			leg = ax1.legend()
			plt.setp(leg.get_texts(), size=8)
			
			ax2.plot(t, self.yd, '.', label='Detrended')
			for i in range(7):
				b = self.md.cond0 == i
				ax2.plot(t[b].mean(), self.yd[b].mean(), 'o', ms=12, color='c')
			ax2.axhline(0, ls='--')
			
			labels = 'Trend Model', 'Observations & Fits', 'Detrended Observations'
			[ax.set_title(s, size=11) for ax,s in zip(axs, labels)]

		else:
			[ax.text(0.5, 0.5, 'Model not yet fit', ha='center')  for ax in axs[1:]]
			ax0.set_title('Design matrix')

		[plt.setp(ax.get_xticklabels() + ax.get_yticklabels(), size=8)  for ax in axs.ravel()]
		plt.tight_layout()
		
	# def plot(self, ax=None):
	# 	ax      = plt.gca() if (ax is None) else ax
	# 	ax.imshow( self.X, cmap='gray', aspect='auto', interpolation='nearest' )


	
class LinearDriftOverObservationsModel(_Model):

	@property
	def X(self):   
		X          = np.zeros( (self.n, 2) )
		X[ : , 0 ] = 1
		X[ : , 1 ] = np.linspace(0, 1, self.n)
		return X


class LinearDriftOverTimeModel(_Model):

	@property
	def X(self):
		t          = self.md.t
		t          = (t - t[0]) / (t.max() - t[0])
		X          = np.zeros( (self.n, 2) )
		X[ : , 0 ] = 1
		X[ : , 1 ] = t
		return X
		
