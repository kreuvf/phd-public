# -*- coding: utf-8 -*-
import csv
import re
import numpy as np
import operator

# Input table
#	Plate, Position (x/Number), Position (y/Letter), 
#	Absorption (dimensionless) at 418 nm, Absorption (dimensionless) at 480 nm, 
#	Absorption difference, Calculated glucose in mg/l, 
#	Dilution factor, Glucose concentration in mg/l (undiluted)
#
# ihgc = inh-hcs glucose consumption
# ihgc layout
#	Plate, Position (y/Letter), Position (x/Number), Inhibitor,
#	A418, A480, Dilution factor, [glc] in g/l (undiluted)
# Plate:
#	0 = ISp, 1 = ISr
# Inhibitor:
#	ISp:
#		A1 to G4 : HMF
#		A5 to G8 : Furfural
#		A9 to G12: Vanillin
#		G4, G8, G12 = medium wells
#	ISr:
#		A1 to G4 : Formic acid
#		A5 to G8 : Acetic acid
#		A9 to G12: Laevulinic acid
# Calibration curve:
#	[glc]_dil = 36.554 mg/l * (A418-A480) - 0.8274 mg/l
# [glc] computation:
#	[glc] = 0.001 mg/g * dilution factor * [glc]_dil

ihgc = [[] for x in range(2)]

category = dict()
category[-1] = 'empty'
category[0] = 'Reference'
category[1] = 'Furfural'
category[2] = 'Hydroxymethylfurfural'
category[3] = 'Vanillin'
category[4] = 'Acetic acid'
category[5] = 'Formic acid'
category[6] = 'Laevulinic acid'
shortcategory = dict()
shortcategory[-1] = 'mpt'
shortcategory[0] = 'Ref.'
shortcategory[1] = 'Fur.'
shortcategory[2] = 'HMF'
shortcategory[3] = 'Van.'
shortcategory[4] = 'Acet.'
shortcategory[5] = 'Form.'
shortcategory[6] = 'Laev.'
platedict = dict()
platedict['IS1r2pmp'] = 0
platedict['ISp'] = 0
platedict['IS1r2rez'] = 1
platedict['ISr'] = 1

# Read file
with open("glc_consumption.txt", 'r') as f:
	reader = csv.reader(f, delimiter="\t")
	ihgc_in = list(reader)

# # # # # # # # # # # # # # # # # # # # 
# Prepare ihgc_in
# Remove lines not necessary for analysis
del ihgc_in[0]
del ihgc_in[-1]

# Remove lines of non-growing strains
del ihgc_in[119]
del ihgc_in[78]
del ihgc_in[66]
del ihgc_in[58]
del ihgc_in[29]
del ihgc_in[17]

# # # # # # # # # # # # # # # # # # # # 
# Populating ihgc
for line in range(len(ihgc_in)):
	# Set inhibitor to value for 'untouched'
	inhibitor = -2
	cur_line = ihgc_in[line]
	if(cur_line[0] == 'IS1r2pmp'):
		# G4, G8, G12 = medium with inhibitor
		if((cur_line[2] == 'G') and ((cur_line[1] == '4') or (cur_line[1] == '8') or (cur_line[1] == '12'))):
			inhibitor = 0
		elif(cur_line[2] == 'H'):
			if(cur_line[1] == '12'):
				inhibitor = 0
			else:
				inhibitor = -1
		else:
			if(int(cur_line[1]) <= 4):
				inhibitor = 2
			elif(int(cur_line[1]) <= 8):
				inhibitor = 1
			else:
				inhibitor = 3
	elif (cur_line[0] == 'IS1r2rez'):
		if(not(cur_line[2] == 'H')):
			if(int(cur_line[1]) <= 4):
				inhibitor = 5
			elif(int(cur_line[1]) <= 8):
				inhibitor = 4
			else:
				inhibitor = 6
		else:
			if(int(cur_line[1]) >= 9):
				inhibitor = 0
			else:
				inhibitor = -1
	else:
		print("Bad input. Plate should be 'IS1r2pmp' or 'IS1r2rez', but is '{}'.".format(cur_line[0]))
		break
	# Calibration curve data see above
	glc_dil = 36.554 * (float(cur_line[3]) - float(cur_line[4])) - 0.8274
	glc = round(0.001 * float(cur_line[7]) * glc_dil, 4)
	ihgc_line = [platedict[cur_line[0]], cur_line[2], int(cur_line[1]), inhibitor,
		float(cur_line[3]), float(cur_line[4]), float(cur_line[7]), glc]

	if(ihgc_line[0] == 0):
		ihgc[0].append(ihgc_line)
	elif(ihgc_line[0] == 1):
		ihgc[1].append(ihgc_line)

# Sort per plate based on the inhibitor
ihgc[0].sort(key=operator.itemgetter(1, 2))
ihgc[1].sort(key=operator.itemgetter(1, 2))

# # # # # # # # # # # # # # # # # # # # 
# Per inhibitor statistics
# ihgcs = ihgc statistics
# Count negative values as zero
# ihgcs layout:
#	Values of inhibitor, lower quartile, median, upper quartile
ihgcs = [ [[], -1.0, -1.0, -1.0] for x in range(7) ]
for plate in range(2):
	for line in range(len(ihgc[plate])):
		# cl = current line
		cl = ihgc[plate][line]
		clglc = max(cl[7], 0)
		if cl[3] >= 0: # Do not consider empty/tainted wells
			ihgcs[cl[3]][0].append(clglc)

for inhibitor in range(len(ihgcs)):
	ihgcs[inhibitor][1] = np.percentile(ihgcs[inhibitor][0], 25)
	ihgcs[inhibitor][2] = np.median(ihgcs[inhibitor][0])
	ihgcs[inhibitor][3] = np.percentile(ihgcs[inhibitor][0], 75)

# # # # # # # # # # # # # # # # # # # # 
# Results Preparation
# Table rows of the complete results
with open('glc-consumption-isp-full.tex', 'w') as f:
	plate = 0
	for line in range(len(ihgc[plate])):
		# cl = current line
		cl = ihgc[plate][line]
		if(cl[3] >= 0):
			row = "{{{}{}}} & {{{}}} & {} & {} & {} & {} \\\\".format(
				cl[1], cl[2], category[cl[3]], cl[4], cl[5], int(cl[6]), cl[7])
			print >> f, row

with open('glc-consumption-isr-full.tex', 'w') as f:
	plate = 1
	for line in range(len(ihgc[plate])):
		# cl = current line
		cl = ihgc[plate][line]
		if(cl[3] >= 0):
			row = "{{{}{}}} & {{{}}} & {} & {} & {} & {} \\\\".format(
				cl[1], cl[2], category[cl[3]], cl[4], cl[5], int(cl[6]), cl[7])
			print >> f, row

with open('glc-consumption-stats.tex', 'w') as f:
	for inhibitor in range(len(ihgcs)):
		# cl = current line
		cl = ihgcs[inhibitor]
		row = "{{{}}} & {:.2f} & {:.2f} & {:.2f} \\\\".format(category[inhibitor], cl[1], cl[2], cl[3])
		print >> f, row
