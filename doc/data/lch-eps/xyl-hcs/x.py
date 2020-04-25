import openpyxl
import numpy as np

xlsx = openpyxl.load_workbook('summary.xlsx', data_only=True)
data_sheet = xlsx.get_sheet_by_name('Tabelle1')

# Select ranges, xylose concentration (diluted value)
xyl1_array = list(data_sheet['B7':'M14'])

# Dilution factor: 50
difa = 50

# Calculate amount of input wells
xyl1_wells = 0
for letter in range(8):
    xyl1_wells = xyl1_wells + len(xyl1_array[letter])

xyl1_wells = xyl1_wells - 1 # one well (Xyl1.E12) was empty

# Get values, from well A1 to H12
# From left to right, from top to bottom
# xc = xylose consumption
xyl_hcs_xc = [[], [], [], [], []]

# Growth categorization (from Excel file)
# bad:       >= 167
# mediocre:  >= 100 and < 167
# good:      >=  30 and < 100
# very good: >=   0 and <  30


for letter in range(8):
    for number in range(12):
        if (not(letter == 4 and number == 11)):
            current_value = float(xyl1_array[letter][number].value)
            xyl_hcs_xc[0].append(round(current_value * difa,1))
            if current_value >= 167.0:
                xyl_hcs_xc[1].append(round(current_value * difa,1))
            elif current_value >= 100.0:
                xyl_hcs_xc[2].append(round(current_value * difa,1))
            elif current_value >= 30.0:
                xyl_hcs_xc[3].append(round(current_value * difa,1))
            elif current_value >= 0.0:
                xyl_hcs_xc[4].append(round(current_value * difa,1))
            else:
                print('What did you do there? current_value is: ' + str(current_value))

# Save to variables for later retrieval
# mab: mediocre and better
xyl_hcs_mab = str(
    len(xyl_hcs_xc[2]) +
    len(xyl_hcs_xc[3]) +
    len(xyl_hcs_xc[4])
)
# gab: good and better
xyl_hcs_gab = str(
    len(xyl_hcs_xc[3]) +
    len(xyl_hcs_xc[4])
)
# veg: very good
xyl_hcs_veg = str(
    len(xyl_hcs_xc[4])
)
xyl_hcs_xmed = '\SImgpl{' + str(int(round(np.median(xyl_hcs_xc[0]), 0))) + '}'
xyl_hcs_xlquart = '\SImgpl{' + str(int(round(np.percentile(xyl_hcs_xc[0], 25), 0))) + '}'
xyl_hcs_xhquart = '\SImgpl{' + str(int(round(np.percentile(xyl_hcs_xc[0], 75), 0))) + '}'

# # # # # # # # # # # #
# Prepare table rows  #
# # # # # # # # # # # #
# Make nested list with values from xyl1_array
# xv = xylose1 array values
# xylhcs_xt = xyl-hcs xylose consumption table rows
# Un-dilute values
# dilution factor: 50
xv = [ [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ] for x in range(8) ]
for letter in range(8):
	for number in range(12):
		# Undilute = factor 50
		# Conversion to g/l from mg/l = factor 0.001
		xv[letter][number] = "{:.2f}".format(round(xyl1_array[letter][number].value * 50 * 0.001, 2))

wellx = dict()
wellx[0] = 'A'; wellx[1] = 'B'
wellx[2] = 'C'; wellx[3] = 'D'
wellx[4] = 'E'; wellx[5] = 'F'
wellx[6] = 'G'; wellx[7] = 'H'

# Prepare table rows
xylhcs_xt = []

with open('xt.tex', 'w') as f:
	for letter in range(8):
		tblrow = "{{{}}} & {} & {} & {} & {} & {} & {} & {} & {} & {} & {} & {} & {} \\\\".format(wellx[letter], xv[letter][0], xv[letter][1], xv[letter][2], xv[letter][3], xv[letter][4], xv[letter][5], xv[letter][6], xv[letter][7], xv[letter][8], xv[letter][9], xv[letter][10], xv[letter][11])
		print >> f, tblrow
