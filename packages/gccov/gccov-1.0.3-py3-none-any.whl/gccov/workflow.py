"""
The :mod:`gccov.main` pileup the workflow.
"""

# Author: Jie Li <mm.jlli6t@gmail.com>
# License: GNU v3.0
# Copyrigth: 2019

import os
import sys
import argparse

import pandas as pd
from biosut.gt_path import real_path

sys.path = [os.path.join((os.path.dirname(real_path(__file__))), '..')] + sys.path

from biosut import gt_file, gt_path
from biosut.io_seq import gc_to_dict

from gccov.scatter import scatter
from gccov.coverm import coverm
from gccov.version import Version

def read_arg(args):

	p = argparse.ArgumentParser(description=Version.show_version())
	required_argument = p.add_argument_group('Required arguments')

	required_argument.add_argument('--contigs', required=True,
								help='contigs/scaffolds for GC content')

	mutual_required_argument = p.add_argument_group('Mutually exclusive required argument')
	mutual_rgs = mutual_required_argument.add_mutually_exclusive_group(required=True)
	mutual_rgs.add_argument('--coverage', help='coverage file, with column name Coverage')
	mutual_rgs.add_argument('--bam_file', help='sorted bam file')

	optional_arguments = p.add_argument_group('Optional arguments')
	optional_arguments.add_argument('-scale', default=False, action='store_true',
					help='set to scale scatter dots with your scaffolds/contigs length')
	optional_arguments.add_argument('-size', default=1, type=float,
					help='bubles relative size you want, default is 1, you can set to 1.5, 3, 5 or so')
	optional_arguments.add_argument('-prefix', default='gc_coverage',
					help='prefix of outputs, [gc_coverage]')
	optional_arguments.add_argument('-contig_len', default=2500, type=float,
					help='contig length cutoff for GC content and plot, [2500]')
	optional_arguments.add_argument('-cov_width', default='0', type=str,
					help='cov range you want to plot, for example 0-100, single 0 means all, [0]')
	optional_arguments.add_argument('-bins_dir', default=None,
					help='bins dir to color genomes you provide')
	optional_arguments.add_argument('-suffix', default='fa',
					help='suffix of bins if you profile -bins_dir, [fa]')
	optional_arguments.add_argument('-outdir', default=os.getcwd(),
					help='output dir')
	return p.parse_args()

class stream:

	def exe(args):
		arg = read_arg(args)
		outdir = gt_path.sure_path_exist(arg.outdir)
		gc_table = gc_to_dict(arg.contigs, arg.contig_len, length=True)

		gc_table = pd.DataFrame.from_dict(gc_table).T
		gc_table.columns = ['gc_count', 'seq_length']
		gc_table['gc_ratio'] = gc_table.gc_count/gc_table.seq_length*100.
		print("Finished get GC content.\n")

		gc_table.to_csv(outdir +'/'+ arg.prefix + '_gc_content.txt', sep='\t')

		if arg.bam_file:
			cov = os.path.join(outdir, arg.prefix+'.coverage')
			coverm_pile = coverm(arg.bam_file, cov)
			coverm_pile.run()
		else:
			cov = arg.coverage
		gt_file.check_file_exist(cov, check_empty=True)

		cov = pd.read_csv(cov, sep="\t", header=0, index_col=0)
		print(cov)
		cov.columns = ['coverage']
		print('Finished get Coverage.\n')

			# get contigs have both gc and coverage
		new = cov.merge(gc_table, how='inner', left_index=True, right_index=True)
		new.to_csv(outdir + '/' + arg.prefix +'_gc_and_coverage.csv', sep='\t')

		if '-' in arg.cov_width:
			cov_width = [float(i) for i in arg.cov_width.split('-')]
			new = new[(new.coverage >= cov_width[0]) & (new.coverage <= cov_width[1])]

		scatter_plot = scatter(new, outdir+'/'+arg.prefix+'.pdf', \
								arg.bins_dir, arg.suffix, arg.scale, \
								arg.size)
#								scatter_plot = scatter(new, outdir+pars['prefix']+'.pdf', **pars)
		scatter_plot.plot()
