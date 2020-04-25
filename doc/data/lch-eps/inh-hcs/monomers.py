# -*- coding: utf-8 -*-
import csv
import re
import numpy as np
import copy
import operator

# # # # # # # # # # # # # # # # # # # # 
# Analysis and Table Rows Generation
# Inhibitor HCS Aldose Monomer Compositions
#
# Read in, correct and analyse
#	* PMP monomer data and
#	* glucose content after gel filtration data.
#
# Generate table rows of
#	* all polymers and
#	* of selected polymers.
#
# Calibration curve:
#	[glc]_dil = 33.148 mg/l * (A418-A480) + 0.1191 mg/l
# [glc] computation:
#	[glc] = dilution factor * [glc]_dil

# Generate some dictionaries for general use
category = dict(
	[(-1, 'empty'), (0, 'Reference'), (1, 'Furfural'), 
	(2, 'Hydroxymethylfurfural'), (3, 'Vanillin'), (4, 'Acetic acid'), 
	(5, 'Formic acid'), (6, 'Laevulinic acid')])
shortcategory = dict(
	[(-1, 'mpt'), (0, 'Ref.'), (1, 'Fur.'), (2, 'HMF'), 
	(3, 'Van.'), (4, 'Acet.'), (5, 'Form.'), (6, 'Laev.'),
	 ('mpt', -1), ('Ref.', 0), ('Fur.', 1), ('HMF', 2), 
	('Van.', 3), ('Acet.', 4), ('Form.', 5), ('Laev.', 6)])
plates = dict(
	[('IS1r2pmp', 0), ('ISp', 0), ('IS1r2rez', 1), ('ISr', 1),
	(0, 'ISp'), (1, 'ISr')])
samples = dict([('Gel filtration', 0), ('Hydrolysis', 1)])

# # # # # # # # # # # # # # # # # # # # 
# Input files
# ihgm = inh-hcs glucose monomers (generated as intermediate)
with open("glc_monomers.txt", 'r') as f:
	reader = csv.reader(f, delimiter="\t")
	ihgm_in = list(reader)

# ihem = inh-hcs exopolysaccharide monomers	(generated as intermediate)
with open("ISp_monomers.txt", 'r') as f:
	reader = csv.reader(f, delimiter="\t")
	ihem_in = list(reader)
with open("ISr_monomers.txt", 'r') as f:
	reader = csv.reader(f, delimiter="\t")
	ihem_in.extend(list(reader))

# # # # # # # # # # # # # # # # # # # # 
# Pre-Processing of ihgm_in
# Remove unnecessary lines
del ihgm_in[180] # SM18 P30S with vanillin
del ihgm_in[176] # SM18 P30S with furfural
del ihgm_in[172] # SM18 P30S with HMF
del ihgm_in[84] # SM18 P30S with vanillin
del ihgm_in[80] # SM18 P30S with furfural
del ihgm_in[76] # SM18 P30S with HMF
del ihgm_in[-1] # empty line

# Transpose for the next step
ihgm_in = np.array(ihgm_in).T.tolist()

# Remove line with calculated glucose
del ihgm_in[7]

# Remove line with absorption difference
del ihgm_in[6]

# Re-transpose for the next steps
ihgm_in = np.array(ihgm_in).T.tolist()

# Conversions
for line in range(1, len(ihgm_in)):
	# cl = current line
	cl = ihgm_in[line]
	# Convert plate names to numbers
	cl[0] = plates[cl[0]]
	# Convert sample types to numbers
	cl[1] = samples[cl[1]]
	# Convert string numbers to float numbers
	for val in range(4,8):
		ihgm_in[line][val] = float(ihgm_in[line][val])

# Unset glucose concentrations
for line in range(1, len(ihgm_in)):
	ihgm_in[line][7] = float('NaN')

# # # # # # # # # # # # # # # # # # # # 
# Building ihgm
# ihgm[plate][sample][line][value]
# ihgmh = ihgm header; plate and sample colums not needed anymore
ihgmh = [copy.deepcopy(ihgm_in[0][2]), copy.deepcopy(ihgm_in[0][3]), 
	copy.deepcopy(ihgm_in[0][4]), copy.deepcopy(ihgm_in[0][5]), 
	copy.deepcopy(ihgm_in[0][6]), copy.deepcopy(ihgm_in[0][7])]
ihgm = [ [ [ihgmh] for x in range(2) ] for x in range(2) ]

for line in range(1,len(ihgm_in)):
	# cl = current line
	cl = ihgm_in[line]
	if((cl[0] == 0 or cl[0] == 1) and (cl[1] == 0 or cl[1] == 1)):
		ihgm[cl[0]][cl[1]].append([cl[2], cl[3], cl[4], cl[5], cl[6], cl[7]])

# Dilution factors given in the table are wrong
# Actual dilution factors (compared with undiluted culture supernatant):
#	Hydrolysis: 1:2 (20 µl + 20 µl)
#	Neutralization (ISp): 1:2.675 (40 µl + 67 µl)
#	Neutralization (ISr): 1:2.7 (40 µl + 68 µl)
#	Glucose assay: 1:10 (5 µl + 45 µl)
#
#	ISp:
#		1:10.0 for gel filtration
#		1:53.5 for hydrolysis
#	ISr:
#		1:10.0 for gel filtration
#		1:54.0 for hydrolysis
for plate in range(len(ihgm)):
	for sample in range(len(ihgm[plate])):
		for line in range(1, len(ihgm[plate][sample])):
			# cl = current line
			cl = ihgm[plate][sample][line]
			if(sample == 0):
				cl[4] = 10.0
			elif(sample == 1):
				if(plate == 0):
					cl[4] = 53.5
				elif(plate == 1):
					cl[4] = 54.0

# Re-calculate glucose concentrations; calibration curve: see above
for plate in range(len(ihgm)):
	for sample in range(len(ihgm[plate])):
		for line in range(1, len(ihgm[plate][sample])):
			# cl = current line
			cl = ihgm[plate][sample][line]
			cl[5] = round(cl[4] * (33.148 * (cl[2] - cl[3]) + 0.1191), 2)

# Consistency check
# Assumptions:
#	no glucose is lost due to hydrolysis
#	analyses are accurate
#	if polymer is present and contains glucose, hydrolysis frees 100% of it
# 	--> glucose concentration after hydrolysis must be >= after gel filtration
for plate in range(len(ihgm)):
	for line in range(1,len(ihgm[plate][0])):
		# gfl = gel filtration line
		gfl = ihgm[plate][0][line]
		# hl = hydrolysis line (corresponding)
		hl = ihgm[plate][1][line]
		if((hl[5] - gfl[5]) < 0):
			print("Warning: {}.{}{:2} inconsistent. Δ[glc](hyd, gf) < 0: {:8.2f} - {:8.2f} = {:8.2f}.".format(plates[plate], gfl[1], gfl[0], hl[5], gfl[5], (hl[5] - gfl[5])))

# # # # # # # # # # # # # # # # # # # # 
# Pre-Processing of ihem_in
# Remove unnecessary lines
del ihem_in[220:]    # Sugar standard 2, empty line
del ihem_in[109:136] # ISr header, sugar standards 2, 
                     # BR sample, SM18 P30S with acet./form.
del ihem_in[107:109] # SM18 P30S with vanillin, sugar standard 1, empty line
del ihem_in[79]      # SM18 P30S with furfural
del ihem_in[51]      # SM18 P30S with HMF
del ihem_in[1:24]    # sugar standards 1, SM18 P30S

# Overwrite sample number with plate identifier
# Magic number: hard-coded end of first plate
ihem_in[0][0] = 'Plate'
for line in range(1, len(ihem_in)):
	if(line < 82):
		ihem_in[line][0] = plates['ISp']
	else:
		ihem_in[line][0] = plates['ISr']

# Merge values of arabinose into xylose
# cl = current line
for line in range(1, len(ihem_in)):
	cl = ihem_in[line]
	# Three cases:
	#	both are 'n.a.' -> do nothing
	#	only ara is a number -> set xyl to number
	#	both are a number -> add ara to xyl
	if(cl[16] != 'n.a.'):
		if(cl[17] == 'n.a.'):
			cl[17] = cl[16]
		else:
			cl[17] = str(float(cl[17]) + float(cl[16]))
# Rename xylose to 'Xyl/Ara'
ihem_in[0][17] = 'Xyl/Ara'

# Transpose list to make the next step easier
ihem_in = np.array(ihem_in).T.tolist()

# Remove arabinose line
del ihem_in[16]

# Remove lines with 'n.a.' only and report the analyte
# ll = line length, el = empty lines
ll = len(ihem_in[0])
el = []
for line in range(len(ihem_in)):
	matches = 0
	for item in range(1,ll):
		if(ihem_in[line][item] == 'n.a.'):
			matches = matches + 1
	if(matches == (ll - 1)):
		el.append(line)
# Use extended slice syntax for reversing the list
for line in range(len(el))[::-1]:
	print("Line {:>6}: Contains only 'n.a.', deleting.".format(ihem_in[el[line]][0]))
	del ihem_in[el[line]]

# Convert numbers to floats, replace 'n.a.' with 'n.d.'
# cl = current line
for line in range(2,len(ihem_in)):
	cl = ihem_in[line]
	for val in range(1,len(cl)):
		if(cl[val] != 'n.a.'):
			cl[val] = float(cl[val])
		else:
			cl[val] = 'n.d.'

# Clear sum column
ihem_in[-1] = ['0.0' for x in range(len(ihem_in[0]))]
ihem_in[-1][0] = 'Sum'

# Add row (column after retransposition) for comments
ihem_in.append(['' for x in range(len(ihem_in[0]))])

# Add row for position letter (sample name will be used as position number)
ihem_in.insert(2, ['' for x in range(len(ihem_in[0]))])

# Add row for inhibitor
ihem_in.insert(1, ['' for x in range(len(ihem_in[0]))])

# Re-transpose for the next steps
ihem_in = np.array(ihem_in).T.tolist()

# Name header columns
ihem_in[0][1] = 'Inhibitor'
ihem_in[0][2] = 'Position (x)'
ihem_in[0][3] = 'Position (y)'
ihem_in[0][-1] = 'Comments'

# Split former sample names into: pos x, pos y and comment
for line in range(1,len(ihem_in)):
	# cl = current line
	cl = ihem_in[line]
	re_sults = re.search('^([A-H][01][0-9])_(Fur|HMF|Van|Am\.s\.|Es\.s\.|Lae\.s\.)_(.*)$', cl[2])
	# Replace non-standard inhibitor names
	inhibitor = re_sults.group(2)
	if(inhibitor == 'Fur'):
		inhibitor = 'Fur.'
	elif(inhibitor == 'Van'):
		inhibitor = 'Van.'
	elif(inhibitor == 'Am.s.'):
		inhibitor = 'Form.'
	elif(inhibitor == 'Es.s.'):
		inhibitor = 'Acet.'
	elif(inhibitor == 'Lae.s.'):
		inhibitor = 'Laev.'
	elif(inhibitor != 'HMF'):
		print("Warning: Unknown inhibitor '{}'.".format(inhibitor))
	cl[1] = shortcategory[inhibitor]
	cl[2] = re_sults.group(1)[1:]
	cl[3] = re_sults.group(1)[0]
	cl[-1] = re_sults.group(3)

# Convert strings to ints or floats
for line in range(1, len(ihem_in)):
	# cl = current line
	cl = ihem_in[line]
	cl[0] = int(cl[0]); cl[2] = int(cl[2])
	for val in range(4,len(cl)-1):
		if(cl[val] != 'n.d.'):
			cl[val] = float(cl[val])

# Apply dilution factors
# 	ISp: 5.35
#	ISr: 5.40
# See below for more details.
# df = dilution factors
df = [5.35, 5.40]
for line in range(1, len(ihem_in)):
	# cl = current line
	cl = ihem_in[line]
	for val in range(4, len(ihem_in[line])-1):
		# cv = current value
		cv = ihem_in[line][val]
		if(cv != 'n.d.'):
			cl[val] = round(df[cl[0]] * cv, 2)

# # # # # # # # # # # # # # # # # # # # 
# Building ihem
# ihem[plate][line][value]
# ihemh = ihem header; plate colum not needed anymore
ihemh = copy.deepcopy(ihem_in[0])
del ihemh[0]
ihem = [ [ihemh] for x in range(2) ]

for line in range(1, len(ihem_in)):
	# cl = current line
	cl = ihem_in[line]
	ihem[ihem_in[line][0]].append(copy.deepcopy(cl))
	# Delete plate number
	del ihem[ihem_in[line][0]][-1][0]

# Sort ihem plates by letter and number
# Remove headers for sorting
del ihem[0][0]
del ihem[1][0]
# Sort
ihem[0].sort(key=operator.itemgetter(2, 1))
ihem[1].sort(key=operator.itemgetter(2, 1))
# Add headers back
ihem[0].insert(0, ihemh)
ihem[1].insert(0, ihemh)

# # # # # # # # # # # # # # # # # # # # 
# Combining ihem and ihgm
# Subtract glucose from after gel filtration
for plate in range(len(ihem)):
	for line in range(1, len(ihem[plate])):
		# ecl = ihem current line
		# gcl = ihgm current line
		ecl = ihem[plate][line]
		gcl = ihgm[plate][0][line]
		if(ecl[11] != 'n.d.'):
			# cglc = corrected glucose concentration
			cglc = round(ecl[11] - gcl[5], 2)
			if(cglc < 0):
				print("Warning: {}.{}{:<2} inconsistent. Δ[glc](pmp, gf) < 0: {:7.2f} - {:7.2f} = {: 7.2f}. Δ[glc](pmp, gf) set to 0.".format(plates[plate], ecl[2], ecl[1], ecl[11], gcl[5], cglc))
				cglc = 0.0
			ecl[11] = cglc
		else:
			print("Warning: No monomeric glucose reported for {}.{}{:<2}, treated as 0. Δ[glc](pmp, gf) < 0: {:7.2f} - {:7.2f} = {: 7.2f}. Δ[glc](pmp, gf) left as 'n.d.'.".format(plates[plate], ecl[2], ecl[1], 0, gcl[5], -gcl[5]))
		# Re-calculate sum
		for val in range(3, len(ecl)-2):
			# cv = current value
			cv = ihem[plate][line][val]
			if(cv != 'n.d.'):
				ecl[-2] = ecl[-2] + cv
		ecl[-2] = round(ecl[-2], 2)

# # # # # # # # # # # # # # # # # # # # 
# Prepare statistics
# ihems = inh-hcs exopolysaccharide cumulative monomers statistics
# Results format: [[values], lower quartile, median, upper quartile, 1/2IQR]
# One list per inhibitor (0 left untouched)
ihems = [ [[], 0.0, 0.0, 0.0, 0.0] for inhibitor in range(7) ]

for plate in range(len(ihem)):
	for line in range(1, len(ihem[plate])):
		# cl = current line
		cl = ihem[plate][line]
		ihems[cl[0]][0].append(cl[-2])

for inhibitor in range(1, 7):
	ihems[inhibitor][1] = int(round(np.percentile(ihems[inhibitor][0], 25), 0))
	ihems[inhibitor][2] = int(round(np.median(ihems[inhibitor][0]), 0))
	ihems[inhibitor][3] = int(round(np.percentile(ihems[inhibitor][0], 75), 0))
	ihems[inhibitor][4] = int(round(0.5*(np.subtract(*np.percentile(ihems[inhibitor][0], [75, 25]))), 0))

# # # # # # # # # # # # # # # # # # # # 
# Construct table rows
# For use in LaTeX document
with open('monomers.tex', 'w') as f:
	for plate in range(len(ihem)):
		for line in range(1, len(ihem[plate])):
			# cl = current line
			cl = ihem[plate][line]
			# Input columns:
			# Man (3), GlcUA (4), GlcN (5), Rib (6), Rha (7), Gen (8),
			# GalN (9), Cel (10), Glc (11), Gal (12), Xyl/Ara (13),
			# Fuc (14), Sum (15)
			# Output columns:
			# Cel, Fuc, Gal, GalN, Gen, Glc, GlcN, GlcUA,
			# Man, Rha, Rib, Xyl/Ara, Sum
			# itl = ihem table line, itlc = itl contents
			# cl[0]: inhibitor; cl[1]: x; cl[2]: y
			itlc = [cl[0], cl[1], cl[2]]
			for val in range(3, len(cl)-2):
				if(cl[val] == 'n.d.'):
					itlc.append('{n.d.}')
				else:
					itlc.append(int(round(cl[val], 0)))
			itlc.append(0)
			# Re-calculate sums to remove rounding errors
			for val in range(3, len(itlc)-1):
				if(itlc[val] != '{n.d.}'):
					itlc[-1] = itlc[-1] + itlc[val]
			itl = "{{{}.{}{}}} & {{{}}} & {} & {} & {} & {} & {} & {} & {} & {} & {} & {} & {} & {} & {} \\\\".format(
				plates[plate], itlc[2], itlc[1], shortcategory[itlc[0]], # plate, y, x, inhibitor, 
				itlc[10], itlc[14], itlc[12], itlc[9], # cel, fuc, gal, galn, 
				itlc[8], itlc[11], itlc[5], itlc[4], # gen, glc, glcn, glcua,
				itlc[3], itlc[7], itlc[6], itlc[13], # man, rha, 2drib, rib, xyl/ara,
				itlc[15]) # sum
			print >> f, itl

# Prepare table with summary statistics
with open('monomers-stats.tex', 'w') as f:
	for inhibitor in range(1, len(ihems)):
		# isl = ihems line
		isl = "{{{}}} & {} & {} & {} \\\\".format(
			category[inhibitor],
			ihems[inhibitor][1],
			ihems[inhibitor][2],
			ihems[inhibitor][3])
		print >> f, isl

# # # # # # # # # # # # # # # # # # # # 
# Output sorted by inhibitor, sum
#del ihem[0][0]
#del ihem[1][0]
#ihem[0].sort(key=operator.itemgetter(0, 18))
#ihem[1].sort(key=operator.itemgetter(0, 18))
#for plate in range(len(ihem)):
#	for line in range(len(ihem[plate])):
#		print(ihem[plate][line])
