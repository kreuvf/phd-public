# # # # # # # # # # # # # # #
# Generate summary graph for inhibitor degradation
# # # # # # # # # # # # # # #

# # # # # # # # # # # # # # #
# Read in data
# idd = inhibitor degradation data
idd <- read.table(
	'inhibitors-stats.txt', 
	sep = '\t', 
	header = FALSE, 
	row.names = 1,
	col.names = c('Inh', 'P25', 'P50', 'P75'),
	fileEncoding = "UTF-8", 
	encoding = "UTF-8")

# Save short row names
rnames <- c("Fur.", "HMF", "Van.", "Acet.", "Form.", "Laev.")

# # # # # # # # # # # # # # #
# Build graphs
# names.arg is empty to suppress automatic printing of column names from data.frame -.-°

svg('../../../fig/inh-hcs_inh-stats.svg', width = 7.5/2.53, height = 6.0/2.53, pointsize = 11)
# mar = margins around plot: top, left, bottom, right
# cex = character expansion ~ font size relative to default
par(mar = c(3.5, 4.4, 1.5, 0) + 0.2, cex = 0.8)
bp <- barplot(idd$P50,
	axes = FALSE,
	names.arg = c('', '', '', '', '', ''),
	ylab = "Median residual concentration in g/l",
	xlab = "",
	ylim = c(0, 1.1*max(idd$P75)),
	col = 'grey',
	border = 'grey'
)

# Make lines of error bars
segments(bp, idd$P25, bp, idd$P75, lwd = 1)

# Make whiskers of error bars
arrows(bp, idd$P25, bp, idd$P75, lwd = 1, angle = 90, code = 3, length = 0.1)

# y-axis
custat <- seq(0, 3.1, by = 0.5)
axis(side = 2,
	las = 1,
	at = custat,
)

# Text for x-axis
# srt = string rotation
text(
	seq(0.8, 2+ nrow(idd), by = 1.2),
	par("usr")[3] - 0.1, 
	srt = 60,
	adj = 1,
	xpd = TRUE,
	labels = paste(rnames)
)
dev.off()

