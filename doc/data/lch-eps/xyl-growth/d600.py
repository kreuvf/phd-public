import openpyxl
import numpy as np

xlsx = openpyxl.load_workbook('d600.xlsx', data_only=True)
data_sheet = xlsx.get_sheet_by_name('loPep_data')

# Select ranges, D600 - reference
eps1_array = list(data_sheet['B4':'M11'])
eps2_array = list(data_sheet['P4':'AA11'])

eps1_wells = 0
eps2_wells = 0

# Calculate amount of input wells
for letter in range(8):
    eps1_wells = eps1_wells + len(eps1_array[letter])
    eps2_wells = eps2_wells + len(eps2_array[letter])

eps1_wells = eps1_wells - 1  # one well (EPS1.D12) was empty

# Get values, from well A1 to H12
# From left to right, from top to bottom
xyl_growth_vals = []

# Pick grown cultures (ok) only
# D600 < 0.01:         no growth
# 0.01 =< D600 < 0.2: low growth
# 0.2 =< D600:         ok growth

for letter in range(8):
    for number in range(12):
        if eps1_array[letter][number].value >= 0.2:
            xyl_growth_vals.append(eps1_array[letter][number].value)

        if eps2_array[letter][number].value >= 0.2:
            xyl_growth_vals.append(eps2_array[letter][number].value)

# Save to variables for later retrieval
xyl_growth_inputno = eps1_wells + eps2_wells
xyl_growth_goodgrowth = len(xyl_growth_vals)
xyl_growth_d600med = round(np.median(xyl_growth_vals),2)
xyl_growth_d600max = round(np.amax(xyl_growth_vals),2)
