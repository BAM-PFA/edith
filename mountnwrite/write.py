#!/usr/bin/env python3

import sys, subprocess
print("AOOOOOOHHhHHHHHHHHHHHHHHHH")
tape = sys.argv[1]
sourceDir = "/Users/BLAS2/Documents/AIP_TARGET"
print("Hello this is Blue. I am going to try writing to "+tape)

try:
	subprocess.run(['/usr/local/bin/writelto', '-t',tape,'-e','N',sourceDir])
except:
	print("Sorry, I am Blue and I failed to write to LTO.")
