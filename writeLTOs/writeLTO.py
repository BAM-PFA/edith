#!/usr/bin/env python3

import sys
sys.path.insert(0, '/Users/RLAS_Admin/Sites/ingest/login')

from login import login

import os, subprocess, paramiko

ltoA = sys.argv[1]
ltoB = sys.argv[2]

# print("TOODLE DEE DOODLE "+ltoA+ltoB)

tapeA = '/Volumes/'+ltoA
tapeB = '/Volumes/'+ltoB
<input type="hidden" name="foo" value="<?php echo $var;?>" />

destination = "blue"
user = login(destination)[0]
cred = login(destination)[1]

def write(tape):
	
	if "B" in tape:
		drive = "1"
	else:
		drive = "0"

	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	volumeList = []
	client.connect('10.253.22.22',username=user, password=cred)
	# print("HELLO ALREADY")

	stdin, stdout, stderr = client.exec_command("ls /Volumes")
	for mountedVolume in stdout.read().splitlines():
		# print(mountedVolume.decode())
		volumeList.append(mountedVolume.decode())
	print(volumeList)