#!/usr/local/bin/python3

import sys, json, subprocess

myfile = sys.argv[1]

user = sys.argv[2]

# def process_file(something):
#     mediainfo = subprocess.call(['mediainfo', something])
#     # stuff = sys.stdout.write(mediainfo)
#     return mediainfo
    # return stuff

print("hello"+user)


# process_file(myfile)
# print(sys.stdout())

stuff = subprocess.run(['mediainfo', myfile], stdout=subprocess.PIPE)
print(stuff)