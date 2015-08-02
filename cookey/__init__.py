# -*- coding: utf-8 -*-
"""Main project's main package's __init__.py file."""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

__versionstr__ = '0.1.0'
__version__ = tuple([int(ver_i) for ver_i in __versionstr__.split('.')])
__author__ = 'Jamiel Almeida'
__email__ = 'slashfoo@gmail.com'
__projname__ = 'cookey'
__shortdoc__ = 'A package to analyze the efficiency of keyboard layouts'
__url__ = ''  # TODO: URL TBD
__license__ = 'MIT'

locals()['__doc__'] = __shortdoc__

if 'ver_i' in locals():
    del locals()['ver_i']  # this remained after using 'ver_i' as a loop var above

# cleaning up feature-imports
del locals()['print_function']
del locals()['unicode_literals']
del locals()['absolute_import']
del locals()['division']
