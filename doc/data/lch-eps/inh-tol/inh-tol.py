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
# Category: 0..6 = reference, furfural, hydroxymethylfurfural,
#                  vanillin, acetic acid, formic acid,
#                  laevulinic acid
# plate: 0 = Xyl1, 1 = Xyl2
# Coordinate (letter): 0...7 = A..H
# Coordinate (number): 0..11 = 1..12
# First value: use flag
#	0: Do not use this value for calculation at all
#	1: Use this value for calculation as a normal value
#	2: Use this value for calculation of background intensity only
# Second value: raw attenuance value (float)
inh_tol = [
	[
		[
			[
				[0, ""] for coord_number in range(12)
			]
		 	for coord_letter in range(8)
		]
		for plate in range(2)
	]
	for category in range(7)
]

# Define categories for automated conversion of filename to index and back
category = dict()
category['ref'] = 0
category['fur'] = 1
category['hmf'] = 2
category['van'] = 3
category['acet'] = 4
category['form'] = 5
category['laev'] = 6
category[0] = 'Reference'
category[1] = 'Furfural'
category[2] = 'Hydroxymethylfurfural'
category[3] = 'Vanillin'
category[4] = 'Acetic acid'
category[5] = 'Formic acid'
category[6] = 'Laevulinic acid'
shortcategory = dict()
shortcategory[0] = 'Ref.'
shortcategory[1] = 'Fur.'
shortcategory[2] = 'HMF'
shortcategory[3] = 'Van.'
shortcategory[4] = 'Acet.'
shortcategory[5] = 'Form.'
shortcategory[6] = 'Laev.'
plateconv = dict()
plateconv[0] = 'Xyl1'
plateconv[1] = 'Xyl2'
letterconv = dict()
letterconv[0] = 'A'
letterconv[1] = 'B'
letterconv[2] = 'C'
letterconv[3] = 'D'
letterconv[4] = 'E'
letterconv[5] = 'F'
letterconv[6] = 'G'
letterconv[7] = 'H'
numberconv = dict()
numberconv[0] = 1
numberconv[1] = 2
numberconv[2] = 3
numberconv[3] = 4
numberconv[4] = 5
numberconv[5] = 6
numberconv[6] = 7
numberconv[7] = 8
numberconv[8] = 9
numberconv[9] = 10
numberconv[10] = 11
numberconv[11] = 12

# Generate list of input files
# First/second value: filename
# Third/fourth value: f: full plate; t: top half; b: bottom half
# 	necessary to transform measured wells to original wells
filelist = [
	['ref1.txt', 'ref2.txt', 'f', 'b'],
	['fur1.txt', 'fur2.txt', 'f', 'b'],
	['hmf1.txt', 'hmf2.txt', 'f', 't'],
	['van1.txt', 'van2.txt', 'f', 'b'],
	['acet1.txt', 'acet2.txt', 'f', 'b'],
	['form1.txt', 'form2.txt', 'f', 't'],
	['laev1.txt', 'laev2.txt', 'f', 't']
]

# Read files and populate inh_tol (this one is huge when printed in the shell)
for item in filelist:
	for plate in range(2):
		with open(item[plate], 'r') as f:
			f.readline() # skip first line
			cat_in = category[re.match('[a-z]{3,4}', item[plate]).group(0)]
			for coord_letter in range(8):
				for coord_number in range(12):
					line = f.readline()
					inh_tol[cat_in][plate][coord_letter][coord_number] = [1, float(re.match('[^\t]+\t[^\t]+\t([0-9]\.[0-9]+)', line).group(1))]

# Transform bottom halves to top halves
# Reduces the amount of differences we will have to deal with
# Basically: tr E-H A-D
# only for Xyl2 plates, that means: plate = 1
for cat in (0, 1, 3, 4):
	for coord_letter in range(4,8):
		# deepcopy due to lists being mutable
		inh_tol[cat][1][coord_letter-4] = copy.deepcopy(inh_tol[cat][1][coord_letter])

# Set use flag to zero for all bottom halves
for cat in range(7):
	for coord_letter in range(4,8):
		for coord_number in range(12):
			inh_tol[cat][1][coord_letter][coord_number][0] = 0

# Set use flag for other wells:
#	7 strains did not grow in the reference --> 2
#	1 strain did not grow in the reference --> 2
#	1 empty well on Xyl1 --> 2
#   8 empty wells on Xyl2 --> 2
# 	1 empty well on laev2 grew (contamination) --> 0

for cat in range(7):
	# 7 strains from Xyl1:      A4, E11, F11, G4, G6, G8, G10
	inh_tol[cat][0][0][3][0]  = 2
	inh_tol[cat][0][4][10][0] = 2
	inh_tol[cat][0][5][10][0] = 2
	inh_tol[cat][0][6][3][0]  = 2
	inh_tol[cat][0][6][5][0]  = 2
	inh_tol[cat][0][6][7][0]  = 2
	inh_tol[cat][0][6][9][0]  = 2
	# 1 strain from Xyl2:       C1
	inh_tol[cat][1][2][0][0]  = 2
	# 1 empty well on Xyl1:     E12
	inh_tol[cat][0][4][11][0] = 2
	# 8 empty wells on Xyl2:    D5, D6, D7, D8, D9, D10, D11, D12
	inh_tol[cat][1][3][4][0]  = 2
	inh_tol[cat][1][3][5][0]  = 2
	inh_tol[cat][1][3][6][0]  = 2
	inh_tol[cat][1][3][7][0]  = 2
	inh_tol[cat][1][3][8][0]  = 2
	inh_tol[cat][1][3][9][0]  = 2
	inh_tol[cat][1][3][10][0] = 2
	inh_tol[cat][1][3][11][0] = 2

# 1 contamination in laev2: D9
inh_tol[6][1][3][8][0] = 0

# Calculation of median background attenuance on a per-plate basis
# First value: average background attenuance, second value: list of all values,
# third value: inter-quartile range
bg = [[ [0.0, [], 0.0] for plate in range(2)] for cat in range(7)]

for cat in range(7):
	for plate in range(2):
		for coord_letter in range(8):
			for coord_number in range(12):
				well = inh_tol[cat][plate][coord_letter][coord_number]
				if well[0] == 2:
					bg[cat][plate][1].append(well[1])
		bg[cat][plate][0] = round(np.median(bg[cat][plate][1]), 7)
		bg[cat][plate][2] = round(np.subtract(*np.percentile(bg[cat][plate][1], [75, 25])), 7)

# Subtract background from each plate's used (=1) values
for cat in range(7):
	for plate in range(2):
		for coord_letter in range(8):
			for coord_number in range(12):
				# Use mutability...
				well = inh_tol[cat][plate][coord_letter][coord_number]
				if well[0] == 1:
					well[1] = round(well[1] - bg[cat][plate][0], 7)

# Divide attenuance of inhibitor plate by attenuance of the reference plate
# Multiply with 100 to get percent values
# Reference plates remain untouched
for cat in range(1,7):
	for plate in range(2):
		for coord_letter in range(8):
			for coord_number in range(12):
				# Use mutability...
				ref = inh_tol[0][plate][coord_letter][coord_number]
				well = inh_tol[cat][plate][coord_letter][coord_number]
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
stats = [ [0, 0, 0, 0, 0, 0, 0, 0] for cat in range(7) ]
for cat in range(1,7):
	for plate in range(2):
		for coord_letter in range(8):
			for coord_number in range(12):
				well1 = inh_tol[cat][plate][coord_letter][coord_number]
				# Only work with values flagged as normal (1)
				if well1[0] == 1:
					if well1[1] >= 120:
						stats[cat][7] = stats[cat][7] + 1
						# GIve details of each excessive grower
						print("{}\t{}.{}{}\t{}\tRef.\t{}".format(
							category[cat], plateconv[plate],
							letterconv[coord_letter], numberconv[coord_number],
							well1[1], inh_tol[0][plate][coord_letter][coord_number][1])
						)
					elif well1[1] >= 100:
						stats[cat][6] = stats[cat][6] + 1
					elif well1[1] >= 80:
						stats[cat][5] = stats[cat][5] + 1
					elif well1[1] >= 60:
						stats[cat][4] = stats[cat][4] + 1
					elif well1[1] >= 40:
						stats[cat][3] = stats[cat][3] + 1
					elif well1[1] >= 20:
						stats[cat][2] = stats[cat][2] + 1
					elif well1[1] >= 5:
						stats[cat][1] = stats[cat][1] + 1
					else:
						stats[cat][0] = stats[cat][0] + 1

# Output data
# For use in LaTeX document
# Background data
bg_attenuance = []
for cat in range(7):
	# Curly braces are escaped not by a '\' but by another curly brace!
	bg_line = "{} & \\num{{{:.4f} \\pm {:.4f}}} & \\num{{{:.4f} \\pm {:.4f}}} \\\\".format(category[cat], round(bg[cat][0][0], 4), round(bg[cat][0][2]/2.0, 4), round(bg[cat][1][0], 4), round(bg[cat][1][2]/2.0, 4))
	# Store strings
	bg_attenuance.append(bg_line)

# Distribution data
dist_data = []
for cat in range(1,7):
	# Curly braces are escaped not by a '\' but by another curly brace!
	dist_line = "{} & \\num{{{}}} & \\num{{{}}} & \\num{{{}}} & \\num{{{}}} & \\num{{{}}} & \\num{{{}}} & \\num{{{}}} & \\num{{{}}} \\\\".format(category[cat], stats[cat][0], stats[cat][1], stats[cat][2], stats[cat][3], stats[cat][4], stats[cat][5], stats[cat][6], stats[cat][7])
	# Store strings
	dist_data.append(dist_line)

# For use in R script
# Distribution data
with open('inh-tol-classes.txt', 'w') as f:
	# Header line
	print >> f, "\t(−∞, 5 %)\t[5 %, 20 %)\t[20 %, 40 %)\t[40 %, 60 %)\t[60 %, 80 %)\t[80 %, 100 %)\t[100 %, 120 %)\t[120 %, +∞)"
	for cat in range(1,7):
		dist_line = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(shortcategory[cat], stats[cat][0], stats[cat][1], stats[cat][2], stats[cat][3], stats[cat][4], stats[cat][5], stats[cat][6], stats[cat][7])
		print >> f, dist_line
