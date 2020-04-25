# # # # # # # # # # # # # # #
# Generate graphs of inhibitor tolerance for each inhibitor
#
# 1.) Furfural
# 2.) Hydroxymethylfurfural
# 3.) Vanillin
# 4.) Acetic acid
# 5.) Formic acid
# 6.) Laevulinic acid
# # # # # # # # # # # # # # #

# # # # # # # # # # # # # # #
# Read in data for all figures
# itd = inhibitor tolerance data
# 'E' = empty
itd <- read.table(
	'inh-tol-classes.txt', 
	sep = '\t', 
	header = TRUE, 
	row.names = 1,
	col.names = c('E', '0', '1', '2', '3', '4', '5', '6', '7'),
	fileEncoding="UTF-8", 
	encoding="UTF-8")

# Define real column names
cnames <- c('(−∞, 5 %)', '[5 %, 20 %)', '[20 %, 40 %)', '[40 %, 60 %)', '[60 %, 80 %)', '[80 %, 100 %)', '[100 %, 120 %)', '[120 %, +∞)')

# Define function for generating graphs
# itmg = inhibitor tolerance make graph
# names.arg is empty to suppress automatic printing of column names from data.frame -.-°
itmg <- function(filename, rowname)
{
	svg(filename, width = 7.5/2.53, height = 6.0/2.53, pointsize = 11)
	# mar = margins around plot: bottom, left, top, right
	# cex = character expansion ~ font size relative to default
	par(mar = c(5.5, 4.4, 1.5, 0) + 0.2, cex = 0.65)
	bp <- barplot(as.matrix(itd[rowname,]),
		axes = FALSE,
		names.arg = c('', '', '', '', '', '', '', ''),
		ylab = "Number of strains in class",
		xlab = "",
		col = 'grey',
		border = 'grey'
	)
	if (max(as.matrix(itd[rowname,])) < 80) {
		custat <- seq(0, 100, by = 5)
	} else {
		custat <- seq(0, 100, by = 10)
	}
	axis(side = 2,
		las = 1,
		at = custat,
	)
	# Text on top of bars
	text(
		x = bp,
		y = as.matrix(itd[rowname,]),
		label = as.matrix(itd[rowname,]),
		pos = 3,
		col = "black",
		xpd = TRUE
	)
	# Text for x-axis
	# srt = string rotation
	# y position set using an offset constant among graphs
	text(
		seq(0.8, 2 + ncol(itd[rowname,]), by = 1.2),
		y = -(1/28)*max(as.matrix(itd[rowname,])), 
		srt = 60,
		adj = 1,
		xpd = TRUE,
		labels = paste(cnames)
	)
	dev.off()
}

# 1.) Furfural
itmg('../../../fig/inh-tol_fur.svg', 'Fur.')

# 2.) Hydroxymethylfurfural
itmg('../../../fig/inh-tol_hmf.svg', 'HMF')

# 3.) Vanillin
itmg('../../../fig/inh-tol_van.svg', 'Van.')

# 4.) Acetic acid
itmg('../../../fig/inh-tol_acet.svg', 'Acet.')

# 5.) Formic acid
itmg('../../../fig/inh-tol_form.svg', 'Form.')

# 6.) Laevulinic acid
itmg('../../../fig/inh-tol_laev.svg', 'Laev.')

