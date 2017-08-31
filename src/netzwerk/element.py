# -*- coding: utf-8 -*-

"""

NETZWERK
Computer network renderer
https://github.com/pleiszenburg/netzwerk

	src/netzwerk/element.py: Basis-Klasse für alle Netzwerk-Gegenstände

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

from .const import *


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# KLASSEN
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Basis-Klasse: Alles ist eine Element, hat einen Namen und Parameter
class element(object):

	def __init__(self, parameter):

		self.p = parameter
		self.svg = {}


	def rendere_svg(self, parameter):

		raise NotImplementedError


	def ersetze_parameter(self, vorlage, parameter):

		for key in list(parameter.keys()):
			vorlage = vorlage.replace('{{' + key + '}}', str(parameter[key]))

		return vorlage


	def schreibe_svg(self, dateiname):

		f = open(dateiname, 'w')
		f.write(self.svg[KEY_SVG])
		f.close()


	def __sortiere_liste_von_elementen__(self, liste_elemente, schluessel):

		sorted(liste_elemente, key = lambda gegenstand: gegenstand.p[schluessel])


	def __vervollstaendige_dict__(self, in_dict, default_dict):

		for schluessel in default_dict.keys():
			if schluessel not in in_dict.keys():
				in_dict[schluessel] = default_dict[schluessel]


	def __vervollstaendige_svg__(self, svg, globaler_kopf = False):

		if globaler_kopf:

			svg.insert(0, '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">' % (
				self.svg[KEY_BREITE], self.svg[KEY_HOEHE], self.svg[KEY_BREITE], self.svg[KEY_HOEHE]
				))
			svg.insert(0, '<?xml version="1.0" encoding="UTF-8"?>\n')

		else:

			if KEY_X in self.svg.keys() and KEY_Y in self.svg.keys():
				svg.insert(0, '<svg x="%d" y="%d" width="%d" height="%d">' % (
					self.svg[KEY_X], self.svg[KEY_Y], self.svg[KEY_BREITE], self.svg[KEY_HOEHE]
					))
			else:
				svg.insert(0, '<svg x="{{' + KEY_X + '}}" y="{{' + KEY_Y + '}}" width="%d" height="%d">' % (
					self.svg[KEY_BREITE], self.svg[KEY_HOEHE]
					))

		svg.append('</svg>')

		self.svg[KEY_SVG] = ''.join(svg)


	def __fixiere_element__(self, position):

		self.svg.update(position)
		self.svg[KEY_SVG] = self.ersetze_parameter(self.svg[KEY_SVG], position)


	def __korrigiere_positionen__(self):

		raise NotImplementedError


	def __zeichne_schnittstellen__(self, svg):

		raise NotImplementedError


	def __ipv4_zu_text__(self, wert):

		return '.'.join([('%d' % seg) for seg in wert])


	def __ipv6_zu_text__(self, wert):

		raise NotImplementedError


	def __mac_zu_text__(self, wert):

		return ':'.join([('%02x' % seg) for seg in wert])
