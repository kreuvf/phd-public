# # # # # # # # # # # # # # # # # # # # 
# Generate graphs of LCHF0
# LCH-PF, two figures, each with four y-axes
# # # # # # # # # # # # # # # # # # # # 
library(splitstackshape) # cSplit
library(lubridate) # as.duration
library(plyr) # round_any, join
library(zoo) # rollapply
library(readxl) # read_excel


# # # # # # # # # # # # # # # # # # # # 
# Data structure and type definitions
# Conversion of sample number to sampling time in seconds
# blk1smptim = block sample times
blk1smptim <- read.table(text = 
"sample.block.1	t
0	3600
1	50400
2	90600
3	135000
4	172800
5	223800
6	259800
7	316800
8	329400", # D600 only sample at the end of the process
header = TRUE, colClasses = c("numeric", "numeric"))
blk1smptim$t <- as.duration(blk1smptim$t)

blk2smptim <- read.table(text = 
"sample.block.2	t
0	3600
1	50400
2	90600
3	135000
4	172800
5	223800
6	259800
7	316800
8	346800
9	403200
10	432000
11	482400",
header = TRUE, colClasses = c("numeric", "numeric"))
blk2smptim$t <- as.duration(blk2smptim$t)

# Dilution factors
# lchfa1df = LCHFA1 dilution factor
lchfa1df <- 5.05 # 61 µl for neutralization
# lchfa223df = LCHFA2_2 and LCHFA2_3 dilution factor
lchfa223df <- 400

# # # # # # # # # # # # # # # # # # # # 
# Function definitions
# Function for reading in fermentation data
getFermDat <- function(df, file){
	# Read in data
	df <- as.data.frame(
		cSplit(
			read.table(file, header = TRUE,
				# Names for description of the expected content only
				col.names = c("Date and time", 
					"Time after inoculation in hh:mm:ss", "pH value", 
					"DO in %", "CO2 in A.U."),
				colClasses = c("NULL", "character", "numeric", "numeric", 
					"numeric"),
				sep = "\t", dec = '.'),
			splitCols = "Time.after.inoculation.in.hh.mm.ss", sep =":", 
			drop = TRUE))
	# Give temporary names
	colnames(df) <- c("pH value", "DO in %", "CO2 in A.U.", "HH", "MM", "SS")
	return(df)
	}

# Function for preparing fermentation data
prepFermDat <- function(df, shorthand){
	# Remove unnecessary pH column
	df <- df[ , c(2, 3, 4, 5, 6)]
	# Reduce time to duration in seconds and
	# round down to 30 s to have matching times when joining columns
	# Rounding down due to F2 data which has seconds of
	# 14, 44, 14, 45, 15, 44, 15, 45 ... giving ~25% of duplicate values
	df$SS <- round_any(
		as.duration(
			df$SS + (df$MM * 60) + (df$HH * 3600))
		, 30, floor)
	# Remove now unnecessary hours and minutes columns, reorder columns
	df <- df[ , c(5, 1, 2)]
	# Name columns sensibly
	# Explanations:
	#	[[1]]	t: process time in s
	# 	[[2]]	DO: dissolved oxygen in percent of max. calibrated at process start
	# 	[[3]]	CO2: CO2 in off-gas in percent
	colnames(df) <- c("t", paste('DO', shorthand, sep='.'), 
		paste('CO2', shorthand, sep='.'))
	# Rolling average over 50 of DO values, last 50 values take median
	df[[2]] <- rollapply(
		df[[2]], 50, mean, fill=c(mean(head(df[[2]], 50)), 
		NA, median(tail(df[[2]], 50))))
	return(df)
	}


# # # # # # # # # # # # # # # # # # # # 
# Input fermentation/on-line data
# 	Data of 8 fermenters: time, pH, DO, CO2

# Vector with filenames
infiles <- c('f1.txt', 'f2.txt', 'f3.txt', 'f4.txt', 
	'f5.txt', 'f6.txt', 'f7.txt', 'f8.txt')
# String with relative path to files
directory <- 'ferm-dat/'
# Create 'indon' as empty list; indon = in data, online
indon <- list()

# Loop for the actual input
for (i in 1:8) {
	indon[[i]] <- getFermDat(indon[[i]], paste(directory, infiles[[i]], sep = ''))
}


# # # # # # # # # # # # # # # # # # # # 
# Input off-line sample data
#	Data of 8 fermenters: time, D600, CDM, Glucose concentration (glucose
# 	assay), Molar mass at RI peak, Furfural (found in block 2, only; data for
# 	all 8 available)
#	Not considered: EPS concentration (at the end, from precipitation), Xylose
#	concentration (PMP, too unreliable), EPS concentration and monomer
# 	compositions (PMP, too unreliable)

# Input D600
d600 <- as.data.frame(
	cSplit(
		read.table('ferm-dat/d600.txt', header = TRUE, sep = "\t", dec = ",",
			col.names = c("Time after inoculation in hh:mm", "D600.F1", "D600.F2", "D600.F3", "D600.F4", "D600.F5", "D600.F6", "D600.F7", "D600.F8"),
			na.strings = "-",
			colClasses = c("character", rep("numeric", 8)), nrows = 13),
		splitCols = "Time.after.inoculation.in.hh.mm", sep = ":", drop = FALSE))
colnames(d600) <- c("t", "D600.F1", "D600.F2", "D600.F3", "D600.F4", "D600.F5", "D600.F6", "D600.F7", "D600.F8", "HH", "MM")

# Input CDM
cdm <- read_excel("lchf0-cdm.xlsx", sheet = "BTM", col_names = TRUE, skip = 1)

# Input glucose assay data (LCHFA2); skip rows with visually appealing header
lchfa2 <- as.data.frame(
	read_excel("glc-results.xlsx", sheet = "conc",
		col_names = c("junk", "UID", "A.418.-A.480.", "Glc.conc."),
		col_types = c("text", "text", "text", "numeric"),
		skip = 4))

# Input EPS monomer data; skip rows with type, unit, analyte, signal
epsamc <- as.data.frame(
	read_excel("eps-amc.xlsx", sheet = "PMP",
		col_names = TRUE,
		col_types = c("text", "text", rep("numeric", 21)),
		na = "n.a.", skip = 4))

# Input molar mass at RI peak data
mp <- as.data.frame(
	read_excel("sec-malls-results.xlsx", sheet = "Tabelle1",
		col_names = c("Sample.ID", "Peak elution time", "Mn in g/mol", "Mw in g/mol", "Mp in g/mol", "Injection datetime"),
		col_types = c("text", rep("numeric", 4), "text"),
		na = "-", skip = 1))

# Input furfural data
fur <- as.data.frame(
	read_excel("glc-xyl-fur-hplc.xlsx", sheet = "PMP",
		col_names = c("junk", "UID", "FermGlc.PMP", "FermXyl.PMP", "HMF", "Fur"),
		col_types = c("text", "text", rep("numeric", 4)),
		na = "n.a.", skip = 4))

# # # # # # # # # # # # # # # # # # # # 
# Process data
# 	Transform time into seconds and round to nearest 30 for comparison, get
# 	rid of unneeded columns, name columns according to their origin
for (i in 1:8) {
	indon[[i]] <- prepFermDat(indon[[i]], paste('F', i, sep = ''))
}

# Transform D600 data
# 	Time data to duration in seconds
# 	Remove no longer necessary columns
d600$t <- as.duration((d600$MM * 60) + (d600$HH * 3600))
d600 <- d600[, 1:9]
# Split into block 1 and 2
blk1d600 <- d600[ , 1:5]
blk2d600 <- d600[ , c(1, 6:9)]
# Remove NAs
blk1d600 <- blk1d600[complete.cases(blk1d600),]
blk2d600 <- blk2d600[complete.cases(blk2d600),]
# Remove last block 1 sample
# it's unnecessary, because there is no other data to correlate it with
blk1d600 <- blk1d600[1:(nrow(blk1d600)-1),]

# Transform CDM data
# 	Columns fermenter, sample, concentration stay; others will be removed
cdm <- cdm[, c(1, 2, 8)]
colnames(cdm) <- c("Fermenter", "Sample", "CDM")
# Remove NA-only rows
cdm <- cdm[rowSums(is.na(cdm)) != ncol(cdm),]
# Reshape format to Sample, Fermenter n ...
cdm <- as.data.frame(reshape(cdm, idvar = "Sample", timevar = "Fermenter", direction = "wide"))
# Replace "Sample" column with sample times
# blk2smptim used, because 8th blk1 sample is D600 only
# +1, because R starts indexing content at 1
cdm[,1] <- blk2smptim[(cdm[,1]+1),2]
# Adapt column names
colnames(cdm) <- c("t", "CDM.F1", "CDM.F2", "CDM.F3", "CDM.F4", "CDM.F5", "CDM.F6", "CDM.F7", "CDM.F8")
# Split into block 1 and 2
blk1cdm <- cdm[ , 1:5]
blk2cdm <- cdm[ , c(1, 6:9)]
# Remove NAs
blk1cdm <- blk1cdm[complete.cases(blk1cdm),]
blk2cdm <- blk2cdm[complete.cases(blk2cdm),]

# Transform glucose assay data
# Remove column 'junk' and absorption differences
lchfa2 <- lchfa2[ , c(2, 4)]
# Split into two parts:
# 	PMP glucose (LCHFA2_0 + LCHFA2_1)
# 	glucose in fermenter (LCHFA2_2 + LCHFA2_3)
pmpglc <- lchfa2[1:152, ]
fermglc <- lchfa2[153:nrow(lchfa2), ]

# Transform PMP glucose data
# Keep rows from before hydrolysis only, renumber rows
pmpglc <- pmpglc[c(1:68),]
rownames(pmpglc) <- NULL
# Reverse dilution (5 µl sample + 45 µl ddH2O)
pmpglc[, 2] <- 10 * pmpglc[, 2]
# Split UID: LCHFA2_0.B9_F1.0 --> LCHFA2	0.B9	F1	0
pmpglc <- as.data.frame(cSplit(pmpglc,
	splitCols = "UID", sep ="_", drop = TRUE, type.convert = FALSE))
pmpglc <- as.data.frame(cSplit(pmpglc,
	splitCols = "UID_3", sep =".", drop = TRUE, type.convert = FALSE))
# Throw away columns: experiment identifier, plate + coordinates
pmpglc <- pmpglc[ , c(1, 4, 5)]
colnames(pmpglc) <- c("PMPGlc", "Fermenter", "Sample")
# Auto-convert columns now
pmpglc[, 3] <- type.convert(pmpglc[, 3])
pmpglc[, 2] <- type.convert(pmpglc[, 2])
# Set negative values to zero
pmpglc[ ,1] <- with(pmpglc, ifelse(PMPGlc < 0, 0, PMPGlc))
# Reorder columns: Sample, Fermenter, Glc. conc.
pmpglc <- pmpglc[ , c(3, 2, 1)]
# Reshape content: columns for every fermenter
pmpglc <- as.data.frame(reshape(pmpglc, idvar = "Sample", timevar = "Fermenter", direction = "wide"))
# Renumber rows
rownames(pmpglc) <- NULL

# Transform Fermentation glucose data
# Renumber rows
rownames(fermglc) <- NULL
# Remove rows with standards and 10 l fermentation
fermglc <- fermglc[-c(9:10, 19:20, 29:30, 39:41, 50:52, 61:63, 72:73, 82:84, 180:212), ]
# Renumber rows
rownames(fermglc) <- NULL
# Fix wrong labelling in raw data: sample F7.2 in (E|F)2 is actually F7.1
fermglc[c(113, 125), 1] <- "LCHFA2_3.E2_F7.1"
# Split UID: LCHFA2_2.A1_F1.0 --> LCHFA2	2.A1	F1.0
fermglc <- as.data.frame(cSplit(fermglc,
	splitCols = "UID", sep ="_", drop = TRUE, type.convert = FALSE))
# Throw away columns: UID_1, UID_2
fermglc <- fermglc[ , c(1, 4)]
# Rename column
colnames(fermglc) <- c("FermGlc", "Fermenter.Sample")
# Create one column for every sample
# 	Max. two values per sample --> mark via duplicate
# 	reshape data to get two rows and lots of columns
fermglc['dpl'] <- as.numeric(duplicated(fermglc[ , c(2)]))
fermglc <- as.data.frame(reshape(fermglc, idvar = "dpl", timevar = "Fermenter.Sample", direction = "wide"))
# Add row with means ignoring NAs
fermglc <- rbind(fermglc, sapply(fermglc, mean, na.rm = 1))
# Remove unneeded rows
fermglc <- fermglc[3, ]
# Re-reshape into long format
fermglc <- as.data.frame(reshape(fermglc))
# Re-number rows
rownames(fermglc) <- NULL
# Drop now useless dpl column
fermglc <- fermglc[ , 2:3]
# Rename columns
colnames(fermglc)[2] <- "FermGlc"
# Split into fermenter and sample
fermglc <- as.data.frame(cSplit(fermglc,
	splitCols = "Fermenter.Sample", sep =".", drop = TRUE, type.convert = FALSE))
# Rename columns
colnames(fermglc)[2:3] <- c("Fermenter", "Sample")
# Auto-convert columns now
fermglc[, 3] <- type.convert(fermglc[, 3])
# FAINARU RISHEIPU (final reshape): Sample	FermGlc.F1	FermGlc.F2 ...
fermglc <- as.data.frame(reshape(fermglc, idvar = "Sample", timevar = "Fermenter", direction = "wide"))
# Re-number rows
rownames(fermglc) <- NULL
# Apply dilution factor
fermglc[, 2:ncol(fermglc)] <- lchfa223df*fermglc[, 2:ncol(fermglc)]
# Convert unit from mg/l to g/l
fermglc[, 2:ncol(fermglc)] <- 0.001*fermglc[, 2:ncol(fermglc)]
# Replace sample number with sample time
# blk2smptim used, because 8th blk1 sample is D600 only
# +1, because R starts indexing content at 1
fermglc[,1] <- blk2smptim[(fermglc[,1]+1),2]
# Rename sample column
colnames(fermglc)[1] <- "t"

# Transform EPS monomer data
# 	Use appropriate column names
#	Remove unused rows and colums
# 	Remove NA only columns
# 	Subtract glucose (from glucose assay)
colnames(epsamc) <- c(
	"Sample number", "Sample name", "Man", "GlcUA", "GlcN", "GalUA", 
	"Rib", "Rha", "Gen", "GalN", "GlcNAc", "Lac", 
	"Cel", "Glc", "GalNAc", "Gal", "Ara", "Xyl", 
	"Fuc", "2dGlc", "2dRib", "HMF", "Fur")
# Throw away junk rows start (standards)
epsamc <- epsamc[21:nrow(epsamc), ]
# Throw away junk rows at the end (standards at the end, 10 l fermentation)
epsamc <- epsamc[1:(nrow(epsamc)-17), ]
# Throw away junk cols (Ara, Xyl)
epsamc <- epsamc[, -(17:18)]
# Throw away junk cols (sample number, HMF, Fur)
epsamc <- epsamc[, 2:(ncol(epsamc)-2)]
# Set sample #10 of fermenter 8 GalUA value to "NA": no GalUA detected in MS!
epsamc[67,5] <- NA
# Remove all columns which contain only NA
epsamc <- Filter(function(x)!all(is.na(x)), epsamc)
# Split sample name column twice to get columns for fermenter and sample
epsamc <- as.data.frame(cSplit(epsamc,
	splitCols = "Sample name", sep ="_", drop = TRUE, type.convert = FALSE))
epsamc <- as.data.frame(cSplit(epsamc,
	splitCols = "Sample name_2", sep =".", drop = TRUE, type.convert = FALSE))
# Throw away column: plate + coordinates
epsamc <- epsamc[ , -6]
# Reorder columns: sample, fermenter and then sugars in alphabetical order
epsamc <- epsamc[ , c(7, 6, 5, 4, 2, 1, 3)]
colnames(epsamc) <- c("Sample", "Fermenter", "AMCGal", "AMCGlc", "AMCGlcN", "AMCMan", "AMCRha")
# Unify fermenter naming: capital "F" followed by fermenter number
epsamc[ , 2] <- paste("F", epsamc[ , 2], sep = "")
# Auto-convert columns now
epsamc[, 1] <- type.convert(epsamc[, 1])
epsamc[, 2] <- type.convert(epsamc[, 2])
# Add new dummy column for monomer sums
epsamc$AMCSum <- rep(NA, nrow(epsamc))
# Reshape content: columns for every fermenter
epsamc <- as.data.frame(reshape(epsamc, idvar = "Sample", timevar = "Fermenter", direction = "wide"))
# Renumber row names
rownames(epsamc) <- NULL
# Reorder columns: first step puts "Sample" at the end
epsamc <- epsamc[ , order(names(epsamc))]
epsamc <- epsamc[ , c(ncol(epsamc), 1:(ncol(epsamc)-1))]
# Apply dilution factor
epsamc[, 2:ncol(epsamc)] <- lchfa1df*epsamc[, 2:ncol(epsamc)]
# Subtract monomeric glucose before hydrolysis
for (i in 1:8) {
	amccol <- paste("AMCGlc.F", i, sep = "")
	pmpcol <- paste("PMPGlc.F", i, sep = "")
	epsamc[ , amccol] <- epsamc[ , amccol] - pmpglc[ , pmpcol]
}
# Calculate sums
# 	Copy dataframe
# 	Replace NAs by 0s
# 	Finally calculate sums
temp.df <- epsamc
temp.df[is.na(temp.df)] <- 0
for (i in 1:8) { # i = Fermenters
	galcol <- paste("AMCGal.F", i, sep = "")
	glccol <- paste("AMCGlc.F", i, sep = "")
	glcncol <- paste("AMCGlcN.F", i, sep = "")
	mancol <- paste("AMCMan.F", i, sep = "")
	rhacol <- paste("AMCRha.F", i, sep = "")
	sumcol <- paste("AMCSum.F", i, sep = "")
	for (j in 1:nrow(epsamc)) {
		epsamc[j, sumcol] <-
			temp.df[j, galcol] + temp.df[j, glccol] +
			temp.df[j, glcncol] + temp.df[j, mancol] +
			temp.df[j, rhacol]
	}
}
remove(temp.df)
# Replace sample number with sample time
# blk2smptim used, because 8th blk1 sample is D600 only
# +1, because R starts indexing content at 1
epsamc[,1] <- blk2smptim[(epsamc[,1]+1),2]
# Change column name accordingly
colnames(epsamc)[1] <- "t"

# Transform molar mass data
# Throw away unneeded columns
mp <- mp[ , c(1, 5)]
# Throw away columns with standards, LiNO3, LCHF1 samples, co-worker samples
mp <- mp[-c(1:13, 15, 23, 32, 41, 50:51, 64, 77, 90, 103:nrow(mp)) ,]
# Split Sample ID: 1.0 -> 1	0
mp <- as.data.frame(cSplit(mp,
	splitCols = "Sample.ID", sep =".", drop = TRUE, type.convert = FALSE))
# Rename columns
colnames(mp) <- c("Mp", "Fermenter", "Sample")
# Unify fermenter naming: capital "F" followed by fermenter number
mp[ , 2] <- paste("F", mp[ , 2], sep = "")
# Reorder columns
mp <- mp[ , c(3, 2, 1)]
# Reshape: Sample	Mp.F1	Mp.F2 ...
mp <- as.data.frame(reshape(mp, idvar = "Sample", timevar = "Fermenter", direction = "wide"))
# Convert column
mp[ ,1] <- type.convert(mp[ ,1])
# Renumber rows
rownames(mp) <- NULL
# Replace sample number with sample time
# blk2smptim used, because 8th blk1 sample is D600 only
# +1, because R starts indexing content at 1
mp[,1] <- blk2smptim[(mp[,1]+1),2]
# Change column name accordingly
colnames(mp)[1] <- "t"

# Transform furfural data
# Remove unnecessary columns (junk, FermGlc.PMP, FermXyl.PMP, HMF)
fur <- fur[ , c(2, 6)]
# Remove unnecessary rows (standards, 10 l samples)
fur <- fur[-c(1:13, 90:nrow(fur)), ]
# Split UID: B01_F1.0 -> B01	F1	0
fur <- as.data.frame(cSplit(fur,
	splitCols = "UID", sep ="_", drop = TRUE, type.convert = FALSE))
fur <- as.data.frame(cSplit(fur,
	splitCols = "UID_2", sep =".", drop = TRUE, type.convert = FALSE))
# Remove unnecessary column
fur <- fur[, -2]
# Rename columns
colnames(fur)[2:3] <- c("Fermenter", "Sample")
# Convert column
fur[ , 3] <- type.convert(fur[ , 3])
# Set negative values to 0 (necessary for plotting)
fur[ ,1] <- with(fur, ifelse(Fur < 0, 0, Fur))
# Convert unit: from mg/l to g/l
fur[ ,1] <- fur[ ,1]/1000
# Reshape: Sample	Fur.F1	Fur.F2	...
fur <- as.data.frame(reshape(fur, idvar = "Sample", timevar = "Fermenter", direction = "wide"))
# Renumber rows
rownames(fur) <- NULL
# Replace sample number with sample time
# blk2smptim used, because 8th blk1 sample is D600 only
# +1, because R starts indexing content at 1
fur[,1] <- blk2smptim[(fur[,1]+1),2]
# Change column name accordingly
colnames(fur)[1] <- "t"

# # # # # # # # # # # # # # # # # # # # 
# Merge data
# 	For every variable, sequence is: block 1 (blk1dat), block 2 (blk2dat)
# Start with fermentation data
blk1dat <- indon[[1]]
for (i in 2:4) {
	blk1dat <- join(blk1dat, indon[[i]], by = c("t"), type = "full", match = "all")
}
blk2dat <- indon[[5]]
for (i in 6:8) {
	blk2dat <- join(blk2dat, indon[[i]], by = c("t"), type = "full", match = "all")
}
# Reorder columns to cluster DO and CO2
blk1dat <- blk1dat[ , c(1, 2, 4, 6, 8, 3, 5, 7, 9)]
blk2dat <- blk2dat[ , c(1, 2, 4, 6, 8, 3, 5, 7, 9)]

# D600 data
blk1dat <- join(blk1dat, blk1d600, by = c("t"), type = "full", match = "all")
blk2dat <- join(blk2dat, blk2d600, by = c("t"), type = "full", match = "all")

# CDM data
blk1dat <- join(blk1dat, blk1cdm, by = c("t"), type = "full", match = "all")
blk2dat <- join(blk2dat, blk2cdm, by = c("t"), type = "full", match = "all")

# Fermenter glucose data
blk1dat <- join(blk1dat, fermglc[ , 1:5], by = "t", type = "full", match = "all")
blk2dat <- join(blk2dat, fermglc[ , c(1, 6:9)], by = "t", type = "full", match = "all")

# Sum of EPS aldose monomers
blk1dat <- join(blk1dat, epsamc[ , c(1, 42:45)], by = "t", type = "full", match = "all")
blk2dat <- join(blk2dat, epsamc[ , c(1, 46:49)], by = "t", type = "full", match = "all")

# Molar mass at RI peak data
blk1dat <- join(blk1dat, mp[ , 1:5], by = "t", type = "full", match = "all")
blk2dat <- join(blk2dat, mp[ , c(1, 6:9)], by = "t", type = "full", match = "all")

# Furfural data
blk1dat <- join(blk1dat, fur[ , 1:5], by = "t", type = "full", match = "all")
blk2dat <- join(blk2dat, fur[ , c(1, 6:9)], by = "t", type = "full", match = "all")

# Remove unnecessary rows of blk1dat (+4 empty)
blk1dat <- blk1dat[1:(nrow(blk1dat)-254), ]

# Remove unnecessary rows of blk2dat (every row after last sample)
blk2dat <- blk2dat[1:(nrow(blk2dat)-108), ]

# Generate statistics and join
quantiles <- c(0.1, 0.50, 0.9)
coltypes <- c("DO", "CO2", "D600", "CDM", "FermGlc", "AMCSum", "Mp", "Fur")
for (i in 1:8) {
	start <- 2 + (4 * (i - 1))
	stop <- start + 3
	newcols <- c(paste(coltypes[i], quantiles[1], sep = "."),
		paste(coltypes[i], quantiles[2], sep = "."),
		paste(coltypes[i], quantiles[3], sep = "."))
	statdat <- as.data.frame(t(apply(blk1dat[, start:stop], 1, quantile, quantiles, na.rm = TRUE)))
	blk1dat[ , newcols] <- statdat
	statdat <- as.data.frame(t(apply(blk2dat[, start:stop], 1, quantile, quantiles, na.rm = TRUE)))
	blk2dat[ , newcols] <- statdat
}
save(blk1dat, file = "block1-plot-data.Rda")
save(blk2dat, file = "block2-plot-data.Rda")

