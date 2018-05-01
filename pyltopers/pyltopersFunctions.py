#!/usr/bin/env python3

import os
import subprocess
import sys

def get_system():
	if sys.platform.startswith("darwin"):
		return 'mac'
	elif sys.platform.startswith("win"):
		return 'windows'
	elif sys.platform.startswith("linux"):
		return 'linux'
	else:
		return False

def find_decks(system):
	foundDecks = []
	if system == 'linux':
		lsscsi,err = subprocess.call(['lsscsi'],stdout=subprocess.PIPE).communicate()
		for line in lsscsi.splitlines():
			if 'tape' in line.decode():
				foundDecks.append(line.decode())


	return foundDecks


def folder_size(path):
	'''
	Stolen from https://stackoverflow.com/q/40840037
	'''
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += folder_size(entry.path)
    return total

 def LTO_free_space(LTOid):
 	'''
 	Get the free space left on an LTO tape and write the vaue in bytes to a text file
 	'''
 	bytesAvailable = subprocess.Popen(['df',LTOid],stdout=subprocess.PIPE).communicate()
