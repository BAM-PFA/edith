#!/usr/bin/env python3

import sys
import os

AIPdirectory = sys.argv[1]

def listAIPs(dir):
	print("<table>")
	for row in os.listdir(AIPdirectory):
		if not row.startswith('.'):
			print("<tr><td>"+row+"</tr></td>")
	print("</table>")

listAIPs(AIPdirectory)
