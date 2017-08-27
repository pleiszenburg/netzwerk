# -*- coding: utf-8 -*-

"""

NETZWERK
Computer network renderer
https://github.com/pleiszenburg/netzwerk

	src/netzwerk/uebergang.py: Übergänge wie Dosen

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

import copy

from .const import *
from .element import element


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# KLASSEN
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Basis für Dosen, Löcher in den Wänden, Patchfelder ...
class uebergang(element):

	def __init__(self, parameter):

		super().__init__(parameter)

		self.schnittstellen = {} # Haben alle Verbindungen Schnittstellen oder nur Ethernet-Dosen?

		# Standart-Parameter setzen, falls nichts vorhanden
		if KEY_NAME not in self.p.keys():
			if KEY_MASKE not in self.p.keys():
				self.p[KEY_MASKE] = '%02d'
			if KEY_PREFIX not in self.p.keys():
				self.p[KEY_PREFIX] = ''
			if KEY_SUFFIX not in self.p.keys():
				self.p[KEY_SUFFIX] = ''
			self.p[KEY_NAME] = self.p[KEY_PREFIX] + (self.p[KEY_MASKE] % self.p[KEY_NUMMER]) + self.p[KEY_SUFFIX]
		if KEY_HIERARCHIEEBENE not in self.p.keys():
			self.p[KEY_HIERARCHIEEBENE] = KEY_RAUM
		if KEY_SCHNITTSTELLEN not in self.p.keys():
			self.p[KEY_SCHNITTSTELLEN] = {}
		if KEY_ETHERNET not in self.p[KEY_SCHNITTSTELLEN].keys():
			self.p[KEY_SCHNITTSTELLEN][KEY_ETHERNET] = []

		# Schnittstellen zu Parametern hinzufuegen
		if self.p[KEY_TYP] == KEY_DOSE:
			if self.p[KEY_HIERARCHIEEBENE] == KEY_RAUM:
				verbindungen = {KEY_A: KEY_KLEMME, KEY_B: KEY_STECKER}
			else:
				verbindungen = {KEY_A: KEY_STECKER, KEY_B: KEY_KLEMME}
		elif self.p[KEY_TYP] == KEY_LOCH:
			verbindungen = {KEY_A: KEY_LOCH, KEY_B: KEY_LOCH}
		elif self.p[KEY_TYP] == KEY_VORBEREITET:
			verbindungen = {KEY_A: KEY_VORBEREITET}
		else:
			raise
		verbindungen_schluessel = list(verbindungen.keys())
		verbindungen_schluessel.sort()
		for index, verbindung in enumerate(verbindungen_schluessel):
			self.p[KEY_SCHNITTSTELLEN][KEY_ETHERNET].append({
				KEY_NAME: verbindung,
				KEY_NUMMER: index,
				KEY_PASSIV: True,
				KEY_ELTERN: self.p[KEY_TYP],
				KEY_VERBINDUNG: verbindungen[verbindung]
				})

		# Schnittstellen erstellen
		for ethernet_port in self.p[KEY_SCHNITTSTELLEN][KEY_ETHERNET]:
			neue_schnittstelle = schnittstelle_ethernet(ethernet_port)
			self.schnittstellen[neue_schnittstelle.p[KEY_NAME]] = neue_schnittstelle


	def __zeichne_schnittstellen__(self, svg):

		for schluessel_schnittstelle in list(self.schnittstellen.keys()):
			self.schnittstellen[schluessel_schnittstelle].__zeichne_schnittstelle__(svg)


	def __korrigiere_positionen__(self):

		for schluessel_schnittstelle in list(self.schnittstellen.keys()):
			ding = self.schnittstellen[schluessel_schnittstelle]
			for dimension in [KEY_X, KEY_Y]:
				ding.svg[dimension] += self.svg[dimension]
			ding.__korrigiere_positionen__()


	def __rendere_svg__(self, parameter):

		svg = []
		self.svg = parameter

		# Hintergrund
		svg.append(
			'<rect x="%d" y="%d" width="%d" height="%d" fill="%s" />' % (
				0, 0, PARAM_DOSE_BREITE, PARAM_DOSE_HOEHE, parameter[KEY_HINTERGRUNDFARBE]
				)
			)

		# Beschriftungen ausgeben
		svg.append(
			'<text x="%d" y="%d" font-family="%s" font-size="%d" fill="%s" dominant-baseline="middle" text-anchor="middle">%s</text>' % (
				PARAM_DOSE_BREITE / 2, PARAM_DOSE_HOEHE / 2, PARAM_TEXT_FONT, PARAM_ETHERNET_SCHRIFTGROESSE, PARAM_TEXT_FARBE, self.p[KEY_NUMMER]
				)
			)

		# Schnittstellen 'darstellen' und positionieren
		if self.p[KEY_HIERARCHIEEBENE] == KEY_RAUM:
			position = {KEY_X: [0, PARAM_DOSE_BREITE], KEY_Y: [PARAM_DOSE_HOEHE / 2, PARAM_DOSE_HOEHE / 2], KEY_ORIENTIERUNG: [KEY_LINKS, KEY_RECHTS]}
		else:
			position = {KEY_X: [PARAM_DOSE_BREITE / 2, PARAM_DOSE_BREITE / 2], KEY_Y: [0, PARAM_DOSE_HOEHE], KEY_ORIENTIERUNG: [KEY_OBEN, KEY_UNTEN]}
		schnittstellen_keys = list(self.schnittstellen.keys())
		schnittstellen_keys.sort()
		for index, schnittstelle in enumerate(schnittstellen_keys):
			self.schnittstellen[schnittstelle].rendere_svg({
				KEY_X: position[KEY_X][index],
				KEY_Y: position[KEY_Y][index],
				KEY_ORIENTIERUNG: position[KEY_ORIENTIERUNG][index]
				})
			svg.append(self.schnittstellen[schnittstelle].svg[KEY_SVG])

		# Parameter zur Rückgabe vorbereiten
		self.svg.update({
			KEY_BREITE: PARAM_DOSE_BREITE,
			KEY_HOEHE: PARAM_DOSE_HOEHE
			})

		# SVG fertig machen
		self.__vervollstaendige_svg__(svg)


# Dosen mit Steckern und Klemmen
class uebergang_dose(uebergang):

	def __init__(self, parameter):

		super().__init__(parameter)


	def rendere_svg(self, parameter):

		parameter[KEY_HINTERGRUNDFARBE] = PARAM_ETHERNET_FARBE
		self.__rendere_svg__(parameter)


# Loch in der Wand
class uebergang_loch(uebergang):

	def __init__(self, parameter):

		super().__init__(parameter)


	def rendere_svg(self, parameter):

		parameter[KEY_HINTERGRUNDFARBE] = PARAM_LOCH_FARBE
		self.__rendere_svg__(parameter)


# Vorbereitete Dose, beispielsweise durch Kabel in Decke
class uebergang_vorbereitet(uebergang):

	def __init__(self, parameter):

		super().__init__(parameter)


	def rendere_svg(self, parameter):

		parameter[KEY_HINTERGRUNDFARBE] = PARAM_VORBEREITET_FARBE
		self.__rendere_svg__(parameter)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINEN
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Viele Dosen bilden ein Patchfeld - Funktion erstellt Liste von Dosen
def verbindung_patchfeld(parameter):

	if KEY_MASKE not in parameter.keys():
		parameter[KEY_MASKE] = '%02d'
	if KEY_PREFIX not in parameter.keys():
		parameter[KEY_PREFIX] = ''
	if KEY_SUFFIX not in parameter.keys():
		parameter[KEY_SUFFIX] = ''

	dosen = []

	anschluesse = parameter[KEY_ANSCHLUESSE]
	anschluesse.sort()
	del parameter[KEY_ANSCHLUESSE]
	parameter[KEY_TYP] = KEY_DOSE

	for anschluss in anschluesse:
		parameter[KEY_NUMMER] = anschluss
		dosen.append(uebergang_dose(copy.deepcopy(parameter)))

	return dosen
