# -*- coding: utf-8 -*-

"""

NETZWERK
Computer network renderer
https://github.com/pleiszenburg/netzwerk

	setup.py: Module setup

	Copyright (C) 2017 Sebastian M. Ernst <ernst@pleiszenburg.de>

<LICENSE_BLOCK>
The contents of this file are subject to the GNU Lesser General Public License
Version 2.1 ("LGPL" or "License"). You may not use this file except in
compliance with the License. You may obtain a copy of the License at
https://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt
https://github.com/pleiszenburg/netzwerk/blob/master/LICENSE

Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for the
specific language governing rights and limitations under the License.
</LICENSE_BLOCK>

"""


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from setuptools import (
	find_packages,
	setup
	)
import os
from glob import glob


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# SETUP
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# Bump version HERE!
_version_ = '0.0.0'


# List all versions of Python which are supported
confirmed_python_versions = [
	('Programming Language :: Python :: %s' % x)
	for x in '3.5 3.6'.split()
	]


# Fetch readme file
with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
	long_description = f.read()


setup(
	name = 'netzwerk',
	packages = find_packages('src'),
	package_dir = {'': 'src'},
	version = _version_,
	description = 'Computer network renderer',
	long_description = long_description,
	author = 'Sebastian M. Ernst',
	author_email = 'ernst@pleiszenburg.de',
	url = 'https://github.com/pleiszenburg/netzwerk',
	download_url = 'https://github.com/pleiszenburg/netzwerk/archive/v%s.tar.gz' % _version_,
	license = 'LGPLv2',
	keywords = ['computer network'],
	scripts = glob(os.path.join('scripts', '*')),
	include_package_data = True,
	install_requires = [],
	zip_safe = False,
	extras_require = {},
	entry_points = {},
	classifiers = [
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
		'Operating System :: POSIX :: Linux',
		'Programming Language :: Python :: 3'
		] + confirmed_python_versions + [
		'Programming Language :: Python :: 3 :: Only',
		'Programming Language :: Python :: Implementation :: CPython',
		'Topic :: Scientific/Engineering',
		'Topic :: Utilities'
		]
)
