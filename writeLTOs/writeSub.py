#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/RLAS_Admin/Sites/ingest/login')

from login import login

import os, subprocess, paramiko

# ltoA = sys.argv[1]
# ltoB = sys.argv[2]
# tapeA = '/Volumes/'+ltoA
# tapeB = '/Volumes/'+ltoB

tape = sys.argv[1]

destination = "blue"
user = login(destination)[0]
cred = login(destination)[1]

sourceDir = "/Users/BLAS2/Documents/AIP_Target/"


def writeSub(tape):
	print("Writing to "+tape)
	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	# print("trying to write to "+tapeA)
	try:
		client.connect('10.253.22.22',username=user, password=cred)
		stdin, stdout, stderr = client.exec_command("echo $(whoami)")
		for item in stdout.readlines():
			print(item)
		stdin, stdout, stderr = client.exec_command("export PATH=$PATH:/usr/local/bin")
		stdin, stdout, stderr = client.exec_command("echo $PATH")
		stdin, stdout, stderr = client.exec_command("/usr/local/bin/writelto -t "+tape+" -e N "+sourceDir)
		for line in stderr.read().splitlines():
			print(line.decode())

		return "yes"
		
		client.close()

	except paramiko.SSHException:
		print("Connection Error")
		return "no"

writeSub(tape)