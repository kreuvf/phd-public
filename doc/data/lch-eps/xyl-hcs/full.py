import csv
import re
import numpy as np

# Input table layout:
#	 0	Strain 	Man  	Nig  	GlcUA 	Lam    	 4
#	 5	GlcN   	GalUA	Rib  	Rha   	Ism    	 9
#	10	Gen    	Koj  	GalN 	GlcNAc	Mal    	14
#	15	Lac    	Cel  	Sop  	Glc   	GalNAc 	19
#	20	Gal    	Ara  	Xyl  	Fuc   	2-d-Glc	24
#	25	2-d-Rib	Sum  	Sum w/o Xyl   	27
# xhf = xyl-hcs-full
with open('full.txt', 'r') as f:
	reader = csv.reader(f, delimiter = '\t')
	xhf = list(reader)

# xht = xyl-hcs-table
xht = []

# Read in raw values in new order
# New order (sum will be recalculated later on):
#	 0	Strain	Fuc    	Gal  	GalN 	GalUA	 4
#	 5	Gen   	2-d-Glc	Glc  	GlcN 	GlcUA	 9
#	10	Man   	Rha    	Rib  	(Sum)	Xyl  	14
#	15	Ism   	Lam    	Nig  	Sop  	17
for i in xhf[1:-1]:
	# Since I never found Ara, there are only 'n's
	# Xyl value is defined to include Ara as well
	xht.append([
	i[0],
	float(i[23]), float(i[20]), float(i[12]), float(i[6]), float(i[10]),
	float(i[24]), float(i[18]), float(i[5]),
	float(i[3]), float(i[1]), float(i[8]), float(i[7]), -1.0,
	float(i[22]), i[9], i[4], i[2], i[17]
	])

# Convert 'j' to 'y'
#
# Multiply raw values by dilution factor 5.6
# Round everything
#
# Calculate sums
for i in range(len(xht)):
	for j in range(15, 19):
		if xht[i][j] == "j":
			xht[i][j] = "y"

	for j in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14]:
		xht[i][j] = int(round(5.6 * xht[i][j], 0))

	xht[i][13] = 0
	for j in range(1, 13):
		xht[i][13] = xht[i][13] + xht[i][j]

# Output summary statistics and classes of the sum column
# Get all sums
sums = []
# belowt = below threshold
# abovet = above threshold (or equal)
belowt = 0
below100 = 0
abovet = 0
for i in range(len(xht)):
	sums.append(xht[i][13])
	if(xht[i][13] < 100.0):
		below100 = below100 + 1
	if(xht[i][13] < 560.0):
		belowt = belowt + 1
	else:
		abovet = abovet + 1

print("Strains: {}, {} below threshold, {} above or equal threshold (560 mg/l); {} below 100 mg/l".format(abovet+belowt, belowt, abovet, below100))
print("Distribution: 25th percentile: {}, median: {}, 75th percentile: {}".format(np.percentile(sums, 25), np.median(sums), np.percentile(sums, 75)))

# Remove 'Xyl1.' at the start of every strain
# It's one plate only and it's always 'Xyl1.'
for i in range(len(xht)):
	xht[i][0] = re.findall('^Xyl1\.([A-H][0-9]{1,2})', xht[i][0])[0]

# Write table
# Table definition:
# {Strain}
#			 & {Fuc} & {Gal} & {GalN} & {GalUA} & {Gen}
#			 & {2-\textsc{d}-Glc} & {Glc} & {GlcN} 
#			 & {GlcUA} & {Man} & {Rha} & {Rib} & {Sum}
#			 & {Xyl/Ara} & {Ism} & {Lam} & {Nig} & {Sop} \\
#
with open('full.tex', 'w') as f:
	# no header line needed
	for i in range(len(xht)):
		tblline = """			{{\\xyli{{{}}}}}
			 & {{{}}} & {{{}}} & {{{}}} & {{{}}} & {{{}}}
			 & {{{}}} & {{{}}} & {{{}}} 
			 & {{{}}} & {{{}}} & {{{}}} & {{{}}} & {{{}}}
			 & {{{}}} & {{{}}} & {{{}}} & {{{}}} & {{{}}} \\\\""".format(
		xht[i][0], 
		xht[i][1], xht[i][2], xht[i][3], xht[i][4], xht[i][5], 
		xht[i][6], xht[i][7], xht[i][8],
		xht[i][9], xht[i][10], xht[i][11], xht[i][12], xht[i][13], 
		xht[i][14], xht[i][15], xht[i][16], xht[i][17], xht[i][18])
		print >> f, tblline
