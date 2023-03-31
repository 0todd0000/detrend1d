

import numpy as np
import matplotlib.pyplot as plt



class Dataset0D(object):
	def __init__(self, y, md):
		self.y   = y
		self.md  = md
		
	@property
	def dv(self):
		return self.y

	@property
	def metadata(self):
		return self.md
		
	@property
	def session_means(self):
		usess = np.unique(self.md._sess)
		return np.array(   [self.y[self.md._sess == u].mean(axis=0)   for u in usess])
		
	def plot_verbose(self):
		fig,axs = plt.subplots( 4, 3, figsize=(12,12) )
		colors  = ['0.7', 'b', 'c', 'r']
		colors0 = [colors[0]]*4 + colors[1:]
		t,y     = self.md.t, self.dv
		cond0   = self.md.cond0
		cond    = self.md.cond
		codes0  = self.md._cond_codes0
		codes   = self.md._cond_codes
	
		# plot all data:
		ax      = axs[0,0]
		for i,c in enumerate(colors):
			ax.plot(t[cond==i], y[cond==i], 'o', color=c, ms=3, label=codes[i])
		for i,c in enumerate(colors0):
			ax.plot(t[cond0==i].mean(), y[cond0==i].mean(), 'o', color=c, ms=12)
		leg = ax.legend(ncol=4)
		plt.setp(leg.get_texts(), size=8)
	
		# plot A sessions:
		for i,c in enumerate(colors0[:4]):
			ax = axs[i,1]
			ax.plot(t[cond0==i], y[cond0==i], 'o', color=c, ms=3)
			ax.text(0.03, 0.91, codes0[i], transform=ax.transAxes, bbox=dict(fc='white'))

		# plot other sessions:
		for i,c in enumerate(colors0[4:]):
			ax = axs[i,2]
			ii = i + 4
			ax.plot(t[cond0==(ii)], y[cond0==(ii)], 'o', color=c, ms=3)
			ax.text(0.03, 0.91, codes0[ii], color=c, transform=ax.transAxes, bbox=dict(fc='white', ec=c))

	
		[ax.set_xlabel('Time (s)', size=14)  for ax in [axs[0,0], axs[3,1], axs[2,2]] ]
		axs[0,0].set_ylabel('Dependent variable', size=14)
	
		[plt.setp(ax.get_xticklabels() + ax.get_yticklabels(), size=8)  for ax in axs.ravel()]
		[ax.set_visible(False)  for ax in axs[1:,0]]
		axs[3,2].set_visible(False)
	
		labels = 'All Sessions', '"A" Sessions', 'Other Sessions'
		[ax.set_title(s, size=14)  for ax,s in zip(axs[0], labels)]
	
		plt.tight_layout()

	def plot(self, ax=None, legend=True, legkwargs={}):
		ax      = plt.gca() if (ax is None) else ax
		colors  = ['0.7', 'b', 'c', 'r']
		scolors = [colors[c]  for c in self.md.scond]
		t,y     = self.md.t, self.dv
		sess    = self.md.sess
		slabels = self.md.scondstr
		h,s     = [],[]
		for i,(color,slabel) in enumerate( zip(scolors,slabels) ):
			hh  = ax.plot(t[sess==i]/60, y[sess==i], 'o', color=color, ms=3)[0]
			if slabel not in s:
				h.append( hh )
				s.append( slabel )
		ax.set_xlabel('Time (min)', size=14)
		if legend:
			ax.legend( h, s, **legkwargs )
		plt.tight_layout()
		
		
	# def plot_trendline(self, model, ax=None, **kwargs):
	# 	ax = plt.gca() if (ax is None) else ax
	# 	ax.plot(self.md.t/60, model.yhat, **kwargs)
		