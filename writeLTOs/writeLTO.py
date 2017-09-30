#!/usr/bin/env python3

import sys
sys.path.insert(0, '/Users/RLAS_Admin/Sites/ingest/login')

import os, subprocess, paramiko

ltoA = sys.argv[1]
ltoB = sys.argv[2]
tapeA = '/Volumes/'+ltoA
tapeB = '/Volumes/'+ltoB

for tape in ltoA,ltoB:
	try:
		subprocess.run(["/usr/local/bin/python3","/Users/RLAS_Admin/Sites/ingest/writeLTOs/writeSub.py",tape])
	except:
		print("#"*100+"\nsomething failed in the subprocess")
