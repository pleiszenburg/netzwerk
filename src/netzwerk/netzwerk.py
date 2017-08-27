# -*- coding: utf-8 -*-

"""

NETZWERK
Computer network renderer
https://github.com/pleiszenburg/netzwerk

	src/netzwerk/netzwerk.py: Klasse zur Repräsentation eines Netzwerkes

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
from .darstellung import darstellung_ebene
from .element import element
from .komponente import (
	komponente_computer_arbeitsplatz,
	komponente_computer_drucker,
	komponente_computer_switch_hub,
	komponente_computer_kopflos,
	komponente_computer_smartphone,
	komponente_computer_switch
	)
from .uebergang import (
	uebergang_dose,
	uebergang_loch,
	uebergang_vorbereitet,
	verbindung_patchfeld
	)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# KLASSEN
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

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
