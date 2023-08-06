"""
The :mod:`gccov.scatter` plot scatter bubbles.
"""

# Author: Jie Li <mm.jlli6t@gmail.com>
# License: GNU v3.0
# Copyrigth: 2019

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from biosut import io_seq
import os
import pandas as pd

class scatter:
	def __init__(self, data, outpdf, bins_dir=None, suffix='fa', scale=False, size=1):
#	def __init__(self, data, outpdf, **targs):
		self.data = data
		self.bins_dir = bins_dir
		self.suffix = suffix
		self.outpdf = outpdf
		self.scale = scale
		self.size = 10000/size

	def plot(self):
		if self.bins_dir:
			full_contigs_color = self._color_set()
		else:
			full_contigs_color = ['grey'] * len(self.data)
		print('You are plotting with color: ', set(full_contigs_color))
#		self.data.color = full_contigs_color
#		self.data.srt_values(by='color')
		plt.figure(1)
		if self.scale:
#			self.data.plot.scatter(x='GC_content', y='Coverage',
#								c=full_contigs_color, linewidths=.5,
#								edgecolors='k', alpha=.5,
#								s=self.data['Seq_length']/10000)
			self.data.plot.scatter(x='gc_ratio', y='coverage',
								c='white', linewidth=.5,
								edgecolors=full_contigs_color,
								alpha=.5, s=self.data['seq_length']/self.size)
		else:
			self.data.plot.scatter(x='gc_ratio', y='coverage',
								c=full_contigs_color, alpha=.5, s=1)

		plt.xlabel('GC%')
		plt.ylabel('Coverage')
		plt.savefig(self.outpdf)

	def _color_set(self):
		flag = 0
		color_sets = ['blue', 'red', 'yellow', 'green', 'orange', 'purple', 'pink']
		contigs_color = {}
		for f in os.listdir(self.bins_dir):
			if f.endswith(self.suffix):
				#print(f)
				print(color_sets[flag])
				f_ids = io_seq.seq_to_dict(os.path.join(self.bins_dir, f), outqual=False)
				for i in f_ids.keys():
					f_ids[i] = color_sets[flag]
				contigs_color.update(f_ids)
				flag += 1
		# then assign grey to all unbinned contigs
		full_contigs_color=[contigs_color[i] if i in contigs_color.keys() else 'grey' for i in self.data.index]
		return full_contigs_color
