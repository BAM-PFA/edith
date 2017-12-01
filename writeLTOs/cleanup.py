#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/RLAS_Admin/Sites/ingest/login')

from login import login
import os
import paramiko
import shutil

# directory = sys.argv[1]

def cleanup(directory):
	if "BLAS2" in directory:
		destination = "blue"
		user = login(destination)[0]
		cred = login(destination)[1]

		client = paramiko.SSHClient()
		client.load_system_host_keys()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			client.connect('10.253.22.22',username=user, password=cred)
			stdin, stdout, stderr = client.exec_command("/usr/local/bin/python3 /Users/BLAS2/Desktop/mountnwrite/cleaner.py")
			for line in stdout.read().splitlines():
				print(line.decode())
			for line in stderr.read().splitlines():
				print(line.decode())
				
			client.close()
			return 1

		except paramiko.SSHException:
			print("Connection Error")
			return 0
	else:
		for package in os.listdir(directory):
			try:
				shutil.rmtree(package)
				return 1
			except:
				print("Couldn't clean "+directory+". You should try again???")
				return 0
