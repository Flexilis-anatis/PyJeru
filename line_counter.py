#!/usr/bin/python

import os

# Shamelessly copied and modified from stackoverflow
total = 0
for root, dirs, files in os.walk("."):
	path = root.split(os.sep)
	for file in files:
		if "line_counter" in file or (".py" not in file) or (".pyc" in file):
			continue
		loc = 0
		with open(root+os.sep+file) as f:
			loc = sum(1 for x in f.read() if x == "\n")
		print(file, loc)
		total += loc
print("Total", total)
