#!/usr/local/bin/python3

import sys, json, subprocess

myfile = sys.argv[1]
user = sys.argv[2]

output = subprocess.run(['/usr/local/bin/mediainfo', myfile], stdout=subprocess.PIPE)

print(output)