# # # # # # # # # # # # # # # # # # # # 
# Generate graphs of EPS aldose monomer composition
# LCH-EPS, Inhibitor High Content Screening
# # # # # # # # # # # # # # # # # # # # 

# # # # # # # # # # # # # # # # # # # # 
# Input data
#
# leihd = LCH-EPS Inhibitor High Content Screening Data
leihd <- read.table(
	'hiperf_comp.txt',
	sep = '\t',
	colClasses = c("character", "character", "factor", "character", "factor", rep("numeric", 5)),
	na.strings = c("n.a.", "n.d."),
	header = TRUE,
	nrows = 4)

# # # # # # # # # # # # # # # # # # # # 
# Process data

# Properly sort by Xyl and then Inhibitors
# (so that it looks like everything's sorted by the ID column)
# Save the column names
leihdcols <- colnames(leihd)
# Explicitly give the inhibitor sort order
leihd$Inhi. <- factor(leihd$Inhi., levels = c("Fur.", "HMF", "Van.", "Acet.", "Form.", "Laev.", "none"))
# Re-apply the saved column names
colnames(leihd) <- leihdcols
# Do the sorting
leihd <- leihd[order(leihd$Xyl, leihd$Inhi.),]

# Remove unnecessary columns:
# MSUID (1), IS nomenclature (2), Xyl nomenclature (3), EPS nomenclature (4), Sum (last)
leihd <- leihd[,c(5:(ncol(leihd)-1))]

# Remove now-duplicate entries
# Before, the IS column and the Xyl column in conjunction with the inhibitor
# column were used (by humans) to distinguish, but for the presentation
# of the data it is not necessary to re-show the same BR data more than once.
leihd <- unique(leihd)

# Replace all NAs with 0.0
leihd[is.na(leihd)] <- 0.0

# Get column names
leihdcols <- colnames(leihd)

# Renumber rows
rownames(leihd) <- NULL

# Calculate percentages
leihd[, 2:5] <- round(100 * leihd[, 2:5] / rowSums(leihd[, 2:5]), 2)

# From here on, work with the important part of the data only
plotdata <- leihd[, 2:5]

# Transpose for plotting
plotdata <- t(plotdata)

# # # # # # # # # # # # # # # # # # # # 
# Output graph
#
# R dimensions are in fucked-up units; 1 inch approx. 2.53 cm
# Height calculated as: 0.7 cm per bar + 2.5 cm for rest of the figure
svg('../../../fig/inh-hcs_comp.svg', width = 13.9/2.53, height = 5.3/2.53, pointsize = 9)
# paragraph
# 	margin (bottom, left, top, right),
# 	margin (axis title, axis labels, axis line)
par(mar = c(6.5, 5, 0, 1), mgp = c(2.5, 1, 0))

# Plot variables
# Colours to use
# ctu = c("#A0A0A0", "#A0A000", "#00A0A0", "#A000A0", "#A00000", "#00A000", "#0000A0", "#FF5050", "#50FF50", "#5050FF")
# Grayscale values to use
ctu = c("#303030", "#606060", "#909090", "#C0C0C0")
# Densities to use (for hatched fill bars per inch); -1 = no hatched fill
dtu = c(-1, -1, -1, -1)
# Angles to use (for hatched fill); 0 = ---; 45 = /; -45 = \
atu = c(0, 0, 0, 0)

# Legend text to use; lro = legend row order; legtxt = legend text
lro = c(1, 2, 3, 4)
legtxt = row.names(plotdata[lro,])

# Start plot from top to bottom, need to reverse columns
# Matrix conversion done for barplot input
plotdatamat <- as.matrix(plotdata)
plotdatamat <- plotdatamat[, rev(seq_len(ncol(plotdatamat)))]

# Prepare column names
# Reverse order (as plot is built from bottom to top)
plotdatacols = rev(leihd$Inhi.)
# Get strain names; as.matrix to convert factor to string
# spnam = split names
spnam <- strsplit(as.matrix(plotdatacols), ",")

# Italicize strain name, add ",", add inhibitor name
nicenames <- c()
for (i in 1:length(spnam)) {
	# Get strain name
	nicenames <- append(
		nicenames, c(
			bquote(
				expression(
					paste(
						.(spnam[[i]][1])
					)
				)
			)
		)
	)
}
# Evaluate all the names
stylishnames <- c()
for (i in 1:length(nicenames)) {
	stylishnames <- append(stylishnames, eval(nicenames[[i]]))
}
print(legtxt)
# Plot the stuff
barplot(plotdatamat,
	axes = FALSE,
	xlim = c(0, 100),
	xlab = "Monomer Percentage in %",
	names.arg = stylishnames,
	legend.text = legtxt,
	col = ctu,
	horiz = TRUE,
	border = NA,
	las = 2,
	density = dtu,
	angle = atu,
	args.legend = list(
		y = -2.8,
		x = 82,
		fill = ctu,
		density = dtu,
		angle = atu,
		border = NA,
		ncol = 4,
		bty = "n",
		x.intersp = 1
	)
)
axis(side = 1,
	las = 1,
	at = seq(0, 100, by = 10)
)
dev.off()

# Hints conversion from 2017-03-10
# alter Zustand der Inputdatei
# 16 Spalten, letzte 11 Monomere + Summe
# erste 5: IS, Xyl, Inh., EPS, ID
#
# neuer Zustand der Inputdatei
# 10 Spalten, letzte 5 Monomere + Summe
# erste 5: MSUID, IS, Xyl, EPS, Inh.
#
# Änderungen (alt -> neu):
# 1 -> 2
# 2 -> 3
# 3 -> 5
# 4 =  4
# 5 -> entfällt
#
# 6 -> entfällt
# 7 -> 6
# 8 -> entfällt
# 9 -> entfällt
# 10 -> 7
# 11 -> entfällt
# 12 -> 8
# 13 -> entfällt
# 14 -> 9
# 15 -> entfällt
# 16 -> 10
#
# ID-Spalte nicht mehr benötigt in weiterer Verarbeitung, da ohnehin gleicher Stamm --> Bezüge auf ID-Spalte durch Inhi. ersetzen (und auch Inh. durch Inhi. ersetzen ;D)
