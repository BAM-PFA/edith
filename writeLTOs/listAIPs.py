#!/usr/bin/env python3

import sys
import os
import os.path
import subprocess

AIPdirectory = sys.argv[1]

def sizeof_fmt(num, suffix='B'):
	for unit in ['',' K',' M',' G',' T','Pi','Ei','Zi']:
		if abs(num) < 1024.0:
			return "%3.1f%s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.1f%s%s" % (num, 'Yi', suffix)

def get_size(itemPath):
	total_size = 0
	for dirpath, dirnames, filenames in os.walk(itemPath):
		for f in filenames:
			fp = os.path.join(dirpath, f)
			total_size += os.path.getsize(fp)
	return total_size

def listAIPs(directory):
	print("<style>table, th, td {border: 1px solid black;}</style><table style='width:75%'><tr><th>Name of package to ingest</th><th>Total size of package</th></tr>")
	
	for item in os.listdir(AIPdirectory):
		itemPath = os.path.join(AIPdirectory,item)
		if os.path.isdir(itemPath):
			print("<tr><td><span style=font-weight:bold>"+item+"<td><span style=font-weight:bold>"+sizeof_fmt(get_size(itemPath))+"</tr></td>")
	
	print("</table><br><br><br>")

listAIPs(AIPdirectory)
