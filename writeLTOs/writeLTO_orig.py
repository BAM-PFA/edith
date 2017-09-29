#!/usr/bin/env python3

import sys
sys.path.insert(0, '/Users/RLAS_Admin/Sites/ingest/login')

import os, subprocess, paramiko, re
import os.path
from login import login

LTOid = sys.argv[1]
ltoRegex = re.compile(r'(\d{5})(A|B)')
ltoMatch = re.match(ltoRegex,LTOid)
ltoPrefix = ltoMatch.group(1)
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
		# print(manifestMD5)
		remoteLocation = "BLAS2@10.253.22.22:"+AIPblueTarget
		# command = ["rsync"," -av ",aipPath," -e "," ssh ",remoteLocation]
		# subprocess.run(["rsync","-av",aipPath,"-e","ssh",remoteLocation])
		# subprocess.run(['/usr/local/bin/rsync','-azv',aipPath,'-e','ssh',' BLAS2@10.253.22.22:',AIPblueTarget])
		# print("<br><br>"+''.join(command))
		targetFile = AIPblueTarget+AIP
					
		client = paramiko.SSHClient()
		client.load_system_host_keys()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			destination = "blue"
			user = login(destination)[0]
			cred = login(destination)[1]

			volumeList = []
			client.connect('10.253.22.22',username=user, password=cred)
			# print("HELLO ALREADY")
			stdin, stdout, stderr = client.exec_command("export PATH=$PATH:/usr/local/bin")
			stdin, stdout, stderr = client.exec_command("echo $PATH")
			print(stdout.readlines())
			stdin, stdout, stderr = client.exec_command("ls /Volumes")
			for mountedVolume in stdout.readlines():
				print(mountedVolume)
				volumeList.append(mountedVolume)
			if not LTOid in volumeList:
				stdin, stdout, stderr = client.exec_command("/usr/local/bin/mountlto 0 1")
				# stdin, stdout, stderr = client.exec_command("/usr/local/bin/mountlto 1")

			stdin, stdout, stderr = client.exec_command("/usr/local/bin/writelto -t "+LTOid+" -e N "+targetFile)
			# stdin, stdout, stderr = ssh.exec_command("echo $PATH")
			for line in stdout:
				print(line)
			for line in stderr:
				print(line)
			print("butt")
			client.close()
		except paramiko.SSHException:
			print("Connection Error")



print("Hi, now I am writing AIPs to tape id: "+LTOid+"<br/> See you later!")