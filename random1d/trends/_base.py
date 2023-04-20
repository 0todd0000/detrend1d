
import numpy as np
from matplotlib import pyplot as plt



class _Trend(object):
	
	def __repr__(self):
		s  = f'{self.__class__.__name__}\n'
		s += f'    beta     = {self.beta_str}\n'
		# s += f'    isfitted = {self.isfitted}\n'
		return s

	
	@property
	def beta_str(self):
		return str( self.beta )
	# @property
	# def design_matrix(self):  # fits (used only during fitting)
	# 	return self._fit.X if self.isfitted else None
	# @property
	# def isfitted(self):
	# 	return self._fit.isfitted
	# @property
	# def yhat(self):
	# 	return self._fit.yhat

	# def detrend(self, t, y):
	# 	self.fit(t, y)
	# 	return y - self.yhat
	#
	# def fit(self, t, y):
	# 	self._fit.fit(t, y)
	# 	self.beta = self._fit.beta

	def plot(self, ax=None, t0=0, t1=10, n=51, **kwargs):
		ax    = plt.gca() if (ax is None) else ax
		t     = np.linspace(t0, t1, n)
		y     = self.apply(t, np.zeros(n))
		ax.plot(t, y, **kwargs)

	# def plot_design(self, ax=None, **kwargs):
	# 	self._fit.plot_design( ax, **kwargs )
	#
	# def plot_fit(self, ax=None, **kwargs):
	# 	self._fit.plot( ax, **kwargs )
		