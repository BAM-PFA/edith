#!/usr/bin/env python3
'''
Useful utility stuff.
'''
# standard libraries
import os
import shutil
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

def get_pymm_path():
	pymmPath = config["PYMM_PATH"]
	return pymmPath

def get_python_path():
	pythonPath = config['PYTHON3_BINARY_PATH']
	return pythonPath

def delete_it(_object):
	if os.path.isfile(_object):
		try:
			os.remove(_object)
		except:
			print("cant remove "+_object)
	elif os.path.isdir(_object):
		try:
			shutil.rmtree(_object)
		except:
			pass
	else:
		print("cant remove "+_object)

def clean_temp_dir():
	for _object in os.listdir(get_temp_dir):
		if not _object.startswith('.'):
			delete_it(_object)

def get_rs_dir():
	rs_dir = config['RESOURCESPACE_PROXY_DIR']
	return rs_dir

def get_rs_base_url():
	rs_base_url = config["RS_BASE_URL"]
	return rs_base_url

def get_rs_credentials(user):
	rsUserName = config["KNOWN_USERS"][user]["RSuserName"]
	rsAPIkey = config["KNOWN_USERS"][user]["resourcespaceKey"]
	return rsUserName,rsAPIkey

def get_extension(basename):
	split = os.path.splitext(basename)
	ext = split[1]
	return ext