#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/RLAS_Admin/Sites/ingest/login')

from login import login

import subprocess, paramiko

tape = sys.argv[1]
# print(tape)

destination = "blue"
user = login(destination)[0]
cred = login(destination)[1]

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect('10.253.22.22',username=user, password=cred)

stdin, stdout, stderr = client.exec_command("/Users/BLAS2/Desktop/mountnwrite/mount.sh "+tape)
for out in stdout.read().splitlines():
	print(out.decode())

for error in stderr.read().splitlines():
	print(error.decode())

client.close()
