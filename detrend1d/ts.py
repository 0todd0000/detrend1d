
import numpy as np
import matplotlib.pyplot as plt


class CyclicalTimeSeries(object):
	def __init__(self, t, y, cycle_labels=None):
		self.t     = t
		self.y     = y
		self.c     = cycle_labels
		
	# def detrend(self, trend):
	# 	trend.fit( self.t, self.y )
	# 	return DetrendedTimeSeries( self.t, self.y, trend )

	def plot(self, ax=None):
		ax = plt.gca() if (ax is None) else ax
		ax.plot(self.t, self.y)


class TimeSeries(object):
	def __init__(self, t, y):
		self.t     = t
		self.y     = y
		
	def detrend(self, trend):
		trend.fit( self.t, self.y )
		return DetrendedTimeSeries( self.t, self.y, trend )

	def plot(self, ax=None):
		ax = plt.gca() if (ax is None) else ax
		ax.plot(self.t, self.y)



class DetrendedTimeSeries(object):
	def __init__(self, t, y, trend):
		self.t     = t
		self.y0    = y
		self.trend = trend
		
	@property
	def y(self):
		return self.y0 - self.yhat

	@property
	def yhat(self):
		return self.trend.get_fitted()

	def plot(self, ax=None):
		ax = plt.gca() if (ax is None) else ax
		ax.plot(self.t, self.y)
		
	def plot_trend(self, ax=None):
		ax = plt.gca() if (ax is None) else ax
		ax.plot(self.t, self.yhat)