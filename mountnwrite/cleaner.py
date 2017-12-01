#!/usr/bin/env python3

import os
import shutil

directory = "/Users/BLAS2/Documents/AIP_TARGET/"
print("Hello this is Blue. I am going to try cleaning "+directory)

for package in os.listdir(directory):
	try:
		shutil.rmtree(package)
		return 1
	except:
		print("Couldn't delete some stuff... ")
		return 0
		