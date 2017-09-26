#!/usr/bin/env python3

import sys
sys.path.insert(0, '/Users/RLAS_Admin/Sites/ingest/login')

import os, subprocess, paramiko
import os.path
from login import login

LTOid = sys.argv[1]
AIPStagingDir = "/Volumes/maxxraid1/LTO_STAGE/"
AIPblueTarget = "/Users/BLAS2/Documents/AIP_TARGET/"

destination = "blue"
user = login(destination)[0]
cred = login(destination)[1]

for AIP in os.listdir(AIPStagingDir):
	aipPath = AIPStagingDir + AIP
	if os.path.isdir(aipPath):
		with open(aipPath+"/tagmanifest-md5.txt") as manifest:
			for n, line in enumerate(manifest):
				if n == 2:
					manifestMD5 = line
				elif n > 2:
					break
		print(manifestMD5)
		# subprocess.run(['rsync','-av',aipPath,user,'@10.253.22.22:',AIPblueTarget])
		targetFile = AIPblueTarget+AIP
					
		# OPEN SSH & SFTP THE FILE
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
		    ssh.connect('10.253.22.21', username=user,
		        password=cred)
		    # stdin, stdout, stderr = ssh.exec_command("writelto -t "+LTOid+" -e ")
		    stdin, stdout, stderr = ssh.exec_command("echo ${whoami}")
		    for line in stdout:
		    	print(line)


		    
		        
		    ssh.close()
		except paramiko.SSHException:
		    print("Connection Error")



print("Hi, now I am writing AIPs to tape id: "+LTOid+"<br/> See you later!")