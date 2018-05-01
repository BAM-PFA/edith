#!/usr/bin/env python3

import os
import subprocess
import sys

import pyltopersFunctions


def stuff():
	system = pyltopersFunctions.get_system()
	foundDecks = find_decks(system)

	if len(foundDecks) > 1:
		knownDecks = []
		for deck in foundDecks:
			knownDecks.append("")
		deckIdToFormat = input("Which deck:")


def main(_args):
	'''
	do some stuff. 
	choose an attached lto drive to format a tape on
	'''
	pass
