# -*- coding: utf-8 -*-
import re
import copy
import numpy as np

# inh_tol[ ][ ][ ][ ]
#         |  |  |  ^- coordinate (number, x-axis)
#         |  |  ^---- coordinate (letter, y-axis)
#         |  ^------- plate
#         ^---------- category
#
# Category: 0..1 = reference, lignocellulose hydrolysate (lch)
# plate: 0 = Xyl1, 1 = Xyl2
# Coordinate (letter): 0...7 = A..H
# Coordinate (number): 0..11 = 1..12
# First value: use flag
#	0: Do not use this value for calculation at all
#	1: Use this value for calculation as a normal value
#	2: Use this value for calculation of background intensity only
# Second value: raw attenuance value (float)
lch_tol = [
	[
		[
			[
				[0, ""] for coord_number in range(12)
			]
		 	for coord_letter in range(8)
		]
		for plate in range(2)
	]
	for category in range(2)
]

# Define categories for automated conversion of filename to index and back
category = dict()
category['ref'] = 0
category['lch'] = 1
category[0] = 'Reference'
category[1] = 'Lignocellulose hydrolysate'
shortcategory = dict()
shortcategory[0] = 'Ref.'
shortcategory[1] = 'LCH'

# Generate list of input files
# First/second value: filename
# Third/fourth value: f: full plate; t: top half; b: bottom half
# 	necessary to transform measured wells to original wells
# No bottom halves in lch-tol
filelist = [
	['ref1.txt', 'ref2.txt', 'f', 't'],
	['lch1.txt', 'lch2.txt', 'f', 't']
]

# Read files and populate lch_tol (this one is huge when printed in the shell)
for item in filelist:
	for plate in range(2):
		with open(item[plate], 'r') as f:
			f.readline() # skip first line
			cat_in = category[re.match('[a-z]{3,4}', item[plate]).group(0)]
			for coord_letter in range(8):
				for coord_number in range(12):
					line = f.readline()
					lch_tol[cat_in][plate][coord_letter][coord_number] = [1, float(re.match('[^\t]+\t[^\t]+\t([0-9]\.[0-9]+)', line).group(1))]

# Set use flag to zero for all bottom halves
for cat in range(2):
	for coord_letter in range(4,8):
		for coord_number in range(12):
			lch_tol[cat][1][coord_letter][coord_number][0] = 0

# Set use flag for other wells:
#	2 strains did not grow in the reference --> 2
#	1 empty well on Xyl1 --> 2

for cat in range(2):
	# 2 strains from Xyl1:      E10, F10
	lch_tol[cat][0][4][9][0] = 2
	lch_tol[cat][0][5][9][0] = 2
	# 1 empty well on Xyl1:     E12
	lch_tol[cat][0][4][11][0] = 2
	# 8 empty wells on Xyl2:    D5, D6, D7, D8, D9, D10, D11, D12
	lch_tol[cat][1][3][4][0]  = 2
	lch_tol[cat][1][3][5][0]  = 2
	lch_tol[cat][1][3][6][0]  = 2
	lch_tol[cat][1][3][7][0]  = 2
	lch_tol[cat][1][3][8][0]  = 2
	lch_tol[cat][1][3][9][0]  = 2
	lch_tol[cat][1][3][10][0] = 2
	lch_tol[cat][1][3][11][0] = 2

# Calculation of median background attenuance on a per-plate basis
# First value: average background attenuance, second value: list of all values,
# third value: inter-quartile range
lch_bg = [[ [0.0, [], 0.0] for plate in range(2)] for cat in range(2)]

for cat in range(2):
	for plate in range(2):
		for coord_letter in range(8):
			for coord_number in range(12):
				well = lch_tol[cat][plate][coord_letter][coord_number]
				if well[0] == 2:
					lch_bg[cat][plate][1].append(well[1])
		lch_bg[cat][plate][0] = round(np.median(lch_bg[cat][plate][1]), 7)
		lch_bg[cat][plate][2] = round(np.subtract(*np.percentile(lch_bg[cat][plate][1], [75, 25])), 7)

# Subtract background from each plate's used (=1) values
for cat in range(2):
	for plate in range(2):
		for coord_letter in range(8):
			for coord_number in range(12):
				# Use mutability...
				well = lch_tol[cat][plate][coord_letter][coord_number]
				if well[0] == 1:
					well[1] = round(well[1] - lch_bg[cat][plate][0], 7)

# Divide attenuance of inhibitor plate by attenuance of the reference plate
# Multiply with 100 to get percent values
# Reference plates remain untouched
for plate in range(2):
	for coord_letter in range(8):
		for coord_number in range(12):
			# Use mutability...
			ref = lch_tol[0][plate][coord_letter][coord_number]
			well = lch_tol[1][plate][coord_letter][coord_number]
			if well[0] == 1:
				#print("{0}.{1}.{2}.{3}: {4}; Ref.: {5}".format(cat, plate, coord_letter, coord_number, well[1], ref[1]))
				well[1] = round(100 * (well[1] / ref[1]), 1)

# Generate list for stats, never use index 0
# List is generated with 7 entries for consistency's sake
# stats contains the amount of strains in a certain interval
# The intervals are:
# 0:  <   5%          no growth
# 1: >=   5%, <  20%  rudimentary growth
# 2: >=  20%, <  40%  strongly inhibited growth
# 3: >=  40%, <  60%  moderately inhibited growth
# 4: >=  60%, <  80%  slightly inhibited growth
# 5: >=  80%, < 100%  normal growth
# 6: >= 100%, < 120%  normal growth
# 7: >= 120%          overshooting growth
lch_stats = [ [0, 0, 0, 0, 0, 0, 0, 0] for cat in range(2) ]
for plate in range(2):
	for coord_letter in range(8):
		for coord_number in range(12):
			well1 = lch_tol[1][plate][coord_letter][coord_number]
			if well1[0] == 1:
				if well1[1] >= 120:
					lch_stats[1][7] = lch_stats[1][7] + 1
				elif well1[1] >= 100:
					lch_stats[1][6] = lch_stats[1][6] + 1
				elif well1[1] >= 80:
					lch_stats[1][5] = lch_stats[1][5] + 1
				elif well1[1] >= 60:
					lch_stats[1][4] = lch_stats[1][4] + 1
				elif well1[1] >= 40:
					lch_stats[1][3] = lch_stats[1][3] + 1
				elif well1[1] >= 20:
					lch_stats[1][2] = lch_stats[1][2] + 1
				elif well1[1] >= 5:
					lch_stats[1][1] = lch_stats[1][1] + 1
				else:
					lch_stats[1][0] = lch_stats[1][0] + 1

# Output data
# For use in LaTeX document
# Background data
lch_bg_attenuance = []
for cat in range(2):
	# Curly braces are escaped not by a '\' but by another curly brace!
	bg_line = "{} & \\num{{{:.4f} \\pm {:.4f}}} & \\num{{{:.4f} \\pm {:.4f}}} \\\\".format(category[cat], round(lch_bg[cat][0][0], 4), round(lch_bg[cat][0][2]/2.0, 4), round(lch_bg[cat][1][0], 4), round(lch_bg[cat][1][2]/2.0, 4))
	# Store strings
	lch_bg_attenuance.append(bg_line)

# Distribution data
lch_dist_data = []
for cat in range(1,2):
	# Curly braces are escaped not by a '\' but by another curly brace!
	dist_line = "{} & \\num{{{}}} & \\num{{{}}} & \\num{{{}}} & \\num{{{}}} & \\num{{{}}} & \\num{{{}}} & \\num{{{}}} & \\num{{{}}} \\\\".format(category[cat], lch_stats[cat][0], lch_stats[cat][1], lch_stats[cat][2], lch_stats[cat][3], lch_stats[cat][4], lch_stats[cat][5], lch_stats[cat][6], lch_stats[cat][7])
	# Store strings
	lch_dist_data.append(dist_line)

# For use in R script
# Distribution data
with open('lch-tol-classes.txt', 'w') as f:
	# Header line
	print >> f, "\t(−∞, 5 %)\t[5 %, 20 %)\t[20 %, 40 %)\t[40 %, 60 %)\t[60 %, 80 %)\t[80 %, 100 %)\t[100 %, 120 %)\t[120 %, +∞)"
	for cat in range(1,2):
		dist_line = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(shortcategory[cat], lch_stats[cat][0], lch_stats[cat][1], lch_stats[cat][2], lch_stats[cat][3], lch_stats[cat][4], lch_stats[cat][5], lch_stats[cat][6], lch_stats[cat][7])
		print >> f, dist_line
