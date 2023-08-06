# -*- coding:utf-8 -*-

from setuptools import setup, find_packages
import os
from gccov.version import Version

setup(
	name = 'gccov',
	description = 'Visualize gc & coverage.',
	version = Version.get_version(),
	url = 'https://github.com/jlli6t/gccov',
	author = 'Jie Li',
	author_email = 'mm.jlli6t@gmail.com',
	maintainer = 'Jie Li',
	maintainer_email = 'mm.jlli6t@gmail.com',

	classifiers = [
				'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
				'Programming Language :: Python :: 3 :: Only',
				'Operating System :: Unix',
		],
	keywords = 'biology bioinformatics',
	scripts=['bin/gccov'],
	packages = find_packages(),
	python_requires = '>=3.6',
	install_requires=['biosut>=2.0.0',],
)
