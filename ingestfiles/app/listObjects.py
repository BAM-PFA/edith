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
print(dirName)
hostName = config["SHARED_DIR"][dirName]['host name']
print(hostName)
source_dir = config["SHARED_DIR"][dirName]['directory full path']
print(source_dir)
remoteDetails = config["REMOTE_CONNECTIONS"][hostName]
print(remoteDetails)

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
			_list = connection.sendCommand("ls /share/Multimedia")
			print(_list)
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