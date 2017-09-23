#!/usr/bin/env python3

import sys
import os
<<<<<<< HEAD
import os.path
import subprocess


AIPdirectory = sys.argv[1]

def listAIPs(directory):
	print("<table>")
	for item in os.listdir(AIPdirectory):
		itemPath = os.path.join(AIPdirectory,item)
		if os.path.isdir(itemPath):
			# print((itemPath))
			# openSelect = """
			# 			<select name="s1">
			# 			<option value="" selected="selected">"""+itemPath+"""</option>

			# """
			# # print(openSelect)
			# result = subprocess.run(
			#     ['php', 'aipListing.php', itemPath],    # program and arguments
			#     stdout=subprocess.PIPE,  # capture stdout
			#     check=True               # raise exception if program fails
			# ) 
			# resultString = result.stdout.decode('utf-8')
			# # print(resultString)
			# closeSelect = """
			# 			</select> 
			# """
			
			# print("<tr><td>"+openSelect+result.stdout.decode('utf-8')+closeSelect+"</tr></td>")
			print("<tr><td><span style=font-weight:bold>"+item+"</tr></td>")
=======

AIPdirectory = sys.argv[1]

def listAIPs(dir):
	print("<table>")
	for row in os.listdir(AIPdirectory):
		if not row.startswith('.'):
			print("<tr><td>"+row+"</tr></td>")
>>>>>>> 0d8bef369fff3d1ce9f5033849dfa0d53549029e
	print("</table>")

listAIPs(AIPdirectory)
