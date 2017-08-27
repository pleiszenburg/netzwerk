# -*- coding: utf-8 -*-

"""

NETZWERK
Computer network renderer
https://github.com/pleiszenburg/netzwerk

	src/netzwerk/komponente.py: Computer, Switche, Hubs ...

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

# Basis für Komponenten: Computer, Switche, Telefone
class komponente(element):

	def __init__(self, parameter):

		super().__init__(parameter)

		self.schnittstellen = {} # Haben alle Komponenten Schnittstellen oder nur Computer?

		# Standart-Parameter setzen, falls nichts vorhanden
		if KEY_SCHNITTSTELLEN not in self.p.keys():
			self.p[KEY_SCHNITTSTELLEN] = {}
		if KEY_ETHERNET not in self.p[KEY_SCHNITTSTELLEN].keys():
			self.p[KEY_SCHNITTSTELLEN][KEY_ETHERNET] = []
		if KEY_ORT not in self.p.keys():
			self.p[KEY_ORT] = {}
		if KEY_STANDORT not in self.p[KEY_ORT].keys():
			self.p[KEY_ORT][KEY_STANDORT] = '' # TODO Gibt es eine Vorgabe?
		if KEY_HAUS not in self.p[KEY_ORT].keys():
			self.p[KEY_ORT][KEY_HAUS] = ''
		if KEY_RAUM not in self.p[KEY_ORT].keys():
			self.p[KEY_ORT][KEY_RAUM] = ''
		if KEY_META not in self.p[KEY_ORT].keys():
			self.p[KEY_ORT][KEY_META] = ''
		if KEY_BETRIEBSSYSTEM not in self.p.keys():
			self.p[KEY_BETRIEBSSYSTEM] = KEY_UNBEKANNT
		if KEY_HIERARCHIEEBENE not in self.p.keys():
			self.p[KEY_HIERARCHIEEBENE] = KEY_RAUM

		# Schnittstellen erstellen, falls die Parameter das vorgeben
		for ethernet_port in self.p[KEY_SCHNITTSTELLEN][KEY_ETHERNET]:
			neue_schnittstelle = schnittstelle_ethernet(ethernet_port)
			self.schnittstellen[neue_schnittstelle.p[KEY_NAME]] = neue_schnittstelle

		# TODO wifi, usb, firewire


	def __zeichne_schnittstellen__(self, svg):

		for schluessel_schnittstelle in list(self.schnittstellen.keys()):
			self.schnittstellen[schluessel_schnittstelle].__zeichne_schnittstelle__(svg)


	def __korrigiere_positionen__(self):

		for schluessel_schnittstelle in list(self.schnittstellen.keys()):
			ding = self.schnittstellen[schluessel_schnittstelle]
			for dimension in [KEY_X, KEY_Y]:
				ding.svg[dimension] += self.svg[dimension]
			ding.__korrigiere_positionen__()


# Computer jedweder Art
class komponente_computer(komponente):

	def __init__(self, parameter):

		super().__init__(parameter)


	def rendere_svg(self, parameter):

		svg = []
		self.svg = parameter

		# Vertikale Position auf linker Seite
		links_y = PARAM_ABSTAND_KLEIN

		# Horizontale Position in Mitte
		mitte_x = 0

		# Netzwerkschnittstellen (auf linker Seite)
		schnittstellen_keys = list(self.schnittstellen.keys())
		schnittstellen_keys.sort()
		for schnittstelle in schnittstellen_keys:
			if self.schnittstellen[schnittstelle].p[KEY_TYP] == KEY_ETHERNET:
				self.schnittstellen[schnittstelle].rendere_svg({KEY_X: mitte_x, KEY_Y: links_y})
				svg.append(self.schnittstellen[schnittstelle].svg[KEY_SVG])
				links_y += self.schnittstellen[schnittstelle].svg[KEY_HOEHE] + PARAM_ABSTAND_KLEIN

		# Abstand zwischen Netzwerk-Schnittstellen und Meta-Informationen anpassen
		links_y += PARAM_ABSTAND_KLEIN

		# Meta-Informationen zusammenstellen
		metainformation = [
			{KEY_SCHRIFTGROESSE: PARAM_ETHERNET_SCHRIFTGROESSE, KEY_TEXT: self.p[KEY_TYP] + ' in ' + self.p[KEY_ORT][KEY_RAUM]},
			{KEY_SCHRIFTGROESSE: PARAM_NAME_SCHRIFTGROESSE, KEY_TEXT: self.p[KEY_NAME]}
			]
		if self.p[KEY_TYP] not in [KEY_DRUCKER]:
			metainformation.append({KEY_SCHRIFTGROESSE: PARAM_ETHERNET_SCHRIFTGROESSE, KEY_TEXT: 'OS: ' + self.p[KEY_BETRIEBSSYSTEM]})
		if KEY_FIRMWARE in self.p.keys():
			metainformation.append({KEY_SCHRIFTGROESSE: PARAM_ETHERNET_SCHRIFTGROESSE, KEY_TEXT: 'FW: ' + self.p[KEY_FIRMWARE]})
		if KEY_SERIENNUMMER in self.p.keys():
			metainformation.append({KEY_SCHRIFTGROESSE: PARAM_ETHERNET_SCHRIFTGROESSE, KEY_TEXT: 'SN: ' + self.p[KEY_SERIENNUMMER]})
		if KEY_BEZEICHNUNG in self.p.keys():
			metainformation.append({KEY_SCHRIFTGROESSE: PARAM_ETHERNET_SCHRIFTGROESSE, KEY_TEXT: 'BZ: ' + self.p[KEY_BEZEICHNUNG]})

		# Meta-Informationen ausgeben
		for element in metainformation:
			links_y += element[KEY_SCHRIFTGROESSE]
			svg.append('<text x="%d" y="%d" font-family="%s" font-size="%d" fill="%s" dominant-baseline="middle">%s</text>' % (
				PARAM_ABSTAND_KLEIN, links_y - (element[KEY_SCHRIFTGROESSE] / 2), PARAM_TEXT_FONT, element[KEY_SCHRIFTGROESSE], PARAM_TEXT_FARBE, element[KEY_TEXT]
				))

		# Höhe des Elementes bestimmen (TODO links/rechts prüfen)
		hoehe = links_y + PARAM_ABSTAND_KLEIN

		# Hintergrund
		svg.insert(0, '<rect x="%d" y="%d" width="%d" height="%d" fill="%s" />' % (0, 0, PARAM_COMPUTER_BREITE, hoehe, PARAM_COMPUTER_FARBE))

		# Parameter zur Rückgabe vorbereiten
		self.svg.update({
			KEY_BREITE: PARAM_COMPUTER_BREITE,
			KEY_HOEHE: hoehe
			})

		# SVG fertig machen
		self.__vervollstaendige_svg__(svg)


# Arbeitsplatzcomputer
class komponente_computer_arbeitsplatz(komponente_computer):

	def __init__(self, parameter):

		super().__init__(parameter)


# Netzwerk-Drucker werden wie Computer behandelt
class komponente_computer_drucker(komponente_computer):

	def __init__(self, parameter):

		super().__init__(parameter)


# Kopflos
class komponente_computer_kopflos(komponente_computer):

	def __init__(self, parameter):

		super().__init__(parameter)


# Smartphone
class komponente_computer_smartphone(komponente_computer):

	def __init__(self, parameter):

		super().__init__(parameter)


# Ein Switch, Sonderfall eines Computers
class komponente_computer_switch(komponente_computer):

	def __init__(self, parameter):

		super().__init__(parameter)

		# Standart-Parameter setzen, falls nichts vorhanden
		if KEY_MASKE not in self.p.keys():
			self.p[KEY_MASKE] = '%02d'
		if KEY_PREFIX not in self.p.keys():
			self.p[KEY_PREFIX] = ''
		if KEY_SUFFIX not in self.p.keys():
			self.p[KEY_SUFFIX] = ''
		if KEY_MIN not in self.p.keys():
			self.p[KEY_MIN] = 1
		if KEY_MAX not in self.p.keys():
			self.p[KEY_MAX] = 24
		if KEY_MAC not in self.p.keys():
			self.p[KEY_MAC] = DEFAULT_MAC

		# Ethernet-Ports für Switch anlegen
		if KEY_UNTERBRECHUNG_MIN in self.p.keys() and KEY_UNTERBRECHUNG_MAX in self.p.keys():
			port_range = list(
					range(self.p[KEY_MIN], self.p[KEY_UNTERBRECHUNG_MIN])
				) + list(
					range(self.p[KEY_UNTERBRECHUNG_MAX] + 1, self.p[KEY_MAX] + 1)
				)
		else:
			port_range = range(self.p[KEY_MIN], self.p[KEY_MAX] + 1)
		for index in port_range:
			port_name = self.p[KEY_PREFIX] + (self.p[KEY_MASKE] % index) + self.p[KEY_SUFFIX]
			self.schnittstellen[port_name] = schnittstelle_ethernet({
				KEY_NAME: port_name,
				KEY_NUMMER: index,
				KEY_PASSIV: True,
				KEY_POSITION: KEY_FRONT
				})


	def rendere_svg(self, parameter):

		svg = []
		self.svg = parameter

		# Vertikale Position auf linker Seite
		links_y = PARAM_ABSTAND_KLEIN

		# Meta-Informationen
		zeile = self.p[KEY_TYP]
		if self.p[KEY_ORT][KEY_RAUM] != '':
			zeile += ' in ' + self.p[KEY_ORT][KEY_RAUM]
		for element in [
			{KEY_SCHRIFTGROESSE: PARAM_ETHERNET_SCHRIFTGROESSE, KEY_TEXT: zeile},
			{KEY_SCHRIFTGROESSE: PARAM_NAME_SCHRIFTGROESSE, KEY_TEXT: self.p[KEY_NAME]}
			]:
			links_y += element[KEY_SCHRIFTGROESSE]
			svg.append(
				'<text x="%d" y="%d" font-family="%s" font-size="%d" fill="%s" dominant-baseline="middle">%s</text>' % (
					PARAM_ABSTAND_KLEIN, links_y - (element[KEY_SCHRIFTGROESSE] / 2), PARAM_TEXT_FONT, element[KEY_SCHRIFTGROESSE], PARAM_TEXT_FARBE, element[KEY_TEXT]
					)
				)

		# Abstand zu den Ethernet-Ports
		links_y += PARAM_ABSTAND_KLEIN

		# Horizontale Position auf unterer Seite
		unten_x = PARAM_ABSTAND_KLEIN

		# Netzwerkschnittstellen (auf linker Seite)
		schnittstellen_keys = list(self.schnittstellen.keys())
		schnittstellen_keys.sort()
		for schnittstelle in schnittstellen_keys:
			if self.schnittstellen[schnittstelle].p[KEY_TYP] == KEY_ETHERNET:
				self.schnittstellen[schnittstelle].rendere_svg({KEY_X: unten_x, KEY_Y: links_y})
				svg.append(self.schnittstellen[schnittstelle].svg[KEY_SVG])
				unten_x += self.schnittstellen[schnittstelle].svg[KEY_BREITE] + PARAM_ABSTAND_KLEIN

		# Breite und Höhe des Elementes bestimmen (TODO ???)
		hoehe = links_y + self.schnittstellen[schnittstelle].svg[KEY_HOEHE]
		breite = unten_x

		# Hintergrund
		svg.insert(0, '<rect x="%d" y="%d" width="%d" height="%d" fill="%s" />' % (0, 0, breite, hoehe, PARAM_COMPUTER_FARBE))

		# Parameter zur Rückgabe vorbereiten
		self.svg.update({
			KEY_BREITE: breite,
			KEY_HOEHE: hoehe
			})

		# SVG fertig machen
		self.__vervollstaendige_svg__(svg)


# Ein Hub, Sonderfall eines Switches, Sonderfall eines Computers
class komponente_computer_switch_hub(komponente_computer_switch):

	def __init__(self, parameter):

		super().__init__(parameter)
