
import numpy as np


class DurationModel(object):
	def __init__(self, mean=1, sd=0):
		self.mean = mean
		self.sd   = sd

	@property
	def isconstant(self):
		return self.sd == 0
	@property
	def isvariable(self):
		return not self.isconstant
	@property
	def value(self):
		return self.rand()
		
	def rand(self):
		return self.mean if self.isconstant else (self.mean + self.sd * np.random.rand())
