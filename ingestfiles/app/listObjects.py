#!/usr/bin/env python3
# standard library
import os
import sys
# nonstandard libraries
import paramiko
# local modules
import app
from . import sshStuff
from . import utils

def list_objects():
	objects = {}
	dirName, hostName, sourceDir = utils.get_shared_dir_stuff()
	if not hostName == 'localhost':
		sourceDir, remoteAddress, remoteUser, remotePassword, sshKeyfile = utils.get_remote_credentials()
		try:
			# print(remoteAddress)
			theStuff = []
			connection = sshStuff.connect(remoteAddress,remoteUser,sshKeyfile)
			# print(sourceDir)
			_list = connection.sendCommand("ls {}".format(sourceDir))
			for item in _list.readlines():
				if not item.startswith('.'):
					theStuff.append(item.rstrip())
			for _object in theStuff:
				objects[(os.path.join(sourceDir,_object))] = _object
		except:
			print("CONNECTION ERROR?")
		
	else:
		for _object in os.listdir(sourceDir):
			if not _object.startswith('.'):
				objects[(os.path.join(sourceDir,_object))] = _object
	
	return objects
