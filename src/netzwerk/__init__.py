# -*- coding: utf-8 -*-

"""

NETZWERK
Computer network renderer
https://github.com/pleiszenburg/netzwerk

	src/netzwerk/__init__.py: Module init

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
from pprint import pprint as pp






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


# Alle Elemente einer Darstellung basieren auf dieser Basis-Klasse
class darstellung(element):

	def __init__(self, parameter):

		super().__init__(parameter)


# Darstellung von Hierarchie-Ebene
class darstellung_ebene(darstellung):

	def __init__(self, parameter):

		super().__init__(parameter)

		# Standart-Parameter setzen, falls nichts vorhanden
		if KEY_HIERARCHIEEBENE not in self.p.keys():
			self.p[KEY_HIERARCHIEEBENE] = PARAM_EBENEN[0] # Global gibt es per Definition nur einmal
		if KEY_ELTERN not in self.p.keys():
			self.p[KEY_ELTERN] = KEY_UNDEFINIERT # Global hat undefinierte Eltern
		if KEY_NAME not in self.p.keys():
			self.p[KEY_NAME] = PARAM_EBENEN[0] # Trägt sonst den Namen von Standorten, Häusern, Räumen
		if KEY_BAUM not in self.p.keys():
			self.__baue_struktur_baum__()

		# Basis-Struktur einer Ebene aufbauen
		self.p.update({
			KEY_TYP: KEY_DARSTELLUNG,
			KEY_HORIZONTAL: { # Spaltenweise
				KEY_KNICKE: 0,
				KEY_SWITCHEBENE: 0,
				KEY_INTER: 0,
				KEY_KOMPONENTENEBENE: 0
				},
			KEY_VERTIKAL: { # Zeilenweise,
				KEY_META: 0, # Informationen wie Name über jeweiligen Ort
				KEY_SWITCHEBENE: 0,
				KEY_INTER: 0,
				KEY_DOSENEBENE: 0,
				KEY_KOMPONENTENEBENE: 0, # Entweder Komponenten oder Ausgänge ist größer ...
				KEY_AUSGAENGE: 0
				},
			KEY_SWITCHES: [], # Switches, Hubs
			KEY_DOSEN: [], # Dosen, die zu Patchfeldern auf Haus-, Standort- oder globaler Ebene gehören
			KEY_KINDER: [], # Weitere Ebenen oder Komponenten
			KEY_AUSGAENGE: [] # Dosen, sonstige Übergänge,
			})

		# Felder für horizontale Maxima hinzufügen, falls es keine Referenz gibt
		if KEY_MAX not in self.p.keys():
			self.__horizontaler_platz_felder__()

		# Basis für SVG schaffen
		self.svg.update({
			KEY_BREITE: 0,
			KEY_HOEHE: 0,
			KEY_SVG: ''
		})

		# Komponenten als Kinder dieser Ebene zuordnen
		self.__finde_meine_komponenten__()

		# Meine Komponenten rendern
		self.__rendere_meine_komponenten__()

		# "Erste" Rekursion, von oben nach unten: Ebenen als Kinder dieser Ebene erstellen
		self.__erstelle_meine_kinder__()

		# "Zweite und dritte" Rekursion, von unten nach oben: Ebenen rendern
		if self.p[KEY_HIERARCHIEEBENE] == PARAM_EBENEN[0]:
			self.__rendere_svg_global__()

		# "Vierte" Rekursion, von oben nach unten: Positionen korrigieren
		if self.p[KEY_HIERARCHIEEBENE] == PARAM_EBENEN[0]:
			self.__korrigiere_positionen__()

		# "Fünfte" Rekursion, von oben nach unten: Schnittstellen zeichnen
		if self.p[KEY_HIERARCHIEEBENE] == PARAM_EBENEN[0]:
			self.__zeichne_schnittstellen__(self.svg[KEY_SVG])



		# TODO Kabel und Stecker kämen hier - für globale Ebene ist self.svg[KEY_SVG] hier noch eine Liste

		# Verbindungen zeichnen
		if self.p[KEY_HIERARCHIEEBENE] == PARAM_EBENEN[0]:
			self.__test_zeichne_verbindungen__(self.svg[KEY_SVG])



		# Falls das hier global ist, SVG vervollständigen
		if self.p[KEY_HIERARCHIEEBENE] == PARAM_EBENEN[0]:
			self.__vervollstaendige_svg__(self.svg[KEY_SVG], True)


	def __test_zeichne_verbindungen__(self, svg):

		linie = '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="%d" stroke-linecap="round" />'

		for verbindung in self.p[KEY_VERBINDUNGEN]:

			orientierungen = []
			for index in range(0, 2):
				orientierungen.append(verbindung[KEY_VERBINDUNG][index][KEY_SCHNITTSTELLE].svg[KEY_STECKER][KEY_ORIENTIERUNG])

			# Klassische 90°-Ecke in Kabel
			if (
				orientierungen[0] in [KEY_OBEN, KEY_UNTEN] and orientierungen[1] in [KEY_LINKS, KEY_RECHTS]
				) or (
				orientierungen[0] in [KEY_LINKS, KEY_RECHTS] and orientierungen[1] in [KEY_OBEN, KEY_UNTEN]
				):

				if orientierungen[0] in [KEY_OBEN, KEY_UNTEN]:
					punkte = [
						[0, 0, 0, 1],
						[0, 1, 1, 1],
						]
				else:
					punkte = [
						[0, 0, 1, 0],
						[1, 0, 1, 1]
						]

				for index in punkte:
					svg.append(linie % (
						verbindung[KEY_VERBINDUNG][index[0]][KEY_SCHNITTSTELLE].svg[KEY_STECKER][KEY_X],
						verbindung[KEY_VERBINDUNG][index[1]][KEY_SCHNITTSTELLE].svg[KEY_STECKER][KEY_Y],
						verbindung[KEY_VERBINDUNG][index[2]][KEY_SCHNITTSTELLE].svg[KEY_STECKER][KEY_X],
						verbindung[KEY_VERBINDUNG][index[3]][KEY_SCHNITTSTELLE].svg[KEY_STECKER][KEY_Y],
						'#FF0000', 2
						))

			# Ein direktes Kabel - Rückfalloption für unbekannte Knick-Sequenzen
			else:

				svg.append(linie % (
					verbindung[KEY_VERBINDUNG][0][KEY_SCHNITTSTELLE].svg[KEY_STECKER][KEY_X],
					verbindung[KEY_VERBINDUNG][0][KEY_SCHNITTSTELLE].svg[KEY_STECKER][KEY_Y],
					verbindung[KEY_VERBINDUNG][1][KEY_SCHNITTSTELLE].svg[KEY_STECKER][KEY_X],
					verbindung[KEY_VERBINDUNG][1][KEY_SCHNITTSTELLE].svg[KEY_STECKER][KEY_Y],
					'#FF0000', 2
					))


	def __zeichne_schnittstellen__(self, svg):

		for ding in (self.p[KEY_SWITCHES] + self.p[KEY_DOSEN] + self.p[KEY_KINDER] + self.p[KEY_AUSGAENGE]):
			ding.__zeichne_schnittstellen__(svg)


	def __korrigiere_positionen__(self):

		for ding in (self.p[KEY_SWITCHES] + self.p[KEY_DOSEN] + self.p[KEY_KINDER] + self.p[KEY_AUSGAENGE]):
			for dimension in [KEY_X, KEY_Y]:
				ding.svg[dimension] += self.svg[dimension]
			ding.__korrigiere_positionen__()


	def __rendere_svg_global__(self):

		# Eine Liste aller Objekte der Klasse Ebene aufstellen
		ebenen_liste = []
		self.__liste_mich_und_meine_kinder__(ebenen_liste)

		# Alle Räume einer Hierarchie-Ebene rendern, über Ortsgrenzen hinweg, und dann nach oben steigen
		for index, hierarchieebene in reversed(list(enumerate(PARAM_EBENEN))):

			# Über alle Objekte der Klasse Ebene laufen - Platzbedarf bestimmen
			for ebene in ebenen_liste:

				# Ebenen der betreffenden Hierarchie-Stufe herausfischen
				if ebene.p[KEY_HIERARCHIEEBENE] == hierarchieebene:

					# Ebene rendern
					ebene.__bestimme_mindesten_platzbedarf_in_mir__()

			# Über alle Objekte der Klasse Ebene laufen - Rendern
			for ebene in ebenen_liste:

				# Ebenen der betreffenden Hierarchie-Stufe herausfischen
				if ebene.p[KEY_HIERARCHIEEBENE] == hierarchieebene:

					# Ebene rendern - falls sie etwas enthält
					if len(ebene.p[KEY_SWITCHES]) > 0 or len(ebene.p[KEY_DOSEN]) > 0 or len(ebene.p[KEY_KINDER]) > 0 or len(ebene.p[KEY_AUSGAENGE]) > 0:
						ebene.__rendere_mich_selbst__()


	def __liste_mich_und_meine_kinder__(self, ebenen_liste):

		ebenen_liste.append(self)
		for kind in self.p[KEY_KINDER]:
			if kind.p[KEY_TYP] == KEY_DARSTELLUNG:
				kind.__liste_mich_und_meine_kinder__(ebenen_liste)


	def __rendere_mich_selbst__(self):

		# Initialisieren
		x = 0
		y = 0
		svg = []

		# Links Platz für Wand-Linie schaffen
		x += PARAM_DOSE_BREITE + PARAM_ABSTAND
		# Oben Platz für Wand-Linie schaffen
		y += 2 * PARAM_ABSTAND

		# Meta ausgeben
		meta_x = x - PARAM_DOSE_BREITE / 2
		svg.append(
			'<text x="%d" y="%d" font-family="%s" font-size="%d" fill="%s" dominant-baseline="middle">%s</text>' % (
				meta_x, y + PARAM_RAUM_SCHRIFTGROESSE / 2, PARAM_TEXT_FONT, PARAM_RAUM_SCHRIFTGROESSE, PARAM_TEXT_FARBE, self.p[KEY_NAME]
				)
			)

		# Switch-Ebene starten lassen
		switch_x = x
		if self.p[KEY_MAX][self.p[KEY_HIERARCHIEEBENE]][KEY_KNICKE] != 0:
			switch_x += self.p[KEY_MAX][self.p[KEY_HIERARCHIEEBENE]][KEY_KNICKE] + PARAM_ABSTAND
		switch_y = y
		if self.p[KEY_VERTIKAL][KEY_META] != 0:
			switch_y += self.p[KEY_VERTIKAL][KEY_META] + PARAM_ABSTAND

		# Switch-Ebene zeichnen
		self.__sortiere_liste_von_elementen__(self.p[KEY_SWITCHES], KEY_NAME)
		for switch in self.p[KEY_SWITCHES]:
			switch.__fixiere_element__({
				KEY_X: switch_x,
				KEY_Y: switch_y
				})
			switch_x += switch.svg[KEY_BREITE] + PARAM_ABSTAND
			svg.append(switch.svg[KEY_SVG])

		# Patchfeld-Ebene (Dosen) starten lassen
		dosen_x = x
		if self.p[KEY_MAX][self.p[KEY_HIERARCHIEEBENE]][KEY_KNICKE] != 0:
			dosen_x += self.p[KEY_MAX][self.p[KEY_HIERARCHIEEBENE]][KEY_KNICKE] + PARAM_ABSTAND
		dosen_y = y
		if self.p[KEY_VERTIKAL][KEY_META] != 0:
			dosen_y += self.p[KEY_VERTIKAL][KEY_META] + PARAM_ABSTAND
		if self.p[KEY_VERTIKAL][KEY_SWITCHEBENE] != 0:
			dosen_y += self.p[KEY_VERTIKAL][KEY_SWITCHEBENE] + PARAM_ABSTAND
		if self.p[KEY_VERTIKAL][KEY_INTER] != 0:
			dosen_y += self.p[KEY_VERTIKAL][KEY_INTER] + PARAM_ABSTAND

		# Patchfeld-Ebene zeichnen
		self.__sortiere_liste_von_elementen__(self.p[KEY_DOSEN], KEY_NAME)
		for dose in self.p[KEY_DOSEN]:
			dose.__fixiere_element__({
				KEY_X: dosen_x,
				KEY_Y: dosen_y
				})
			dosen_x += dose.svg[KEY_BREITE] + PARAM_ABSTAND_KLEIN
			svg.append(dose.svg[KEY_SVG])

		# Ausgangsebene (Dosen und Löcher in den Wänden) starten
		ausgang_x = 0
		ausgang_y = y
		if self.p[KEY_VERTIKAL][KEY_META] != 0:
			ausgang_y += self.p[KEY_VERTIKAL][KEY_META] + PARAM_ABSTAND
		if self.p[KEY_VERTIKAL][KEY_SWITCHEBENE] != 0:
			ausgang_y += self.p[KEY_VERTIKAL][KEY_SWITCHEBENE] + PARAM_ABSTAND
		if self.p[KEY_VERTIKAL][KEY_INTER] != 0:
			ausgang_y += self.p[KEY_VERTIKAL][KEY_INTER] + PARAM_ABSTAND
		if self.p[KEY_VERTIKAL][KEY_DOSENEBENE] != 0:
			ausgang_y += self.p[KEY_VERTIKAL][KEY_DOSENEBENE] + PARAM_ABSTAND

		# Ausgangsebene zeichnen
		self.__sortiere_liste_von_elementen__(self.p[KEY_AUSGAENGE], KEY_NAME)
		for ausgang in self.p[KEY_AUSGAENGE]:
			ausgang.__fixiere_element__({
				KEY_X: ausgang_x,
				KEY_Y: ausgang_y
				})
			ausgang_y += ausgang.svg[KEY_HOEHE] + PARAM_ABSTAND_KLEIN
			svg.append(ausgang.svg[KEY_SVG])

		# Kinder-Ebene starten
		kinder_x = x
		if self.p[KEY_MAX][self.p[KEY_HIERARCHIEEBENE]][KEY_KNICKE] != 0:
			kinder_x += self.p[KEY_MAX][self.p[KEY_HIERARCHIEEBENE]][KEY_KNICKE] + PARAM_ABSTAND
		if self.p[KEY_MAX][self.p[KEY_HIERARCHIEEBENE]][KEY_SWITCHEBENE] != 0:
			kinder_x += self.p[KEY_MAX][self.p[KEY_HIERARCHIEEBENE]][KEY_SWITCHEBENE] + PARAM_ABSTAND
		if self.p[KEY_MAX][self.p[KEY_HIERARCHIEEBENE]][KEY_INTER] != 0:
			kinder_x += self.p[KEY_MAX][self.p[KEY_HIERARCHIEEBENE]][KEY_INTER] + PARAM_ABSTAND
		if self.p[KEY_MAX][self.p[KEY_HIERARCHIEEBENE]][KEY_KOMPONENTENEBENE] != 0:
			kinder_x += self.p[KEY_MAX][self.p[KEY_HIERARCHIEEBENE]][KEY_KOMPONENTENEBENE] # Ohne Abstand: von Rechts positioniert!
		kinder_y = y
		if self.p[KEY_VERTIKAL][KEY_META] != 0:
			kinder_y += self.p[KEY_VERTIKAL][KEY_META] + PARAM_ABSTAND
		if self.p[KEY_VERTIKAL][KEY_SWITCHEBENE] != 0:
			kinder_y += self.p[KEY_VERTIKAL][KEY_SWITCHEBENE] + PARAM_ABSTAND
		if self.p[KEY_VERTIKAL][KEY_INTER] != 0:
			kinder_y += self.p[KEY_VERTIKAL][KEY_INTER] + PARAM_ABSTAND
		if self.p[KEY_VERTIKAL][KEY_DOSENEBENE] != 0:
			kinder_y += self.p[KEY_VERTIKAL][KEY_DOSENEBENE] + PARAM_ABSTAND

		# Kinder-Ebene zeichnen
		self.__sortiere_liste_von_elementen__(self.p[KEY_KINDER], KEY_NAME)
		for kind in self.p[KEY_KINDER]:
			if kind.p[KEY_TYP] != KEY_DARSTELLUNG:
				kind.__fixiere_element__({
					KEY_X: kinder_x - kind.svg[KEY_BREITE],
					KEY_Y: kinder_y
					})
				kinder_y += kind.svg[KEY_HOEHE] + PARAM_ABSTAND
				svg.append(kind.svg[KEY_SVG])
		for kind in self.p[KEY_KINDER]:
			if kind.p[KEY_TYP] == KEY_DARSTELLUNG:
				kind.__fixiere_element__({
					KEY_X: kinder_x - kind.svg[KEY_BREITE],
					KEY_Y: kinder_y
					})
				kinder_y += kind.svg[KEY_HOEHE] + PARAM_ABSTAND
				svg.append(kind.svg[KEY_SVG])

		# Eigene Hoehe und Breite sind Nebenprodukte
		if (kinder_y + PARAM_ABSTAND) > (ausgang_y + 2 * PARAM_ABSTAND - PARAM_ABSTAND_KLEIN):
			self.svg[KEY_HOEHE] = kinder_y + PARAM_ABSTAND
		else:
			self.svg[KEY_HOEHE] = ausgang_y + 2 * PARAM_ABSTAND - PARAM_ABSTAND_KLEIN
		self.svg[KEY_BREITE] = kinder_x

		# Eigene Breite in maximalen Breiten der Kinder eine Ebene höher vermerken, falls wir nicht schon global sind
		if self.p[KEY_HIERARCHIEEBENE] != PARAM_EBENEN[0]:
			if self.p[KEY_MAX][PARAM_EBENEN[PARAM_EBENEN.index(self.p[KEY_HIERARCHIEEBENE]) - 1]][KEY_KOMPONENTENEBENE] < self.svg[KEY_BREITE]:
				self.p[KEY_MAX][PARAM_EBENEN[PARAM_EBENEN.index(self.p[KEY_HIERARCHIEEBENE]) - 1]][KEY_KOMPONENTENEBENE] = self.svg[KEY_BREITE]

		# Raum einen Rahmen geben
		linie = '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#80DD80" stroke-width="4" stroke-linecap="round" />'
		for koordinaten in [
			(PARAM_DOSE_BREITE / 2, PARAM_ABSTAND, self.svg[KEY_BREITE], PARAM_ABSTAND),
			(PARAM_DOSE_BREITE / 2, self.svg[KEY_HOEHE] - PARAM_ABSTAND, self.svg[KEY_BREITE], self.svg[KEY_HOEHE] - PARAM_ABSTAND),
			(PARAM_DOSE_BREITE / 2, PARAM_ABSTAND, PARAM_DOSE_BREITE / 2, self.svg[KEY_HOEHE] - PARAM_ABSTAND)
			]:
			svg.insert(0, linie % koordinaten)

		# SVG abschließen - außer wenn es global ist, dann wird nur die Liste gesichert
		if self.p[KEY_HIERARCHIEEBENE] != PARAM_EBENEN[0]:
			self.__vervollstaendige_svg__(svg)
		else:
			self.svg[KEY_X] = 0
			self.svg[KEY_Y] = 0
			self.svg[KEY_SVG] = svg


	def __horizontaler_platz_felder__(self):

		self.p[KEY_MAX] = {}
		for ebene in PARAM_EBENEN:
			self.p[KEY_MAX].update({ebene: {}})
			for parameter in list(self.p[KEY_HORIZONTAL].keys()):
				self.p[KEY_MAX][ebene][parameter] = 0


	def __bestimme_mindesten_platzbedarf_in_mir__(self):

		# HOEHE: Meta - entspricht Schriftgröße
		self.p[KEY_VERTIKAL][KEY_META] = PARAM_RAUM_SCHRIFTGROESSE
		# HOEHE: Switches - höchster gewinnt
		for switch in self.p[KEY_SWITCHES]:
			if self.p[KEY_VERTIKAL][KEY_SWITCHEBENE] < switch.svg[KEY_HOEHE]:
				self.p[KEY_VERTIKAL][KEY_SWITCHEBENE] = switch.svg[KEY_HOEHE]
		# HOEHE: Inter - Anzahl der Inter-Switch-Verbindungen mal Abstand
		self.p[KEY_VERTIKAL][KEY_INTER] = 0 # TODO
		# HOEHE: Dosen - höchste gewinnt
		for dosen in self.p[KEY_DOSEN]:
			if self.p[KEY_VERTIKAL][KEY_DOSENEBENE] < dosen.svg[KEY_HOEHE]:
				self.p[KEY_VERTIKAL][KEY_DOSENEBENE] = dosen.svg[KEY_HOEHE]
		# HOEHE: Komponenten / Kinder - Summe ihrer Höhe plus Summe-1 mal Abstand
		for kind in self.p[KEY_KINDER]:
			self.p[KEY_VERTIKAL][KEY_KOMPONENTENEBENE] += kind.svg[KEY_HOEHE]
		if len(self.p[KEY_KINDER]) > 1:
			self.p[KEY_VERTIKAL][KEY_KOMPONENTENEBENE] += (len(self.p[KEY_KINDER]) - 1) * PARAM_ABSTAND

		# BREITE: Knicke - Anzahl der Dosen mal Abstand
		self.p[KEY_HORIZONTAL][KEY_KNICKE] = len(self.p[KEY_AUSGAENGE]) * PARAM_ABSTAND
		# BREITE: Switches - Summe ihrer Breite plus Summe-1 mal Abstand
		for switch in self.p[KEY_SWITCHES]:
			self.p[KEY_HORIZONTAL][KEY_SWITCHEBENE] += switch.svg[KEY_BREITE]
		if len(self.p[KEY_SWITCHES]) > 1:
			self.p[KEY_HORIZONTAL][KEY_SWITCHEBENE] += (len(self.p[KEY_SWITCHES]) - 1) * PARAM_ABSTAND
		# BREITE: Inter - Anzahl der Inter-Kinder-Verbindungen mal Abstand
		self.p[KEY_HORIZONTAL][KEY_INTER] = 0 # TODO
		# BREITE: Komponenten / Kinder - breitestes gewinnt
		for kind in self.p[KEY_KINDER]:
			if self.p[KEY_HORIZONTAL][KEY_KOMPONENTENEBENE] < kind.svg[KEY_BREITE]:
				self.p[KEY_HORIZONTAL][KEY_KOMPONENTENEBENE] = kind.svg[KEY_BREITE]

		# Horizontale Werte in globaler Tabelle notieren
		for spalte in list(self.p[KEY_HORIZONTAL].keys()):
			if self.p[KEY_MAX][self.p[KEY_HIERARCHIEEBENE]][spalte] < self.p[KEY_HORIZONTAL][spalte]:
				self.p[KEY_MAX][self.p[KEY_HIERARCHIEEBENE]][spalte] = self.p[KEY_HORIZONTAL][spalte]


	def __erstelle_meine_kinder__(self):

		for ort in list(self.p[KEY_BAUM].keys()):
			self.p[KEY_KINDER].append(darstellung_ebene({
				KEY_NAME: ort,
				KEY_ELTERN: self.p[KEY_NAME],
				KEY_HIERARCHIEEBENE: PARAM_EBENEN[PARAM_EBENEN.index(self.p[KEY_HIERARCHIEEBENE]) + 1],
				KEY_BAUM: self.p[KEY_BAUM][ort],
				KEY_KOMPONENTEN: self.p[KEY_KOMPONENTEN],
				KEY_VERBINDUNGEN: self.p[KEY_VERBINDUNGEN],
				KEY_MAX: self.p[KEY_MAX]
				}))


	def __finde_meine_komponenten__(self):

		# Durch alle Komponenten des Netzwerkes laufen
		for komponente in list(self.p[KEY_KOMPONENTEN].keys()):

			# Liegt dieses Element in meiner Ebene?
			if self.p[KEY_KOMPONENTEN][komponente].p[KEY_HIERARCHIEEBENE] == self.p[KEY_HIERARCHIEEBENE]:

				# Prüfung des Ortes ...
				richtiger_ort = False

				# Globales Element
				if self.p[KEY_NAME] == PARAM_EBENEN[0]:

					# Immer ein Treffer
					richtiger_ort = True

				# Element mit Standort
				else:

					# Gibt es die Ortsebene?
					if self.p[KEY_HIERARCHIEEBENE] in self.p[KEY_KOMPONENTEN][komponente].p[KEY_ORT].keys():

						# Richtiger Ort?
						if self.p[KEY_KOMPONENTEN][komponente].p[KEY_ORT][self.p[KEY_HIERARCHIEEBENE]] == self.p[KEY_NAME]:

							# Treffer
							richtiger_ort = True

				# Falls der Ort stimmt ...
				if richtiger_ort:

					# Switches, Hubs ... ?
					if self.p[KEY_KOMPONENTEN][komponente].p[KEY_TYP] in [KEY_SWITCH, KEY_HUB]: # TODO zuordnen

						# In die Liste
						self.p[KEY_SWITCHES].append(self.p[KEY_KOMPONENTEN][komponente])

					# Ausgänge wie Dosen?
					elif self.p[KEY_KOMPONENTEN][komponente].p[KEY_TYP] in [KEY_DOSE, KEY_LOCH, KEY_VORBEREITET]: # TODO zuordnen

						# Ist es eine Dose in der untersten Hierarchie-Ebene?
						if self.p[KEY_KOMPONENTEN][komponente].p[KEY_TYP] == KEY_DOSE and self.p[KEY_HIERARCHIEEBENE] != PARAM_EBENEN[-1]:

							# In die Liste der Dosen
							self.p[KEY_DOSEN].append(self.p[KEY_KOMPONENTEN][komponente])

						else:

							# Sonst in die Liste der Ausgänge
							self.p[KEY_AUSGAENGE].append(self.p[KEY_KOMPONENTEN][komponente])

					# Computer, Kopflos, ...
					elif self.p[KEY_KOMPONENTEN][komponente].p[KEY_TYP] in [KEY_ARBEITSPLATZ, KEY_KOPFLOS, KEY_DRUCKER, KEY_SMARTPHONE]: # TODO zuordnen

						# In die Liste der KINDER (!)
						self.p[KEY_KINDER].append(self.p[KEY_KOMPONENTEN][komponente])

					# Sonstiges
					else:

						pp(komponente.p)
						raise


	def __rendere_meine_komponenten__(self):

		for gruppe in [KEY_KINDER, KEY_SWITCHES, KEY_DOSEN, KEY_AUSGAENGE]:
			for element in self.p[gruppe]:
				element.rendere_svg({})


	def __baue_struktur_baum__(self):

		self.p[KEY_BAUM] = {}

		# TODO rekursiv mit PARAM_EBENEN
		for komponente in list(self.p[KEY_KOMPONENTEN].keys()):

			ort = self.p[KEY_KOMPONENTEN][komponente].p[KEY_ORT]

			if ort[KEY_STANDORT] != '' and ort[KEY_STANDORT] not in self.p[KEY_BAUM].keys():
				self.p[KEY_BAUM][ort[KEY_STANDORT]] = {}
			if ort[KEY_HAUS] != '' and ort[KEY_HAUS] not in self.p[KEY_BAUM][ort[KEY_STANDORT]].keys():
				self.p[KEY_BAUM][ort[KEY_STANDORT]][ort[KEY_HAUS]] = {}
			if ort[KEY_RAUM] != '' and ort[KEY_RAUM] not in self.p[KEY_BAUM][ort[KEY_STANDORT]][ort[KEY_HAUS]].keys():
				self.p[KEY_BAUM][ort[KEY_STANDORT]][ort[KEY_HAUS]][ort[KEY_RAUM]] = {}


# Ein Netzwerk
class netzwerk(element):

	def __init__(self, parameter):

		super().__init__(parameter)

		self.komponenten = {}
		self.verbindungen = []


	def erstelle_komponente(self, komponente):

		typ_klasse = {
			KEY_ARBEITSPLATZ: komponente_computer_arbeitsplatz,
			KEY_DOSE: uebergang_dose,
			KEY_DRUCKER: komponente_computer_drucker,
			KEY_HUB: komponente_computer_switch_hub,
			KEY_KOPFLOS: komponente_computer_kopflos,
			KEY_LOCH: uebergang_loch,
			KEY_PATCHFELD: verbindung_patchfeld,
			KEY_SMARTPHONE: komponente_computer_smartphone,
			KEY_SWITCH: komponente_computer_switch,
			KEY_VORBEREITET: uebergang_vorbereitet
			}

		objekte = typ_klasse[komponente[KEY_TYP]](komponente)

		if type(objekte) == list:
			for objekt in objekte:
				self.komponenten.update({
					objekt.p[KEY_NAME]: objekt
					})
		else:
			self.komponenten.update({
				objekte.p[KEY_NAME]: objekte
				})


	def verbinde_komponenten(self, parameter):

		# Über jedes "Kabel" laufen und Wege mit mehr als Zwei Knoten zerlegen
		for index in range(1, len(parameter), 2):

			# Namen der Schnittstelle am Anfang finden
			if KEY_SCHNITTSTELLE in parameter[index - 1].keys():
				anfang_schnittstelle_name = parameter[index - 1][KEY_SCHNITTSTELLE]
			elif KEY_SCHNITTSTELLEN in parameter[index - 1].keys():
				anfang_schnittstelle_name = parameter[index - 1][KEY_SCHNITTSTELLEN][1]
			else:
				raise

			# Namen der Schnittstelle am Ende finden
			if KEY_SCHNITTSTELLE in parameter[index + 1].keys():
				ende_schnittstelle_name = parameter[index + 1][KEY_SCHNITTSTELLE]
			elif KEY_SCHNITTSTELLEN in parameter[index + 1].keys():
				ende_schnittstelle_name = parameter[index + 1][KEY_SCHNITTSTELLEN][0]
			else:
				raise

			# Referenzen auf Objekte finden
			anfang = self.komponenten[parameter[index - 1][KEY_NAME]]
			anfang_schnittstelle = anfang.schnittstellen[anfang_schnittstelle_name]
			ende = self.komponenten[parameter[index + 1][KEY_NAME]]
			ende_schnittstelle = ende.schnittstellen[ende_schnittstelle_name]

			# Ist der Typ, beispielsweise Ethernet gleich? Nein: Fehler!
			if anfang_schnittstelle.p[KEY_TYP] != ende_schnittstelle.p[KEY_TYP]:
				raise

			# Verbindung in Liste eintragen
			self.verbindungen.append({
				KEY_VERBINDUNG: [
					{
						KEY_KOMPONENTE: anfang,
						KEY_SCHNITTSTELLE: anfang_schnittstelle
						},
					{
						KEY_KOMPONENTE: ende,
						KEY_SCHNITTSTELLE: ende_schnittstelle
						}
					],
				KEY_META: parameter[index]
				})


	def rendere_netzwerk(self, dateiname):

		# Struktur der zukünftigen Darstellung erfassen und rendern
		self.struktur = darstellung_ebene({
			KEY_HIERARCHIEEBENE: KEY_GLOBAL,
			KEY_KOMPONENTEN: self.komponenten,
			KEY_VERBINDUNGEN: self.verbindungen
			})

		# SVG in Datei schreiben
		self.struktur.schreibe_svg(dateiname)
