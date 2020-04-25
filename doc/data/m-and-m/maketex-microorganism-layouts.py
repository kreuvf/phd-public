# -*- coding: utf-8 -*-
import csv
from collections import OrderedDict

import re
import copy

# # # # # # # # # # # # # # # # # # # # 
# Setup and Definitions
#
# dictaddinv: Invert key value pairs and add to dictionary
# Source: http://code.activestate.com/recipes/252143-invert-a-dictionary-one-liner/#c6
def dictaddinv(d):
	assert len(d) == len(dict([v,k] for k,v in d.iteritems())), 'Duplicate value in dictionary.'
	d.update(dict([v,k] for k,v in d.iteritems()))

# Empty variables for abbreviation list
abbrlist = []
abbrdict = dict()
texdict = dict()

# Abbreviation list filename
abbrfn = "eps_abbr.txt"

# Empty variables for EPS plate layouts
# epsli = EPS layouts, in
# epsabbr = EPS strain abbreviations used per plate
epsli = [[], []]
epslayouts = [[[[] for col in range(13)] for row in range(8)] for plate in range(2)]
epsabbr = [[], []]

# EPS plate layout filenames (input)
epsfn = ["eps1.txt", "eps2.txt"]

# # # # # # # # # # # # # # # # # # # # 
# File Input
#
# Read abbreviation list file
# Columns: Abbreviation, Full name (de), Full name (en), TeX name (en)
# Sample: Bac	Bacillus	Bacillus	\mo{Bacillus}
with open(abbrfn, 'r') as abbrs:
	reader = csv.reader(abbrs, delimiter = "\t" )
	abbrlist = list(reader)

# Read plate layouts
with open(epsfn[0], 'r') as eps1:
	reader = csv.reader(eps1, delimiter = "\t")
	epsli[0] = list(reader)
with open(epsfn[1], 'r') as eps2:
	reader = csv.reader(eps2, delimiter = "\t")
	epsli[1] = list(reader)

# # # # # # # # # # # # # # # # # # # # 
# Data Processing
# 
# Delete unneeded entries
del abbrlist[-1] # empty
del abbrlist[0] # header

del epsli[0][-1] # empty
del epsli[0][0] # header

del epsli[1][-1] # empty
del epsli[1][0] # header

# Generation of abbreviation dictionaries
for abbr in range(len(abbrlist)):
	abbrdict["{}".format(abbrlist[abbr][1])] = abbrlist[abbr][0]
	texdict["{}".format(abbrlist[abbr][3])] = abbrlist[abbr][0]
# Add reverse entries as well
dictaddinv(abbrdict)
dictaddinv(texdict)
# Add the empty string
abbrdict[''] = ''

# Abbreviate plates
for plate in range(len(epsli)):
	for row in range(len(epsli[plate])):
		# Copy first items = row names
		epslayouts[plate][row][0] = epsli[plate][row][0]
		for col in range(1, len(epsli[plate][row])):
			epslayouts[plate][row][col] = abbrdict[epsli[plate][row][col]]

# Gather abbreviations used per plate
for plate in range(len(epslayouts)):
	for row in range(len(epslayouts[plate])):
		for col in range(1, len(epslayouts[plate][row])):
			# cw = current well
			cw = epslayouts[plate][row][col]
			if(cw != ''):
				epsabbr[plate].append(cw)

# # # # # # # # # # # # # # # # # # # # 
# Output Preparation
# Create TeX table rows of the plate layouts
# tepl = TeX EPS plate layouts
tepl = [[], []]
for plate in range(len(epslayouts)):
	for row in range(len(epslayouts[plate])):
		# cr = current row
		cr = epslayouts[plate][row]
		# line = one line of TeX for a table
		line = "\t{} & {} & {} & {} & {} & {} & {} & {} & {} & {} & {} & {} & {} \\\\".format(
			cr[0], cr[1], cr[2], cr[3], cr[4], cr[5], cr[6],
			cr[7], cr[8], cr[9], cr[10], cr[11], cr[12]
			)
		tepl[plate].append(line)

# Unify and sort abbreviation lists
# Case insensitive: http://stackoverflow.com/a/10269708
# Probably problematic with Python 3, should use unicode.lower instead, but too lazy
epsabbr[0] = sorted(list(OrderedDict.fromkeys((epsabbr[0]))), key=str.lower)
epsabbr[1] = sorted(list(OrderedDict.fromkeys((epsabbr[1]))), key=str.lower)

# Create abbreviation texts (per plate)
# texabbr = TeX texts with abbreviations
texabbr = [[], []]
for plate in range(len(epsabbr)):
	# Last element needs to have a full stop
	for abbr in range(len(epsabbr[plate])-1):
		line = '{}: {}; '.format(
			epsabbr[plate][abbr],
			texdict[epsabbr[plate][abbr]])
		texabbr[plate].append(line)
	line = '{}: {}.'.format(
		epsabbr[plate][-1],
		texdict[epsabbr[plate][-1]])
	texabbr[plate].append(line)

# Concatenate single abbreviation chunks into one sentence.
# textext = final text with TeX commands
textext = [[], []]
for plate in range(len(texabbr)):
	textext[plate] = ''.join(texabbr[plate])

# # # # # # # # # # # # # # # # # # # # 
# Output Files
with open("eps1_layout.tex", "w") as f:
	for line in range(len(tepl[0])):
		print >> f, tepl[0][line]

with open("eps2_layout.tex", "w") as f:
	for line in range(len(tepl[1])):
		print >> f, tepl[1][line]

# # # # # # # # # # # # # # # # # # # # 
# Output Abbreviations (screen only)
print(textext[0])
print(textext[1])