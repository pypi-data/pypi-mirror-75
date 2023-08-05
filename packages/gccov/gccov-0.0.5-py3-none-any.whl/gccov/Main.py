#!/usr/bin/env python3

__author__ = 'Jie Li'
__copyright__ = 'Copyright 2019'
__credits__ = ['Jie Li']
__email__ = 'mm.jlli6t@gmail.com'
__status__ = 'Development'

import os
import sys
import argparse

import pandas as pd


sys.path = [os.path.join((os.path.dirname(os.path.realpath(__file__))), '..')] + sys.path

from biosut.biosys import gt_file, gt_path
from biosut.io_seq import gc_to_dict
from gccov.scatter import scatter
from gccov.coverm import coverm

def read_pars(args):

	p = argparse.ArgumentParser(description=__doc__)
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

if __name__ == '__main__':
	pars = read_pars(sys.argv)
	outdir = gt_path.sure_exist(pars.outdir)
	gc_table = gc_to_dict(pars.contigs, pars.contig_len, length=True)

	gc_table = pd.DataFrame.from_dict(gc_table)

	print("Finished get GC content.\n")

	gc_table.to_csv(outdir + pars.prefix + '_gc_content.txt', sep='\t')

	if pars.bam_file:
		cov = os.path.join(outdir, pars.prefix+'.coverage')
		coverm_pile = coverm(pars.bam_file, cov)
		coverm_pile.run()
	else:
		cov = pars.coverage
	gt_file.check_exist(cov, check_empty=True)

	cov = pd.read_csv(cov, sep="\t", header=0, index_col=0)
	cov.columns = ['Coverage']
	print('Finished get Coverage.\n')

	# get contigs have both gc and coverage
	new = cov.merge(gc_table, how='inner', left_index=True, right_index=True)
	new.to_csv(outdir + pars.prefix +'_gc_and_coverage.csv', sep='\t')

	if '-' in pars.cov_width:
		cov_width = [float(i) for i in pars.cov_width.split('-')]
		new = new[(new.Coverage >= cov_width[0]) & (new.Coverage <= cov_width[1])]

	scatter_plot = scatter(new, outdir+pars.prefix+'.pdf', \
							pars.bins_dir, pars.suffix, pars.scale, \
							pars.size)
#	scatter_plot = scatter(new, outdir+pars['prefix']+'.pdf', **pars)
	scatter_plot.plot()
