#!/usr/bin/env python3

import sys
sys.path.insert(0, '/Users/RLAS_Admin/Sites/ingest/login')

import os, subprocess#, paramiko
import os.path

ltoA = sys.argv[1]
ltoB = sys.argv[2]
tapeA = '/Volumes/'+ltoA
tapeB = '/Volumes/'+ltoB

AIPStagingDir = "/Volumes/maxxraid1/LTO_STAGE/"
AIPblueTarget = "/Users/BLAS2/Documents/AIP_TARGET/"

remoteLocation = "BLAS2@10.253.22.22:"+AIPblueTarget
	
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
		# command = ["rsync"," -av ",aipPath," -e "," ssh ",remoteLocation]
		subprocess.run(["rsync","-av",aipPath,"-e","ssh",remoteLocation])
		# subprocess.run(['/usr/local/bin/rsync','-azv',aipPath,'-e','ssh',' BLAS2@10.253.22.22:',AIPblueTarget])
		# print("<br><br>"+''.join(command))

# I NEEDED TO MAKE SURE THIS PROCESS DIDN'T GET SKIPPED BEFORE IT FINISHED, SO 
# I PUT THE ACTUAL writelto CALL IN A SUB-SCRIPT AND USED subprocess TO BLOCK
# ANYTHING ELSE FROM HAPPENING IN THE MEANTIME.
# for tape in ltoA,ltoB:
# 	try:
# 		subprocess.run(["/usr/local/bin/python3","/Users/RLAS_Admin/Sites/ingest/writeLTOs/writeSub.py",tape])
# 	except:
# 		print("#"*100+"\nsomething failed in the subprocess")
