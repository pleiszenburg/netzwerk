# NETZWERK
# Computer network renderer
# https://github.com/pleiszenburg/netzwerk
#
#	makefile: GNU makefile for project management
#
# 	Copyright (C) 2017 Sebastian M. Ernst <ernst@pleiszenburg.de>
#
# <LICENSE_BLOCK>
# The contents of this file are subject to the GNU Lesser General Public License
# Version 2.1 ("LGPL" or "License"). You may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# https://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt
# https://github.com/pleiszenburg/netzwerk/blob/master/LICENSE
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for the
# specific language governing rights and limitations under the License.
# </LICENSE_BLOCK>


docu:
	@(cd docs; make clean; make html)

release:
	-rm dist/*
	-rm -r src/*.egg-info
	python setup.py sdist bdist_wheel
	gpg --detach-sign -a dist/netzwerk*.whl
	gpg --detach-sign -a dist/netzwerk*.tar.gz

upload:
	for filename in $$(ls dist/*.tar.gz dist/*.whl) ; do \
		twine upload $$filename $$filename.asc ; \
	done

upload_test:
	for filename in $$(ls dist/*.tar.gz dist/*.whl) ; do \
		twine upload $$filename $$filename.asc -r pypitest ; \
	done

install:
	pip install -r requirements.txt
	pip install .

install_link:
	pip install -r requirements.txt
	pip install -e .

test:
	make docu
	-rm tests/__pycache__/*.pyc
	pytest
