# -*- coding: utf-8 -*-
# # # # # # # # # # # # # # # # # # # # 
import openpyxl
import numpy as np
import operator

# # # # # # # # # # # # # # # # # # # # 
# Defines
# df = dilution factor (from hydrolysis and neutralization)
df = 5.55

# concs = concentrations in mg/l, EPS solutions for analysis
concs = dict()
# EPS1.B5 = Xyl2.C11 = Rahnella
concs['Xyl2.C11'] = 1000
concs['EPS1.B5'] = 1000
concs['G06_SK_1.B5'] = 1000
# EPS2.A11 = Xyl1.H10 = Sphingomonas
concs['Xyl1.H10'] = 4000
concs['EPS2.A11'] = 4000
concs['G07_SK_2.A11'] = 4000
# EPS2.B5 = Xyl1.F6 = Paenibacillus
concs['Xyl1.F6'] = 1000
concs['EPS2.B5'] = 1000
concs['G09_SK_2.B5'] = 1000
# EPS2.H7 = Xyl2.B8 = Paenibacillus
concs['Xyl2.B8'] = 10000
concs['EPS2.H7'] = 10000
concs['G09_SK_2.H7'] = 10000
# EPS2.H7top = Xyl2.B8top = Paenibacillus; Polymer floating on top
concs['Xyl2.B8top'] = 1000
concs['EPS2.H7top'] = 1000
concs['G10_SK_2.H7oben'] = 1000

# Name conversion for LaTeX output
# nc = name conversion
nc = dict()
nc['Xyl2.C11'] = '\\xylj{C11}'
nc['EPS1.B5'] = '\\epsi{EPS1.B5}'
nc['G06_SK_1.B5'] = '\\epsi{EPS1.B5}'
nc['Xyl1.H10'] = '\\xyli{H10}'
nc['EPS2.A11'] = '\\epsj{A11}'
nc['G07_SK_2.A11'] = '\\epsj{A11}'
nc['Xyl1.F6'] = '\\xyli{F6}'
nc['EPS2.B5'] = '\\epsj{B5}'
nc['G09_SK_2.B5'] = '\\epsj{B5}'
nc['Xyl2.B8'] = '\\xylj{B8}'
nc['EPS2.H7'] = '\\epsj{H7}'
nc['G09_SK_2.H7'] = '\\epsj{H7}'
nc['Xyl2.B8top'] = '\\xylj{B8}$^{\\text{top}}$'
nc['EPS2.H7top'] = '\\epsj{H7}$^{\\text{top}}$'
nc['G10_SK_2.H7oben'] = '\\epsj{H7}$^{\\text{top}}$'

# EPS origin column
strains = ['Strain', 'Xyl2.C11', 'Xyl1.H10', 'Xyl1.F6', 'Xyl2.B8', 'Xyl2.B8top']

# lpssd = LCH-PF Strain Selection Data
lpssd = [ [] for x in range(6) ]

# # # # # # # # # # # # # # # # # # # # 
# Input data
xlsx = openpyxl.load_workbook('scm0-results.xlsx')
data_sheet = xlsx.get_sheet_by_name('SCM0union')

# Select range with header
hdrrange = data_sheet.range('C4:U4')
# Select range with monomer data, without sum column
monorange = data_sheet.range('C9:U13')

# Populate lpssd
for cell in range(len(hdrrange[0])):
	lpssd[0].append(hdrrange[0][cell].value)
lpssd[0].append(u'Sum')
lpssd[0].append(u'Recovery')
for line in range(len(monorange)):
	for cell in range(len(monorange[line])):
		lpssd[line+1].append(monorange[line][cell].value)
	lpssd[line+1].append(0.0) # for sum
	lpssd[line+1].append(0.0) # for recovery

# Add EPS origin names
for line in range(len(lpssd)):
	lpssd[line].insert(0, strains[line])

# # # # # # # # # # # # # # # # # # # # 
# Process data
# Transpose
lpssd = np.array(lpssd).T.tolist()

# Remove lines with only 'n. n.'; read in reverse
for line in range(1, len(lpssd))[::-1]:
	#print("Line: {}, len: {}".format(line, len(lpssd[line])))
	for cell in range(1, len(lpssd[line])):
		#print("Cell: {}, value: {}".format(cell, lpssd[line][cell]))
		if ( not(lpssd[line][cell] == u'n. n.') ):
			#print("lpssd[line][cell] is not u'n. n.'. Break.")
			break
		elif (cell == len(lpssd[line]) - 1): # -1, because range(6) = [0, ..., 5]
			print("{}: no usable values detected, removing...".format(lpssd[line][0]))
			del(lpssd[line])

# Retranspose
lpssd = np.array(lpssd).T.tolist()

# Turn 'n. n.' into 'n.d.', reconvert numbers to floats
for line in range(len(lpssd)):
	for cell in range(1, len(lpssd[line])):
		if (lpssd[line][cell] == u'n. n.'):
			lpssd[line][cell] = u'n.d.'
		elif (line >= 1):
			# Monomer values are diluted --> apply dilution factor
			lpssd[line][cell] = round(float(lpssd[line][cell]) * df, 0)

# Sort by strain
lpssd.sort(key=operator.itemgetter(0))

# Recalculate sum
# Get number of sum column
# sc = sum column
for cell in range(len(lpssd[0])):
	if ( lpssd[0][cell] == u'Sum' ):
		sc = cell

for line in range(1, len(lpssd)):
	for cell in range(1, len(lpssd[line])-2): # -2, because stop before sum
		if (lpssd[line][cell] != u'n.d.'):
			lpssd[line][sc] = lpssd[line][sc] + round(lpssd[line][cell], 0)

# Calculate recovery
for line in range(1, len(lpssd)):
	lpssd[line][-1] = 100 * lpssd[line][sc] / concs[lpssd[line][0]]

# # # # # # # # # # # # # # # # # # # # 
# Construct output
# LaTeX table rows
# ltr = latex table rows
ltr = []

for line in range(1, len(lpssd)):
	# tv = table values
	tv = []
	tv.append(nc[lpssd[line][0]])
	for cell in range(1, len(lpssd[line])): # 0 is known to be a string
		if(lpssd[line][cell] == u'n.d.'):
			tv.append('{n.d.}')
		else:
			tv.append("{:.0f}".format(lpssd[line][cell]))
	# tv order is:
	#	Strain Man GlcUA GlcN Rib Rha GalN GlcNAc Glc Gal Sum Recovery
	#	   0    1    2     3   4   5    6     7    8   9   10    11
	# tl order should be:
	#	Strain Gal GalN Glc GlcN GlcNAc GlcUA Man Rha Rib Sum Recovery
	#	   0    9    6   8    3     7     2    1   5   4   10    11
	# tl = table line
	tl = "{{{}}} & {} & {} & {} & {} & {} & {} & {} & {} & {} & {} & \\SIpct{{{}}} \\\\".format(
		tv[0], tv[9], tv[6], tv[8], tv[3], tv[7], tv[2], tv[1], tv[5], tv[4], tv[10], tv[11])
	ltr.append(tl)

# CSV-style table rows for R; sum, recovery not needed
# rtr = R table rows
rtr = []

for line in range(len(lpssd)):
	# tv = table values
	tv = []
	tv.append(lpssd[line][0])
	for cell in range(1, len(lpssd[line]) - 1): # 0 is known to be a string; last is recovery, not needed
		if(lpssd[line][cell] == u'n.d.'):
			tv.append(0.0)
		else:
			tv.append(lpssd[line][cell])
	# tl = table line
	tl = "{};{};{};{};{};{};{};{};{};{}".format(
		tv[0], tv[1], tv[2], tv[3], tv[4], tv[5], tv[6], tv[7], tv[8], tv[9])
	rtr.append(tl)

print(ltr)
print(rtr)

# # # # # # # # # # # # # # # # # # # # 
# Save output to files
# LaTeX output
with open('scm0-results.tex', 'w') as f:
	for line in range(len(ltr)):
		print >> f, ltr[line]

# CSV output
with open('scm0-results.csv', 'w') as f:
	for line in range(len(rtr)):
		print >> f, rtr[line]

