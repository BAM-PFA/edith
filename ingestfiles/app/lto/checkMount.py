#!/usr/bin/env python3

import sys
sys.path.insert(0, '/Users/RLAS_Admin/Sites/ingest/login')

from login import login

import os
import subprocess
import paramiko

LTOid = sys.argv[1]

# tape = '/Volumes/'+LTOid

destination = "blue"
user = login(destination)[0]
cred = login(destination)[1]

def mount(tape):
	# print(LTOid)
	
	# if "B" in tape:
	# 	drive = "1"
	# else:
	# 	drive = "0"

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
	# print(volumeList)
	if not LTOid in volumeList:
		# stdin, stdout, stderr = client.exec_command("/usr/local/bin/python3 /Users/BLAS2/Desktop/mountnwrite/mount.py "+tape)
		subprocess.run(["/Users/RLAS_Admin/Sites/ingest/writeLTOs/mount.py",LTOid])
		# for item in stdout.read().splitlines():
		# 	print(item.decode())
		volumeList = []
		stdin, stdout, stderr = client.exec_command("ls /Volumes")
		for mountedVolume in stdout.read().splitlines():
			# print(mountedVolume)
			volumeList.append(mountedVolume.decode())
		# print(volumeList)
		if not LTOid in volumeList:
			reinsert = 'YOU NEED TO REINSERT '+LTOid
			print(reinsert)
			return reinsert
		else:
			print("It looks like <span style='font-weight:bold'>"+LTOid+"</span> is mounted! You can write to it.<br/><br/>")
			return 1	
	else:
		print("It looks like <span style='font-weight:bold'>"+LTOid+"</span> is mounted! You can write to it.<br/><br/>")
		return 1
	client.close()

mount(LTOid)