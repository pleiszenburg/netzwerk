# -*- coding: utf-8 -*-

"""

NETZWERK
Computer network renderer
https://github.com/pleiszenburg/netzwerk

	src/netzwerk/schnittstelle.py: Ports an Netzwerkkarten, Hauptplatinen ...

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
from .element import element


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# KLASSEN
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Basis für Schnittstellen: Ethernet, USB, Firewire ...
class schnittstelle(element):

	def __init__(self, parameter):

		super().__init__(parameter)


	def __vervollstaendige_stecker__(self):

		if self.svg[KEY_STECKER][KEY_ORIENTIERUNG] == KEY_OBEN:
			self.svg[KEY_STECKER].update({
				KEY_X: self.svg[KEY_BREITE] / 2,
				KEY_Y: 0
				})
		elif self.svg[KEY_STECKER][KEY_ORIENTIERUNG] == KEY_UNTEN:
			self.svg[KEY_STECKER].update({
				KEY_X: self.svg[KEY_BREITE] / 2,
				KEY_Y: self.svg[KEY_HOEHE]
				})
		elif self.svg[KEY_STECKER][KEY_ORIENTIERUNG] == KEY_LINKS:
			self.svg[KEY_STECKER].update({
				KEY_X: 0,
				KEY_Y: self.svg[KEY_HOEHE] / 2
				})
		elif self.svg[KEY_STECKER][KEY_ORIENTIERUNG] == KEY_RECHTS:
			self.svg[KEY_STECKER].update({
				KEY_X: self.svg[KEY_BREITE],
				KEY_Y: self.svg[KEY_HOEHE] / 2
				})
		else:
			raise


	def __zeichne_schnittstelle__(self, svg):

		svg.append('<circle cx="%d" cy="%d" r="%d" fill="%s"/>' % (
			self.svg[KEY_STECKER][KEY_X], self.svg[KEY_STECKER][KEY_Y], PARAM_RJ45W_R, PARAM_RJ45W_FARBE
			))


	def __korrigiere_positionen__(self):

		for dimension in [KEY_X, KEY_Y]:
			self.svg[KEY_STECKER][dimension] += self.svg[dimension]


# Ethernet-Schnittstellen
class schnittstelle_ethernet(schnittstelle):

	def __init__(self, parameter):

		super().__init__(parameter)

		self.p[KEY_TYP] = KEY_ETHERNET

		# Standart-Parameter setzen, falls nichts vorhanden
		if KEY_PREFIX not in self.p.keys():
			self.p[KEY_PREFIX] = ''
		if KEY_SUFFIX not in self.p.keys():
			self.p[KEY_SUFFIX] = ''
		if KEY_MASKE not in self.p.keys():
			self.p[KEY_MASKE] = '%d'
		if KEY_NUMMER not in self.p.keys():
			self.p[KEY_NUMMER] = 0
		if KEY_NAME not in self.p.keys():
			self.p[KEY_NAME] = self.p[KEY_PREFIX] + (self.p[KEY_MASKE] % self.p[KEY_NUMMER]) + self.p[KEY_SUFFIX]
		if KEY_PASSIV not in self.p.keys():
			self.p[KEY_PASSIV] = False
		if KEY_VERBINDUNG not in self.p.keys():
			self.p[KEY_VERBINDUNG] = KEY_STECKER
		if KEY_ELTERN not in self.p.keys():
			self.p[KEY_ELTERN] = KEY_COMPUTER
		if KEY_POSITION not in self.p.keys():
			self.p[KEY_POSITION] = KEY_UNBEKANNT
		if KEY_MAC not in self.p.keys():
			self.p[KEY_MAC] = DEFAULT_MAC
		if KEY_IPV4 not in self.p.keys():
			self.p[KEY_IPV4] = {}
		if not self.p[KEY_PASSIV]:
			if KEY_ADRESSE not in self.p[KEY_IPV4].keys():
				self.p[KEY_IPV4][KEY_ADRESSE] = DEFAULT_IPV4
				default_ipv4 = True
			else:
				default_ipv4 = False
			if KEY_SUBNETZMASKE not in self.p[KEY_IPV4].keys():
				self.p[KEY_IPV4][KEY_SUBNETZMASKE] = DEFAULT_SUBNETZMASKE
			if KEY_DHCP not in self.p[KEY_IPV4].keys():
				if default_ipv4:
					self.p[KEY_IPV4][KEY_DHCP] = True
				else:
					self.p[KEY_IPV4][KEY_DHCP] = False


	def __rendere_svg_computerport__(self, parameter):

		svg = []
		self.svg = parameter

		# Hintergrund
		svg.append(
			'<rect x="%d" y="%d" width="%d" height="%d" fill="%s" />' % (
				0, 0, PARAM_ETHERNET_BREITE, PARAM_ETHERNET_HOEHE + 2 * PARAM_ABSTAND_KLEIN, PARAM_ETHERNET_FARBE
				)
			)

		# Beschriftungen zusammenstellen
		beschriftung = [
			{KEY_TEXT: self.p[KEY_NAME] + ' [' + self.p[KEY_POSITION] + ']'},
			{KEY_TEXT: self.__mac_zu_text__(self.p[KEY_MAC])}
			]
		if self.p[KEY_IPV4][KEY_DHCP]:
			beschriftung.append({KEY_TEXT: KEY_DHCP})
		else:
			beschriftung.append({KEY_TEXT: self.__ipv4_zu_text__(self.p[KEY_IPV4][KEY_ADRESSE])})

		# Beschriftungen ausgeben
		y = PARAM_ABSTAND_KLEIN
		for zeile in beschriftung:
			svg.append(
				'<text x="%d" y="%d" font-family="%s" font-size="%d" fill="%s" dominant-baseline="middle">%s</text>' % (
					2 * PARAM_ABSTAND_KLEIN, y + PARAM_ETHERNET_SCHRIFTGROESSE / 2, PARAM_TEXT_FONT, PARAM_ETHERNET_SCHRIFTGROESSE, PARAM_TEXT_FARBE, zeile[KEY_TEXT]
					)
				)
			y += PARAM_ETHERNET_SCHRIFTGROESSE

		# Parameter zur Rückgabe vorbereiten
		self.svg.update({
			KEY_BREITE: PARAM_ETHERNET_BREITE,
			KEY_HOEHE: PARAM_ETHERNET_HOEHE + 2 * PARAM_ABSTAND_KLEIN,
			KEY_STECKER: {
				KEY_ORIENTIERUNG: KEY_LINKS,
				KEY_X: 0,
				KEY_Y: (PARAM_ETHERNET_HOEHE + 2 * PARAM_ABSTAND_KLEIN) / 2
				}
			})

		# Stecker definieren
		self.__vervollstaendige_stecker__()

		# SVG fertig machen
		self.__vervollstaendige_svg__(svg)


	def __rendere_svg_switchport__(self, parameter):

		svg = []
		self.svg = parameter

		# Hintergrund
		svg.append(
			'<rect x="%d" y="%d" width="%d" height="%d" fill="%s" />' % (
				0, 0, PARAM_ETHERNETPASSIV_BREITE, PARAM_ETHERNETPASSIV_HOEHE, PARAM_ETHERNET_FARBE
				)
			)

		# Beschriftungen ausgeben
		svg.append(
			'<text x="%d" y="%d" font-family="%s" font-size="%d" fill="%s" dominant-baseline="middle" text-anchor="middle">%s</text>' % (
				PARAM_ETHERNETPASSIV_BREITE / 2, PARAM_ETHERNETPASSIV_HOEHE / 2, PARAM_TEXT_FONT, PARAM_ETHERNET_SCHRIFTGROESSE, PARAM_TEXT_FARBE, self.p[KEY_NAME]
				)
			)

		# Parameter zur Rückgabe vorbereiten
		self.svg.update({
			KEY_BREITE: PARAM_ETHERNETPASSIV_BREITE,
			KEY_HOEHE: PARAM_ETHERNETPASSIV_HOEHE,
			KEY_STECKER: {
				KEY_ORIENTIERUNG: KEY_UNTEN,
				KEY_X: PARAM_ETHERNETPASSIV_BREITE / 2,
				KEY_Y: PARAM_ETHERNETPASSIV_HOEHE
				}
			})

		# Stecker definieren
		self.__vervollstaendige_stecker__()

		# SVG fertig machen
		self.__vervollstaendige_svg__(svg)


	def __rendere_svg_doseport__(self, parameter):

		self.svg = parameter

		# Parameter zur Rückgabe vorbereiten
		self.svg.update({
			KEY_SVG: '',
			KEY_BREITE: 0,
			KEY_HOEHE: 0,
			KEY_STECKER: {
				KEY_ORIENTIERUNG: self.svg[KEY_ORIENTIERUNG],
				KEY_X: 0,
				KEY_Y: 0
				}
			})


	def rendere_svg(self, parameter):

		# Auf einer Dose oder einem Loch in der Wand?
		if self.p[KEY_ELTERN] in [KEY_DOSE, KEY_LOCH, KEY_VORBEREITET]:

			self.__rendere_svg_doseport__(parameter)

		# Auf einem Computer?
		elif self.p[KEY_ELTERN] == KEY_COMPUTER:

			# Passiv auf einem Switch oder aktiv auf einem Computer?
			if self.p[KEY_PASSIV]:
				self.__rendere_svg_switchport__(parameter)
			else:
				self.__rendere_svg_computerport__(parameter)

		# Unbekannte Eltern
		else:

			raise
