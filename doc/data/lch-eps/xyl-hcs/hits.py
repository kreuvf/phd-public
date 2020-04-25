import sys
import csv
import numpy as np

with open(sys.argv[1], 'r') as results:
	reader = csv.reader(results, delimiter="\t")
	xyl_hcs_hits = list(reader)

# Remove empty last element
del xyl_hcs_hits[-1]

for row in range(1,11):
	if row != 10:
		for col in range(1,14):
			# Rounding to remove numeric imprecision
			xyl_hcs_hits[row][col] = round(float(xyl_hcs_hits[row][col]) * 5.6, 0)
	else:
		for col in range(1,14):
			# Recalculate sums without xylose (row '9')
			xyl_hcs_hits[row][col] = 0.0
			for sumrow in range(1,9):
				xyl_hcs_hits[row][col] += xyl_hcs_hits[sumrow][col]

# Remove lines with only 'n'
delrows = [9] # line for xylose
for row in range(11,19):
	coln = 0
	for col in range(1,len(xyl_hcs_hits[row])):
		if xyl_hcs_hits[row][col] == 'n':
			coln = coln + 1
	if coln == len(xyl_hcs_hits[row]) - 1:
		delrows.append(row)

for row in range(len(delrows)):
	del xyl_hcs_hits[delrows[-1]]
	del delrows[-1]

# Transpose table
xhh = np.array(xyl_hcs_hits).T.tolist()

with open('hits_processed.txt', 'wb') as outfile:
	resultswriter = csv.writer(outfile, delimiter="\t",)
	for row in range(len(xhh)):
		resultswriter.writerow(xhh[row])
