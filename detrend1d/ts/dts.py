
import numpy as np
import matplotlib.pyplot as plt



class DetrendedTimeSeries(object):
	def __init__(self, t, y, trend):
		self.t     = np.asarray(t)
		self.y0    = np.asarray(y)
		self.trend = trend

	@property
	def y(self):
		return self.y0 - self.yhat

	@property
	def yhat(self):
		return self.trend.get_fitted()

	def asarray(self):
		return np.vstack( [self.t, self.y] ).T
	
	def plot(self, ax=None):
		ax = plt.gca() if (ax is None) else ax
		ax.plot(self.t, self.y)

	def plot_trend(self, ax=None):
		ax = plt.gca() if (ax is None) else ax
		ax.plot(self.t, self.yhat)