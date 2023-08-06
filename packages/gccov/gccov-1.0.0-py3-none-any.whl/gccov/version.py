"""
The :mod:`gccov.version` printing version information.
"""

# Author: Jie Li <mm.jlli6t@gmail.com>
# License: GNU v3.0

import os
from biosut.gt_path import abs_path

class Version:

    def get_version():
        ver1 = os.path.dirname(abs_path(__file__)) + '/version'
        ver2 = os.path.dirname(abs_path(__file__)) + '/../version'
        if os.path.isfile(ver1):return open(ver1).readline().strip()
        if os.path.isfile(ver2):return open(ver2).readline().strip()
        return 'Unknow version'

    @classmethod
    def show_version(cls):
        ver = cls.get_version()
        print('\n\n\t\tgccov version * %s *\n\n' % ver)
