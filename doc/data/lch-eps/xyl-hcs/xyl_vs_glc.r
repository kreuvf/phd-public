# # # # # # # # # # # # # # #
# Generate graphs of EPS aldose monomer composition
#
# 1.) General function for AMC plots
# 2.) Data and parameters
# 3.) Make plots
# # # # # # # # # # # # # # #


# # # # # # # # # # # # # # #
# Function definition
# # # # # # # # # # # # # # #
# Function for xyl-hcs_xyl plots (greyscale for thesis, colour for presentation)
# AMC: aldose monomer composition
AMCPlotThesis <- function(hits, rowOrder, colors, outFile){
	# Convert to percent, only two decimal places needed
	hits <- round(100 * hits / rep(colSums(hits), each = nrow(hits)),2)

	svg(outFile)

	par(mar = c(7, 4.4, 0.6, 0) + 0.2)

	barplot(as.matrix(hits[rowOrder,]),
		axes = FALSE,
		ylim = c(0, 100),
		ylab = "Monomer Percentage in %",
		legend.text = rev(row.names(hits[rowOrder,])),
		border = NA,
		las = 2,
		col = colors,
		args.legend = list(
			y = -0.17 * max(colSums(hits)),
			fill = colors,
			border = NA,
			bty = "n",
			text.width = c(1.05, 1.05, 1.05, 1.12, 1.14, 1.05, 1.05, 1.05),
			x.intersp = 0.4,
			horiz = TRUE
		)
	)
	axis(side = 2,
		las = 1,
		at = seq(0, 100, by = 10)
	)
	dev.off()
}

AMCPlotPresentation <- function(hits, rowOrder, colors, outFile){
	# Convert to percent, only two decimal places needed
	hits <- round(100 * hits / rep(colSums(hits), each = nrow(hits)),2)

	svg(outFile)

	par(mar = c(7, 5.4, 0, 1) + 0.2, cex.axis = 1.2)

	barplot(as.matrix(rev(hits[rowOrder,])),
		axes = FALSE,
		border = NA,
		horiz = TRUE,
		cex.sub = 1.1,
		xlim = c(0, 100),
		xlab = "Monomer Percentage in %",
		cex.lab = 1.4,
		las = 2,
		col = colors,
		legend.text = row.names(hits[rowOrder,]),
		args.legend = list(
			x = 100,
			y = 0.18*(-0.17 * max(colSums(hits))),
			fill = colors,
			border = NA,
			bty = "n",
			text.width = 7*c(1.05, 1.05, 1.05, 1.12, 1.14, 1.05, 1.05, 1.05),
			x.intersp = 0.4,
			horiz = TRUE,
			cex = 1.2
		)
	)
	axis(side = 1,
		las = 1,
		at = seq(0, 100, by = 10),
		lwd = 2,
		cex.axis = 1.2
	)
	dev.off()
}

# # # # # # # # # # # # # # #
# Data and Parameters
# # # # # # # # # # # # # # #

# Polymers on xylose
# xhh = xyl-hcs_hits
# Cols: Hits
# Rows: Monomers, only first 8 rows relevant
xhh <- read.table('hits.txt', sep = '\t', header = TRUE, row.names = 1, nrows = 8)

# ro = row order
# Gal, Rha, Glc, Man, GlcUA, GlcN, Rib, Fuc
# Reasoning
# Stack from top to bottom and start with most frequently found monomer
# Important: This does _not_ mean "most abundant".
# E. g. Gal goes first, because it is present in 13/13 polymers,
# then comes Rha, also present in 13/13 polymers,
# then comes Glc, present in only 12/13 polymers, ...
ro = c(2, 7, 3, 6, 5, 4, 8, 1)


# Polymers on glucose
# brh = Broder's hits
brh <- read.table('hits_glc_BR.txt', sep = '\t', header = TRUE, row.names = 1, nrows = 10, blank.lines.skip = FALSE)

# brh contains GalN, GalUA as well
# Remove those
brh <- brh[-c(3, 4), ]


# Colours for vertical presentation plots
presentationColours = c(
		"#C13A48FF",
		"#3ac1b3FF",
		"#c1923aFF",
		"#3a69c1FF",
		"#8bc13aFF",
		"#703ac1FF",
		"#3ac14eFF",
		"#C13AADFF"
	)

# # # # # # # # # # # # # # #
# Make Plots
# # # # # # # # # # # # # # #
# Thesis plots
AMCPlotThesis(
	hits = xhh,
	rowOrder = ro,
	colors = grey.colors(nrow(xhh)),
	outFile = '../../../fig/xyl-hcs_xyl.svg'
)
AMCPlotThesis(
	hits = brh,
	rowOrder = ro,
	colors = grey.colors(nrow(brh)),
	outFile = '../../../fig/xyl-hcs_glc.svg'
)

# Presentation plots
AMCPlotPresentation(
	hits = xhh,
	rowOrder = ro,
	colors = presentationColours,
	outFile = '../../../fig/xyl-hcs_xyl_colour_vert.svg'
)
AMCPlotPresentation(
	hits = brh,
	rowOrder = ro,
	colors = presentationColours,
	outFile = '../../../fig/xyl-hcs_glc_colour_vert.svg'
)
