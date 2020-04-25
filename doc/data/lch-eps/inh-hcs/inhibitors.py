# -*- coding: utf-8 -*-
import csv
import re
import copy
import numpy as np
import operator

# Input table layout (ISp)
#	Sample Name, Furfural, HMF, Vanillin
# Input table layout (ISr)
#	Sample Name, Acetic acid, Formic acid, Laevulinic acid
#
# Sample name layouts
# 	A01_HMF_X1.A07
#	G08_Fur_SM18_P30S
#	H10_3Mix_002
#	H12_SM18_P30S
#
# inh_hcs table layout
#	0: ISp; 1: ISr
#	Well (y), Well (x), Inhibitor, Comment
#	Conc. Furfural/Acetic acid, 
#	Conc. HMF/Formic acid, 
#	Conc. Vanillin/Laevulinic acid, 
# 	Original value of conc. Furfural/Acetic acid, 
# 	Original value of conc. HMF/Formic acid, 
# 	Original value of conc. Vanillin/Laevulinic acid
# Inhibitor
# 0: Furfural, 1: HMF, 2: Vanillin, 
# 3: Acetic acid, 4: Formic acid, 5: Laevulinic acid

inh_hcs = [[] for x in range(2)]

category = dict()
category['Fur'] = 0
category['HMF'] = 1
category['Van'] = 2
category['Es.s.'] = 3
category['Am.s.'] = 4
category['Lae.s.'] = 5
category[0] = 'Furfural'
category[1] = 'Hydroxymethylfurfural'
category[2] = 'Vanillin'
category[3] = 'Acetic acid'
category[4] = 'Formic acid'
category[5] = 'Laevulinic acid'
shortcategory = dict()
shortcategory[0] = 'Fur.'
shortcategory[1] = 'HMF'
shortcategory[2] = 'Van.'
shortcategory[3] = 'Acet.'
shortcategory[4] = 'Form.'
shortcategory[5] = 'Laev.'

# Read files and populate inh_hcs
with open("ISp_inhibitors.txt", 'r') as f:
	reader = csv.reader(f, delimiter="\t")
	ISp_in = list(reader)
with open("ISr_inhibitors.txt", 'r') as f:
	reader = csv.reader(f, delimiter="\t")
	ISr_in = list(reader)

# # # # # # # # # # # # # # # # # # # # 
# Prepare ISp_in and ISr_in
# Remove lines not necessary for analysis
del ISp_in[0:14]
del ISp_in[-4:]
del ISr_in[0:17]
del ISr_in[-1]
del ISr_in[-4]

# Remove lines of non-growing strains
del ISp_in[74]
del ISp_in[54]
del ISp_in[50]
del ISp_in[37]
del ISp_in[33]
del ISr_in[63]

# Change some entries to match the standard
# H10_SM18_P30S_+_2_g/l_Am.s. --> H10_Am.s._SM18_P30S
# Lä.s. -> Lae.s.
for well in range(len(ISr_in)):
	cur_well = ISr_in[well]
	if(re.search('_\+_2_g/l', cur_well[0])):
		cur_well[0] = re.sub('^([A-H][01][0-9])_(.*)_\+_2_g/l_(.*)$', '\g<1>_\g<3>_\g<2>', cur_well[0])
		cur_well[0] = re.sub('Lä\.s\.', 'Lae.s.', cur_well[0])

# # # # # # # # # # # # # # # # # # # # 
# Post-processing of ISp_in
# Convert "n.a." to 0.0
# Convert text to numbers
# Make numbers < 0.0 equal 0.0
# ISp only: Set numbers > 2000 equal 2000.0
# Split sample name into coordinates and category
for well in range(len(ISp_in)):
	cur_well = ISp_in[well]
	ori_well = copy.deepcopy(ISp_in[well])
	for val in range(1, 4):
		if(re.match('^n\.a\.$', cur_well[val])):
			cur_well[val] = 0.0
			print("{} has been tampered with! Set to 0.0, value was 'n.a.'.".format(cur_well[0]))
		else:
			cur_well[val] = float(cur_well[val])
			if (cur_well[val] < 0.0):
				print("{} has been tampered with! Set to 0.0, value was {}.".format(cur_well[0], cur_well[val]))
				cur_well[val] = 0.0
			elif (cur_well[val] > 2000.0):
				print("{} has been tampered with! Set to 2000.0, value was {}.".format(cur_well[0], cur_well[val]))
				cur_well[val] = 2000.0
	re_sult = re.match('([A-H])([01][0-9])_(Fur|HMF|Van)_?(.*)', cur_well[0])
	inh_hcs[0].append([re_sult.group(1), int(re_sult.group(2)), category[re_sult.group(3)], re_sult.group(4), cur_well[1], cur_well[2], cur_well[3], ori_well[1], ori_well[2], ori_well[3]])

# Sort inh_hcs[0] by well
inh_hcs[0].sort(key=operator.itemgetter(0, 1))

# # # # # # # # # # # # # # # # # # # # 
# Post-processing of ISr_in
# Convert "n.a." to 0.0
# Convert text to numbers
# Make numbers < 0.0 equal 0.0
# Split sample name into coordinates and category
for well in range(len(ISr_in)):
	cur_well = ISr_in[well]
	ori_well = copy.deepcopy(ISr_in[well])
	for val in range(1, 4):
		if(re.match('^n\.a\.$', cur_well[val])):
			cur_well[val] = 0.0
			print("{} has been tampered with! Set to 0.0, value was 'n.a.'.".format(cur_well[0]))
		else:
			cur_well[val] = float(cur_well[val])
			if (cur_well[val] < 0.0):
				print("{} has been tampered with! Set to 0.0, value was {}.".format(cur_well[0], cur_well[val]))
				cur_well[val] = 0.0
	re_sult = re.match('([A-H])([01][0-9])_(Am\.s\.|Es\.s\.|Lae\.s\.)_?(.*)', cur_well[0])
	inh_hcs[1].append([re_sult.group(1), int(re_sult.group(2)), category[re_sult.group(3)], re_sult.group(4), cur_well[1], cur_well[2], cur_well[3], ori_well[1], ori_well[2], ori_well[3]])

# Sort inh_hcs[1] by well
inh_hcs[1].sort(key=operator.itemgetter(0, 1))

# # # # # # # # # # # # # # # # # # # # 
# Results Preparation
# Select only sample lines
# Results format: [lower quartile, median, upper quartile, 1/2IQR, [values]]
# ihr = inh_hcs_results
ihr = [['', '', '', '', []] for x in range(6)]

plate = inh_hcs[0]
for inhibitor in range(3):
	for well in range(len(plate)):
		cur_well = plate[well]
		# Do not consider medium controls G4, G8, G12 --> have "SM18_P30S" in the name
		if((cur_well[2] == inhibitor) and not(re.match('SM18_P30S', cur_well[3]))):
			ihr[inhibitor][4].append(plate[well][inhibitor+4])
	# Convert from mg/l to g/l --> round(0.001*..., 2)
	ihr[inhibitor][0] = round(0.001*(np.percentile(ihr[inhibitor][4], 25)), 2)
	ihr[inhibitor][1] = round(0.001*(np.median(ihr[inhibitor][4])), 2)
	ihr[inhibitor][2] = round(0.001*(np.percentile(ihr[inhibitor][4], 75)), 2)
	ihr[inhibitor][3] = round(0.5 * 0.001*(np.subtract(*np.percentile(ihr[inhibitor][4], [75, 25]))), 2)

plate = inh_hcs[1]
for inhibitor in range(3, 6):
	for well in range(len(plate)):
		cur_well = plate[well]
		if((cur_well[2] == inhibitor) and not(re.match('SM18_P30S', cur_well[3]))):
			ihr[inhibitor][4].append(plate[well][inhibitor+1])
	# Unit: g/l --> round(, 2)
	ihr[inhibitor][0] = round(np.percentile(ihr[inhibitor][4], 25), 2)
	ihr[inhibitor][1] = round(np.median(ihr[inhibitor][4]), 2)
	ihr[inhibitor][2] = round(np.percentile(ihr[inhibitor][4], 75), 2)
	ihr[inhibitor][3] = round(0.5 * np.subtract(*np.percentile(ihr[inhibitor][4], [75, 25])), 2)

# # # # # # # # # # # # # # # # # # # # 
# Construct table rows
# For use in LaTeX document
# iht = inh-hcs table rows, used for stats
with open('inhibitors-stats.tex', 'w') as f:
	for inhibitor in range(6):
		iht_line = "{{{}}} & {:.2f} & {:.2f} & {:.2f} \\\\".format(category[inhibitor], ihr[inhibitor][0], ihr[inhibitor][1], ihr[inhibitor][2])
		print >> f, iht_line

with open('inhibitors-stats.txt', 'w') as f:
	for inhibitor in range(6):
		iht_line = "{}\t{:.2f}\t{:.2f}\t{:.2f}".format(category[inhibitor], ihr[inhibitor][0], ihr[inhibitor][1], ihr[inhibitor][2])
		print >> f, iht_line

# ihtf = iht_full = all inh-hcs table rows, unaltered
with open('inhibitors-ISp-full.tex', 'w') as f:
	for well in range(len(inh_hcs[0])):
		cur_well = inh_hcs[0][well]
		# Well, Inhibitor tested, Fur., HMF, Van.
		ihtf_line = "{{{}{}}} & {{{}}} & {} & {} & {} \\\\".format(cur_well[0], cur_well[1], category[cur_well[2]], cur_well[7], cur_well[8], cur_well[9])
		ihtf_line = re.sub('n.a.', '{n.d.}', ihtf_line)
		print >> f, ihtf_line

with open('inhibitors-ISr-full.tex', 'w') as f:
	for well in range(len(inh_hcs[1])):
		cur_well = inh_hcs[1][well]
		# Well, Inhibitor tested, Acet., Form., Laev.
		ihtf_line = "{{{}{}}} & {{{}}} & {} & {} & {} \\\\".format(cur_well[0], cur_well[1], category[cur_well[2]], cur_well[7], cur_well[8], cur_well[9])
		ihtf_line = re.sub('n.a.', '{n.d.}', ihtf_line)
		print >> f, ihtf_line
