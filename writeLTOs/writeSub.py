#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/RLAS_Admin/Sites/ingest/login')

from login import login
import os, subprocess, paramiko

sourceDir = "/Users/BLAS2/Documents/AIP_Target/"
AIPStagingDir = "/Volumes/maxxraid1/LTO_STAGE"
tape = sys.argv[1]

print("OK "*100)

def writeSub(tape):
	destination = "blue"
	user = login(destination)[0]
	cred = login(destination)[1]

	print("Writing to "+tape)
	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		client.connect('10.253.22.22',username=user, password=cred)
		stdin, stdout, stderr = client.exec_command("echo $(whoami)")
		for item in stdout.readlines():
			print(item)
		# stdin, stdout, stderr = client.exec_command("export PATH=$PATH:/usr/local/bin")
		# stdin, stdout, stderr = client.exec_command("echo $PATH")
		stdin, stdout, stderr = client.exec_command("/usr/local/bin/python3 /Users/BLAS2/Desktop/mountnwrite/write.py "+tape)
		for line in stdout.read().splitlines():
			print(line.decode())
		for line in stderr.read().splitlines():
			print(line.decode())
				
		client.close()
		return 1

	except paramiko.SSHException:
		print("Connection Error")
		return 0

writeSub(tape)
