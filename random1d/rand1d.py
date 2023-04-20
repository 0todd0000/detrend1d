
'''
One-dimensional random number generators
'''

import numpy as np



def _sigmoid(Q, q0=0, q1=5, x0=0, x1=1):
	z          = np.zeros(Q)
	zz         = 6
	z[:q0]     = -zz
	z[q1:]     = +zz
	z[q0:q1]   = np.linspace(-zz, zz, q1-q0)
	y          = 1.0 / (1.0 + np.exp(-1.0 * z))
	y          = (y - y[0]) / (y[-1]-y[0])
	y          = x0 + (y * (x1-x0))
	return y


def _sigmoid_taper(Q, taper_rel):
	taper   = max( round( taper_rel * Q ), 1 )
	w0      = _sigmoid(Q, 0, taper, 0, 1)
	w1      = _sigmoid(Q, Q-taper-1, Q-1, 1, 0)
	w       = w0 * w1
	return w



class GaussianRandomFieldGenerator(object):
	def __init__(self, fwhm=25, amp=1, taper=None):
		self._wtaperfn  = None
		self.fwhm       = fwhm
		self.amp        = amp
		self.gen        = None
		self.taper      = taper
		self._init_generator()
		self._init_taper()

	def _init_generator(self):
		import rft1d
		self.gen = lambda x: rft1d.randn1d(1, x, FWHM=self.fwhm, pad=True)

	def _init_taper(self):
		if self.taper is not None:
			self._wtaperfn = lambda x: _sigmoid_taper( x, self.taper )

	def generate(self, n):
		w = 1 if self.taper is None else self._wtaperfn(n)
		return w * self.amp * self.gen( n )


# much easier to implement variable-durations in the CyclicalTimeSeriesGenerator class

# class VariableLengthGaussianRandomFieldGenerator(object):
# 	def __init__(self, Q=101, Qsd=None, fwhm=25, amp=1, taper=None):
# 		self._wtaperfn  = None
# 		self.Q          = Q
# 		self.Qsd        = Qsd
# 		self.fwhm       = fwhm
# 		self.amp        = amp
# 		self.gen        = None
# 		self.taper      = taper
# 		self._init_taper()
#
# 	def _init_taper(self):
# 		if self.taper is not None:
# 			self._wtaperfn = lambda x: _sigmoid_taper( x, self.taper )
#
# 	def generate(self):
# 		import rft1d
# 		Q  = self.Q if (self.Qsd in [0,None]) else round(self.Q + self.Qsd * np.random.randn())
# 		y  = self.amp * rft1d.randn1d(1, Q, FWHM=self.fwhm, pad=False)
# 		w  = 1 if self.taper is None else self._wtaperfn(n)
# 		return w * y


