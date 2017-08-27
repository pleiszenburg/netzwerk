# -*- coding: utf-8 -*-

"""

NETZWERK
Computer network renderer
https://github.com/pleiszenburg/netzwerk

	src/netzwerk/scripte.py: Eingangspunkte für Scripte

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

import json
import sys

from .const import KEY_NAME
from .netzwerk import netzwerk


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINEN
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def renderer():

	datei_name = sys.argv[1]

	f = open(datei_name, 'r')
	netzwerk_liste = json.load(f)
	f.close()

	netzwerk_obj = netzwerk({KEY_NAME: datei_name})

	for element in netzwerk_liste:
		if type(element) == list:
			netzwerk_obj.verbinde_komponenten(element)
		elif type(element) == dict:
			netzwerk_obj.erstelle_komponente(element)
		else:
			raise # TODO

	netzwerk_obj.rendere_netzwerk(datei_name + '.svg')
