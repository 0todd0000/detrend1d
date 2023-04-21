
import numpy as np
from matplotlib import pyplot as plt
# from . import inter, intra
from . inter import *
from . intra import *




class Compound(object):
	def __init__(self, inter=None, intra=None):
		self.trend0  = inter
		self.trend1  = intra
		
	def apply(self, t, y):
		y1 = self.trend0.apply(t, y)
		return self.trend1.apply(t, y1)

	def plot(self, ax=None, t0=0, t1=10, n=51):
		ax    = plt.gca() if (ax is None) else ax
		t     = np.linspace(t0, t1, n)
		y     = self.apply(t, np.zeros(n))
		ax.plot(t, y)	