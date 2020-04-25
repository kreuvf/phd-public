# -*- coding: utf-8 -*-
import csv
from collections import OrderedDict

import re
import copy
import numpy as np

# # # # # # # # # # # # # # # # # # # # 
# Setup and Definitions
#
# dictaddinv: Invert key value pairs and add to dictionary
# Source: http://code.activestate.com/recipes/252143-invert-a-dictionary-one-liner/#c6
def dictaddinv(d):
	assert len(d) == len(dict([v,k] for k,v in d.iteritems())), 'Duplicate value in dictionary.'
	d.update(dict([v,k] for k,v in d.iteritems()))

# mam_dat[materials file][table rows]
# mam_abb[materials file][abbreviations]
#
# materials file:
#	0..8 =
#		chemicals, enzymes, nucleotides, sequences,
#		microorganisms, consumables, equipment,
#		glassware, software
# table rows: list of strings with LaTeX-ready table rows
#
# mam_dat = materials and methods data
# mam_abb = materials and methods abbreviations
mam_dat = [[] for category in range(9)]
mam_abb = [[] for category in range(9)]

# Define categories for automated conversion of materials file to index and back
category = dict()
category['chemicals'] = 0
category['enzymes'] = 1
category['nucleotides'] = 2
category['sequences'] = 3
category['microorganisms'] = 4
category['consumables'] = 5
category['equipment'] = 6
category['glassware'] = 7
category['software'] = 8
# Add reverse entries as well
dictaddinv(category)

# Generate list of input files
filelist = [
	'chemicals.txt', 'enzymes.txt', 'nucleotides.txt',
	'sequences.txt', 'microorganisms.txt', 'consumables.txt',
	'equipment.txt', 'glassware.txt', 'software.txt'
]

# actfiles = active files; to iterate over the existing files only
actfiles = [0, 1, 2, 3, 5, 6, 8]

# abbrfiles = abbreviate files; to iterate over files in need of abbr. only
abbrfiles = [0, 1, 2, 5, 6, 8]

# Generate abbreviation dictionaries for vendor shorthand notation
vendor = dict()
vendor['?'] = 'UNK'
vendor['A. Hartenstein GmbH, Würzburg'] = 'AHW'
vendor['Agilent Technologies, Waldbronn'] = 'AT'
vendor['Alfa Aesar GmbH + Co. KG, Karlsruhe'] = 'AAG'
vendor['Analytik Jena AG, Jena'] = 'AJA'
vendor['Andreas Hettich GmbH \& Co. KG, Tuttlingen'] = 'AHT'
vendor['Anton Paar GmbH, Graz, Austria'] = 'APG'
vendor['AppliChem GmbH, Darmstadt'] = 'ACG'
vendor['Avantor Performance Materials B.V., Deventer, Netherlands'] = 'APM'
vendor['B. Braun Melsungen AG, Melsungen'] = 'BBM'
vendor['Beckman Coulter GmbH, Krefeld'] = 'BCG'
vendor['BINDER GmbH, Tuttlingen'] = 'BG'
vendor['BRAND GmbH + Co. KG, Wertheim'] = 'BGK'
vendor['Bio-Rad Laboratories GmbH, Munich'] = 'BRL'
vendor['BlueSens gas sensor GmbH, Herten'] = 'BGS'
vendor['Boekel Scientific, Feasterville, PA, USA'] = 'BS'
vendor['Brookhaven Instruments Corporation, Holtsville, NY, USA'] = 'BIC'
vendor['Bruker Daltonik GmbH, Bremen'] = 'BDG'
vendor['Cargill France SAS, Saint-Germain-en-Lage, France'] = 'CFS'
vendor['Carl Roth GmbH + Co. KG, Karlsruhe'] = 'CRG'
vendor['Carl Zeiss Microscopy GmbH, Jena'] = 'CZM'
vendor['DASGIP GmbH, Jülich'] = 'DG'
vendor['Denver Instrument, Bohemia, NY, USA'] = 'DI'
vendor['Deutsche METROHM GmbH \& Co. KG, Filderstadt'] = 'DMG'
vendor['Dionex Corporation, Sunnyvale, CA, USA'] = 'DC'
vendor['Dispomed Witt oHG, Gelnhausen'] = 'DWO'
vendor['Dr. Klaus Schopp Forschung + Technik, Karlsruhe'] = 'KSF'
vendor['ELGA Lab Water, Celle'] = 'ELW'
vendor['EMD Biosciences, Inc., La Jolla, CA, USA'] = 'EMD'
vendor['Edmund Bühler GmbH, Hechingen'] = 'EBG'
vendor['Eppendorf AG, Hamburg'] = 'EA'
vendor['GE Healthcare Europe GmbH, Freiburg'] = 'GHE'
vendor['GE Healthcare UK Ltd., Buckinghamshire, United Kingdom'] = 'GHU'
vendor['GFL Gesellschaft für Labortechnik mbH, Burgwedel'] = 'GFL'
vendor['Greiner Bio-One GmbH, Frickenhausen'] = 'GBO'
vendor['HP Medizintechnik GmbH, Oberschleißheim'] = 'HPM'
vendor['Hamilton Bonaduz AG, Bonaduz, Switzerland'] = 'HBA'
vendor['Harvard Apparatus, Holliston, MA, USA'] = 'HA'
vendor['Heidolph Instruments GmbH \& Co. KG, Schwabach'] = 'HIG'
vendor['Hellma GmbH \& Co. KG, Müllheim'] = 'HG'
vendor['Henke-Sass, Wolf GmbH, Tuttlingen'] = 'HSW'
vendor['ifm electronic, Essen'] = 'IFM'
vendor['IKA-Werke GmbH \& Co. KG, Staufen'] = 'IKA'
vendor['Implen GmbH, München'] = 'IG'
vendor['Infors AG, Bottmingen/Basel, Switzerland'] = 'IA'
vendor['Ingenieurbüro CAT, M. Zipperer GmbH, Staufen'] = 'ICZ'
vendor['Intas-Science-Imaging Instruments GmbH, Göttingen'] = 'IIG'
vendor['Jungbunzlauer Suisse AG, Basel, Switzerland'] = 'JSA'
vendor['KERN \& SOHN GmbH, Balingen'] = 'KSG'
vendor['Liebherr Hausgeräte, Ochsenhausen'] = 'LH'
vendor['Macherey-Nagel GmbH \& Co. KG, Düren'] = 'MNG'
vendor['Mallinckrodt Baker B. V., Deventer, Netherlands'] = 'MBB'
vendor['Martin Christ Gefriertrocknungsanlagen GmbH, Osterode am Harz'] = 'MCG'
vendor['Memmert GmbH + Co. KG, Schwabach'] = 'MG'
vendor['Merck KGaA, Darmstadt'] = 'MK'
vendor['Merck Schuchardt OHG, Hohenbrunn'] = 'MSO'
vendor['Mettler-Toledo GmbH, Gießen'] = 'MTG'
vendor['Motic Deutschland GmbH, Wetzlar'] = 'MDG'
vendor['New England Biolabs GmbH, Frankfurt am Main'] = 'NEB'
vendor['Ohaus Corp., Pine Brook, NJ, USA'] = 'OC'
vendor['PSS Polymer Standards Service GmbH, Mainz'] = 'PSS'
vendor['Pall Corporation, Ann Arbor, MI, USA'] = 'PC'
vendor['Peter Huber Kältemaschinenbau GmbH, Offenburg'] = 'PHK'
vendor['Phenomenex Ltd., Aschaffenburg'] = 'PL'
vendor['QIAGEN GmbH Deutschland, Hilden'] = 'QGD'
vendor['Rapidozym Gesellschaft für Laborhandel und DNA Diagnostika mbH, Berlin'] = 'RLD'
vendor['Restek Corporation, Bellefonte, PA, USA'] = 'RC'
vendor['SI Analytics GmbH, Mainz'] = 'SIA'
vendor['Sarstedt AG \& Co. KG, Nümbrecht'] = 'SAK'
vendor['Sartorius AG, Göttingen'] = 'SAG'
vendor['Sartorius Lab Instruments GmbH \& Co. KG, Göttingen'] = 'SLI'
vendor['Sartorius Stedim Biotech GmbH, Göttingen'] = 'SSB'
vendor['Sartorius Stedim Systems, Göttingen'] = 'SSS'
vendor['SensoQuest Biomedizinische Elektronik GmbH, Göttingen'] = 'SBE'
vendor['Serva Electrophoresis GmbH, Heidelberg'] = 'SEG'
vendor['Shimadzu, Kyoto, Japan'] = 'SKK'
vendor['Showa Denko K.K., Kawasaki, Japan'] = 'SDK'
vendor['Sigma-Aldrich Chemie GmbH, Steinheim'] = 'SAC'
vendor['Spencer Kimball, Peter Mattis and the GIMP Development Team'] = 'KMG'
vendor['Thermo Electron LED GmbH, Langenselbold'] = 'TEL'
vendor['Thermo Fisher Scientific Inc., Waltham, MA, USA'] = 'TFS'
vendor['Tosoh Bioscience GmbH, Stuttgart'] = 'TBG'
vendor['VACUUBRAND GmbH + Co. KG, Wertheim'] = 'VAG'
vendor['VWR International bvba/sprl, Leuven, Belgium'] = 'VWR'
vendor['ZMK-Analytik-GmbH, Bitterfeld-Wolfen'] = 'ZAG'
vendor['Zefa-Laborservice GmbH, Harthausen'] = 'ZLG'
# Add reverse entries as well
dictaddinv(vendor)

# # # # # # # # # # # # # # # # # # # # 
# File Input
#
# Read files and save to temp list
mam_in = [ [""] for i in range(9)]
for material in range(9):
	with open(filelist[material], 'r') as results:
		reader = csv.reader(results, delimiter="\t")
		mam_in[material] = list(reader)

# # # # # # # # # # # # # # # # # # # # 
# Data Processing
# 
# Remove empty entries at the end
for material in actfiles:
	# Empty lists evaluate to false
	while not(mam_in[material][-1]):
		del mam_in[material][-1]

# Remove entries unused in the final version of the thesis
for material in actfiles:
	# Reversed since we are deleting and doing that from the back end will not affect the indices of items with lower index
	for entry in reversed(range(len(mam_in[material]))):
		if(mam_in[material][entry][-1] == 'n'):
			del mam_in[material][entry]

# Remove unnecessary columns (transpose, remove line, re-transpose)
for material in actfiles:
	mam_in[material] = np.array(mam_in[material]).T.tolist()

# All
for material in actfiles:
	del mam_in[material][-1] # Yes/no column which was already used

# Chemicals
# cc = current category
cc = category['chemicals']
del mam_in[cc][9] # comments
del mam_in[cc][8] # CBR ID
del mam_in[cc][7] # date of first use
del mam_in[cc][6] # CAS
del mam_in[cc][5] # lot
del mam_in[cc][4] # art. no.
del mam_in[cc][0] # sort key

# Enzymes
cc = category['enzymes']
del mam_in[cc][4] # comments
del mam_in[cc][3] # lot

# Nucleotides
cc = category['nucleotides']
del mam_in[cc][5] # comments
del mam_in[cc][4] # lot
del mam_in[cc][0] # sort key

# Sequences
cc = category['sequences']
del mam_in[cc][0] # sort key

# Consumables
cc = category['consumables']
del mam_in[cc][5] # comments
del mam_in[cc][4] # lot

# Equipment
cc = category['equipment']
del mam_in[cc][4] # comments
del mam_in[cc][3] # s/n

# Software
cc = category['software']
del mam_in[cc][4] # comments

# Abbreviate manufacturers/vendors
# Column 1 in enzymes, nucleotides
# Column 2 in chemicals, consumables, equipment
# Column 3 in software
for material in [category['enzymes'], category['nucleotides']]:
	for item in range(1, len(mam_in[material][1])):
		mam_in[material][1][item] = vendor[mam_in[material][1][item]]
for material in [category['chemicals'], category['consumables'], category['equipment']]:
	for item in range(1, len(mam_in[material][2])):
		mam_in[material][2][item] = vendor[mam_in[material][2][item]]
for item in range(1, len(mam_in[category['software']][3])):
	mam_in[category['software']][3][item] = vendor[mam_in[category['software']][3][item]]

# Re-transpose
for material in actfiles:
	mam_in[material] = np.array(mam_in[material]).T.tolist()
# # # # # # # # # # # # # # # # # # # # 
# Table Row Preparation
# 
# Write rows for LaTeX tables to mam_dat
# 
# 	chemicals: Chemical, Grade, Manufacturer or vendor
# 	enzymes: Enzyme, Manufacturer, Article number
# 	nucleotides: Nucleotide, Manufacturer, Article number
# 	sequences: Name, Sequence
# 	microorganisms: to be done
# 	consumables: Type, Name, Manufacturer or vendor, Article number
# 	equipment: Type, Model, Manufacturer or vendor
# 	glassware: to be done
# 	software: Category, Name, Version, Manufacturer or vendor
#
# --> Default treatment: use three columns
# --> sequences, consumables, software: special cases
# --> microorganisms, glassware are NOOPs

# Create tables
for material in range(9):
	if material in actfiles:
		if(material == category['consumables']):
			for line in range(1, len(mam_in[material])):
				tblline = '\t{{{}}} & {{{}}} & {{{}}} & {{{}}} \\\\'.format(
					mam_in[material][line][0], 
					mam_in[material][line][1], 
					mam_in[material][line][3], 
					mam_in[material][line][2])
				mam_dat[material].append(tblline)
		elif(material == category['software']):
			for line in range(1, len(mam_in[material])):
				tblline = '\t{{{}}} & {{{} {}}} & {{{}}} \\\\'.format(
					mam_in[material][line][0], 
					mam_in[material][line][1], 
					mam_in[material][line][2], 
					mam_in[material][line][3])
				mam_dat[material].append(tblline)
		elif(material == category['sequences']):
			for line in range(1, len(mam_in[material])):
				tblline = '\t{{{}}} & {{{}}} \\\\'.format(
					mam_in[material][line][0],
					mam_in[material][line][1])
				mam_dat[material].append(tblline)
		elif(material == category['equipment'] or
			material == category['chemicals']):
			for line in range(1, len(mam_in[material])):
				tblline = '\t{{{}}} & {{{}}} & {{{}}} \\\\'.format(
					mam_in[material][line][0], 
					mam_in[material][line][1], 
					mam_in[material][line][2])
				mam_dat[material].append(tblline)
		else:
			for line in range(1, len(mam_in[material])):
				tblline = '\t{{{}}} & {{{}}} & {{{}}} \\\\'.format(
					mam_in[material][line][0], 
					mam_in[material][line][2], 
					mam_in[material][line][1])
				mam_dat[material].append(tblline)
		# Wipe out double entries (stemming from different lots, art. no.)
		uniqdat = list(OrderedDict.fromkeys(mam_dat[material]))
		mam_dat[material] = uniqdat
	else:
		mam_dat[material].append('Not yet implemented.')
		print('material is {} which corresponds to {} which is still empty.'.format(material, category[material]))

# Create abbreviation lists
# Column 1 in enzymes, nucleotides
# Column 2 in chemicals, consumables, equipment
# Column 3 in software
for material in [category['enzymes'], category['nucleotides']]:
	for item in range(1, len(mam_in[material])):
		mam_abb[material].append(mam_in[material][item][1])
	uniqdat = list(OrderedDict.fromkeys(mam_abb[material]))
	mam_abb[material] = sorted(uniqdat)
for material in [category['chemicals'], category['consumables'], category['equipment']]:
	for item in range(1, len(mam_in[material])):
		mam_abb[material].append(mam_in[material][item][2])
	uniqdat = list(OrderedDict.fromkeys(mam_abb[material]))
	mam_abb[material] = sorted(uniqdat)
for item in range(1, len(mam_in[category['software']])):
	mam_abb[category['software']].append(mam_in[category['software']][item][3])
uniqdat = list(OrderedDict.fromkeys(mam_abb[category['software']]))
mam_abb[category['software']] = sorted(uniqdat)

# Create abbreviation texts (per category and overall)
allabb = []
for material in abbrfiles:
	for abb in range(len(mam_abb[material])):
		# abbentry = abbreviation entry
		abbentry = "\t{} & {} \\\\".format(mam_abb[material][abb], vendor[mam_abb[material][abb]])
		mam_abb[material][abb] = abbentry
		allabb.append(abbentry)
# Sort
allabb = sorted(allabb)
# Uniq
allabb = list(OrderedDict.fromkeys(allabb))

# # # # # # # # # # # # # # # # # # # # 
# Output Files
# 
# Write to files
for material in range(9):
	with open('{}.tex'.format(category[material]), "w") as f:
		for line in mam_dat[material]:
			print >> f, line

# Output abbreviations
with open('matabbr.tex', "w") as f:
	for abbr in range(len(allabb)):
		print >> f, allabb[abbr]

