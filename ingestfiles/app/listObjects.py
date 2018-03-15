#!/usr/bin/env python3
# standard library
import os
# nonstandard libraries
import paramiko
# local modules
import app
from . import sshStuff

config = app.app_config

dirName = list(config["SHARED_DIR"].keys())[0]
hostName = config["SHARED_DIR"][dirName]['host name']
source_dir = config["SHARED_DIR"][dirName]['directory full path']
remoteDetails = config["REMOTE_CONNECTIONS"][hostName]

def list_objects():
	objects = {}
	
	if not hostName == 'localhost':
		try:
			remoteAddress = remoteDetails["address"]
			remoteUser = remoteDetails["username"]
			relativeKeyfile = remoteDetails["ssh private key file"]
			sshKeyfile = os.path.expanduser(relativeKeyfile)

			theStuff = []
			connection = sshStuff.connect(remoteAddress,remoteUser,sshKeyfile)
			_list = connection.sendCommand("ls {}".format(source_dir))
			for item in _list.readlines():
				theStuff.append(item.rstrip())


			for _object in theStuff:
				objects[(os.path.join(source_dir,_object))] = _object
		except:
			print("CONNECTION ERROR?")
	
	else:
		for _object in os.listdir(source_dir):
			if not _object.startswith('.'):
				objects[(os.path.join(source_dir,_object))] = _object

	return objects
