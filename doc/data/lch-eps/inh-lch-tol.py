# -*- coding: utf-8 -*-
import csv
import re
#import copy
#import numpy as np

# Input table layout
#	Plate, Well (A-H), Well (1-12), Ranks..., Values...
# Rank order:
#	Furfural, HMF, vanillin, acetic acid, formic aid,
#	laevulinic acid, LCH
# Values remain unused.

# Read files and populate inh_tol (this one is huge when printed in the shell)
with open("inh-lch-tol_ranks.txt", 'r') as f:
	reader = csv.reader(f, delimiter="\t")
	tol_ranks = list(reader)

# del unused header line
del tol_ranks[0]

# Replace Xyl1/Xyl2 with corresponding shorthand function
# Replace hyphens with armoured hyphens
for line in range(len(tol_ranks)):
	tol_ranks[line][0] = re.sub('Xyl1', '\\xyli', tol_ranks[line][0])
	tol_ranks[line][0] = re.sub('Xyl2', '\\xylj', tol_ranks[line][0])
	for inhibitor in range(1, len(tol_ranks[line])):
		tol_ranks[line][inhibitor] = re.sub('-', '{-}', tol_ranks[line][inhibitor])

# Construct table rows
# For use in LaTeX document
tol_tr = []
with open('inh-lch-tol_ranks.tex', 'w') as f:
	for line in range(len(tol_ranks)):
		tol_line = "{}{{{}{}}} & {} & {} & {} & {} & {} & {} & {} \\\\".format(tol_ranks[line][0], tol_ranks[line][1], tol_ranks[line][2], tol_ranks[line][3], tol_ranks[line][4], tol_ranks[line][5], tol_ranks[line][6], tol_ranks[line][7], tol_ranks[line][8], tol_ranks[line][9])
		print >> f, tol_line
