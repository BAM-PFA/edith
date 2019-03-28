#!/usr/bin/env python3
'''
Useful utility stuff.
'''
# standard library stuff
import configparser
import glob
import os
import shutil
import subprocess
import time
# non-standard modules
from flask_login import current_user
# local modules
import app

config = app.app_config

def get_shared_dir_stuff(dirType):
	if dirType == 'shared':
		dirName = list(config["SHARED_DIR"].keys())[0]
		hostName = config["SHARED_DIR"][dirName]['host name']
		sourceDir = config["SHARED_DIR"][dirName]['directory full path']
	elif dirType == 'aip':
		dirName = list(config["AIP_STAGING_DIR"].keys())[0]
		hostName = config["AIP_STAGING_DIR"][dirName]['host name']
		sourceDir = config["AIP_STAGING_DIR"][dirName]['directory full path']
	elif dirType == 'dip':
		dirName = list(config["DIP_OUT_DIR"].keys())[0]
		hostName = config["DIP_OUT_DIR"][dirName]['host name']
		sourceDir = config["DIP_OUT_DIR"][dirName]['directory full path']

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

def get_pymm_log():
	pymmPath = get_pymm_path()
	pymmConfigPath = os.path.join(pymmPath,'pymmconfig','config.ini')
	pymmConfig = configparser.SafeConfigParser()
	pymmConfig.read(pymmConfigPath)
	pymmLogDir = pymmConfig['logging']['pymm_log_dir']
	pymmLogPath = os.path.join(pymmLogDir,'pymm_log.txt')
	lines = []
	try:
		with open(pymmLogPath,'r') as f:
			for line in f.readlines():
				lines.append(line.rstrip())
		log = lines
	except:
		log = ["Couldn't read the pymm log.. sorry."]

	return log


def get_python_path():
	pythonPath = config['PYTHON3_BINARY_PATH']
	return pythonPath

def delete_it(_object):
	if os.path.isfile(_object):
		try:
			os.remove(_object)
		except:
			print("cant remove {}".format(_object))
	elif os.path.isdir(_object):
		try:
			shutil.rmtree(_object)
		except:
			pass
	else:
		print("cant remove {}".format(_object))

# def clean_temp_dir():
# 	for _object in os.listdir(get_temp_dir):
# 		if not _object.startswith('.'):
# 			if not 
# 			delete_it(_object)

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

def get_current_LTO_id():
	tmpDir = get_temp_dir()
	ltoIdFilePath = os.path.join(tmpDir,'LTOID.txt')
	if not os.path.exists(ltoIdFilePath):
		try:
			with open(ltoIdFilePath,'w') as idfile:
				idfile.write('no lto id in use')
		except:
			print("You have some permission issues writing to the tmp dir")
	try:
		with open(ltoIdFilePath,'r') as idfile:
			currentLTOid = idfile.readline().strip()
	except:
		currentLTOid = "Couldn't read the LTO id file"

	return currentLTOid

def get_devices():

	linuxDevices = {
		"/dev/nst0":"",
		"/dev/nst1":""
		}

	return linuxDevices

def get_a_and_b():
	noID = [
		"no lto id in use",
		"Couldn't read the LTO id file"
		]
	theID = get_current_LTO_id()

	if not theID in noID:		
		aTapeID = theID
		bTapeID = aTapeID[:-1]+"B"
	else:
		aTapeID = "no id"
		bTapeID = "no id"

	return aTapeID,bTapeID

def now():
	now = time.strftime("%Y-%m-%dT%H-%M-%S")
	return now

def mount_tape(command):
	print(command)
	subprocess.run(command,stdin=None,stdout=None,close_fds=True)
	print("gave it a shot")
	return True

def clean_temp_dir(_type=None):
	tempDir = get_temp_dir()
	for thing in os.listdir(tempDir):
		if '.json' in thing:
			if _type == 'ingest':
				if 'tempTapeStats' not in thing:
					print('deleting '+thing)
					os.remove(os.path.join(tempDir,thing))
			else:
				print('deleting '+thing)
				os.remove(os.path.join(tempDir,thing))
		if os.path.isdir(thing):
			try:
				os.rmdir(thing)
			except OSError:
				print(thing+" is not empty... I won't delete it.")

def humansize(nbytes):
	'''
	Return Mebibytes/Gibibytes (1024-based blocks)
	this file size calc came from:
	http://stackoverflow.com/questions/14996453/
	  python-libraries-to-calculate-human-readable-filesize-from-bytes
	'''
	nbytes = int(nbytes)
	suffixes = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB']
	if nbytes == 0:
		return '0 B'
	i = 0
	while nbytes >= 1024 and i < len(suffixes)-1:
		nbytes /= 1024.
		i += 1
	f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
	return '%s %s' % (f, suffixes[i])

def get_object_size(path):
	'''
	Stolen from https://stackoverflow.com/q/40840037
	'''
	total = 0
	for entry in os.scandir(path):
		if entry.is_file():
			total += entry.stat().st_size
		elif entry.is_dir():
		   total += get_object_size(entry.path)
	return total

def get_proxy_framerate(proxyPath):
	'''
	So, AFAICT the framerate of the input master file is always going to be
	the same as the proxy. Jon wants to have a quick reference in
	ResourceSpace of the master file framerate, which will combine with 
	the PFA projection frame rate in the case of silent film transfers to 
	provide a fuller picture of what an exhibition mezzanine will need to
	look like.
	Also: this will return an empty string for things like audio that don't 
	have a Video track.
	'''
	pythonPath = get_python_path()
	pymmPath = get_pymm_path()
	makeMetadataPath = os.path.join(pymmPath,'makeMetadata.py')
	makeMetadataCommand = [
		pythonPath,
		makeMetadataPath,
		'-i', proxyPath,
		'-v','FrameRate/String',
		'-t','Video'
	]
	out = subprocess.run(makeMetadataCommand,stdout=subprocess.PIPE)
	framerate = out.stdout.decode().rstrip()

	return framerate

def construct_user_name():
	userFirstName = current_user.first_name
	userLastName = current_user.last_name
	# Construct the user's full name, unless the user is missing
	# one of these values (they shouldn't be...)
	if not any(x in (userFirstName,userLastName) for x in ("None",None)):
		user = "{} {}".format(userFirstName,userLastName)
	else:
		# otherwise default to the user's email address
		user = current_user.email

	return user
