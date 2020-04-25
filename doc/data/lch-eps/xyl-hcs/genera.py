# # # # # # # # # # # # # # # # # # # #
# Statistics on a per-genus base
# # # # # # # # # # # # # # # # # # # #
import openpyxl
import numpy as np


# # # # # # # # # # # # # # # # # # # #
# Define constants, functions
# # # # # # # # # # # # # # # # # # # #
# dictaddinv: Invert key value pairs and add to dictionary
# Source: http://code.activestate.com/recipes/252143-invert-a-dictionary-one-liner/#c6
def dictaddinv(d):
	assert len(d) == len(dict([v,k] for k,v in d.iteritems())), 'Duplicate value in dictionary.'
	d.update(dict([v,k] for k,v in d.iteritems()))

# Mask for strain assignment
# 0: empty; 1: Arthrobacter; 2: Bacillus; 3: Microbacterium
# 4: Paenibacillus; 5: Pseudomonas; 6: Rhodococcus; 7: Sphingomonas
# genmap = genera map
genmap = \
	[
		[ 1 for x in range(12) ],
		[ 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2 ],
		[ 2 for x in range(12) ],
		[ 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3 ],
		[ 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 0 ], # E10 did not grow
		[ 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5 ],
		[ 5 for x in range(12) ],
		[ 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 7 ]
	]

# Define genus names <-> numbers
genusdict = dict()
genusdict[0] = 'empty'
genusdict[1] = 'Arthrobacter'
genusdict[2] = 'Bacillus'
genusdict[3] = 'Microbacterium'
genusdict[4] = 'Paenibacillus'
genusdict[5] = 'Pseudomonas'
genusdict[6] = 'Rhodococcus'
genusdict[7] = 'Sphingomonas'
dictaddinv(genusdict)

# Dilution factor: 50
difa = 50

# Define row to letter dict
wellx = dict()
wellx[0] = 'A'; wellx[1] = 'B'
wellx[2] = 'C'; wellx[3] = 'D'
wellx[4] = 'E'; wellx[5] = 'F'
wellx[6] = 'G'; wellx[7] = 'H'

# # # # # # # # # # # # # # # # # # # #
# Input raw data
# # # # # # # # # # # # # # # # # # # #
xlsx = openpyxl.load_workbook('summary.xlsx')
data_sheet = xlsx.get_sheet_by_name('Tabelle1')

# Select ranges, xylose concentration (diluted value)
xyl1_array = data_sheet.range('B7:M14')


# # # # # # # # # # # # # # # # # # # #
# Processing
# # # # # # # # # # # # # # # # # # # #
# Build lists for single genera: gd = genus data
# Apply dilution factor here as well, convert from mg/l to g/l = factor 0.001
gd = [ [] for x in range(8) ]
for row in range(len(genmap)):
	for col in range(len(genmap[row])):
		genus = genmap[row][col]
		val = round(float(xyl1_array[row][col].value * difa * 0.001), 2)
		gd[genus].append(val)


# # # # # # # # # # # #
# Prepare table rows  #
# # # # # # # # # # # #
# Prepare table row data on the fly
with open('xgt.tex', 'w') as f:
	for genus in range(1,8):
		tblrow = "{{\\mo{{{}}} ({})}} & {:.2f} & {:.2f} & {:.2f} \\\\".format(
			genusdict[genus],
			len(gd[genus]),
			round(np.percentile(gd[genus], 25), 2),
			round(np.median(gd[genus]), 2),
			round(np.percentile(gd[genus], 75), 2))
		print >> f, tblrow
