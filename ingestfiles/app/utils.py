#!/usr/bin/env python3
'''
Useful utility stuff.
'''
# standard libraries
import os
# local modules
import app

config = app.app_config

def get_shared_dir_stuff():
	dirName = list(config["SHARED_DIR"].keys())[0]
	hostName = config["SHARED_DIR"][dirName]['host name']
	sourceDir = config["SHARED_DIR"][dirName]['directory full path']
	
	return dirName, hostName, sourceDir

def get_remote_credentials():
	dirName, hostName, sourceDir = get_shared_dir_stuff()
	remoteDetails = config["REMOTE_CONNECTIONS"][hostName]
	remoteAddress = remoteDetails["address"]
	remoteUser = remoteDetails["username"]
	remotePassword = remoteDetails["password"]
	relativeKeyfile = remoteDetails["ssh private key file"]
	sshKeyfile = os.path.expanduser(relativeKeyfile)

	return sourceDir, remoteAddress, remoteUser, remotePassword, sshKeyfile

def get_temp_dir():
	scriptDir = os.path.dirname(os.path.realpath(__file__))
	tempDir = os.path.join(scriptDir,'tmp')
	return tempDir
