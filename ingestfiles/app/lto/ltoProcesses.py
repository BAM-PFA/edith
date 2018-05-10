#!/usr/bin/env python3
# standard library modules
import ast
from multiprocessing.dummy import Pool as ThreadPool
import os
import re
import subprocess
import sys
from time import sleep
# non-standard libraries
from flask import render_template, request
import wtforms
# local modules
from .. import utils

def run_ltfs(devname,tempdir,mountpoint):
	command = (
		"sudo ltfs "
		"-o gid=33 "
		"-o uid=33 "
		"-o work_directory={} "
		"-o noatime "
		"-o capture_index "
		"-o devname={} "
		"{}".format(tempdir,devname,mountpoint)
		)
	commandList = command.split()
	print(commandList)
	doit = subprocess.Popen(
		commandList,
		stdin=subprocess.DEVNULL,
		stdout=subprocess.DEVNULL,
		stderr=subprocess.PIPE,
		close_fds=True
		)
	for line in doit.stderr.read().splitlines():
		print(line.decode())

	return doit.stderr

def folder_size(path):
	'''
	Stolen from https://stackoverflow.com/q/40840037
	'''
	total = 0
	for entry in os.scandir(path):
		if entry.is_file():
			total += entry.stat().st_size
		elif entry.is_dir():
		   total += folder_size(entry.path)
	return total

def LTO_free_space(mountpoint):
	'''
	Get the free space left on an LTO tape and return the value in bytes`
	'''
	output = subprocess.run(['df',mountpoint],stdout=subprocess.PIPE)
	dfLine = output.stdout.decode().splitlines()[1]
	# should look like:
	# "ltfs:/dev/nst1 # mountpoint
	# 5597795328  # 1K-blocks
	# 6144 # used
	# 5597789184  # available
	# 1% # Use%
	# /path/to/mtn/point/18051B" # mounted on
	if dfLine.startswith('ltfs'):
		bytesAvailable = dfLine.split()[3]
		return int(bytesAvailable)
	else:
		return 0



