# # # # # # # # # # # # # # #
# Generate graph of inhibitor/LCH tolerance for the presentation
#
# 1.) General function for the plot
# 2.) Data and parameters
# 3.) Make plot
# # # # # # # # # # # # # # #


# # # # # # # # # # # # # # #
# Function definition
# # # # # # # # # # # # # # #
inhLCHPlot <- function(data, colors, legendOrder, outFile){
	# Order: Acet/Form/Laev/Fur/HMF/Van///LCH
	# Convert to percent, only two decimal places needed
	data <- round(100 * data / rep(colSums(data), each = nrow(data)),2)

	svg(outFile)

	par(mar = c(8, 4, 0, 1.2) + 0.2, cex.axis = 1.2)

	barplot(data,
		axes = FALSE,
		border = NA,
		horiz = TRUE,
		cex.sub = 1.1,
		xlim = c(0, 100),
		xlab = "Percentage of Strains in %",
		cex.lab = 1.4,
		las = 2,
		col = colors,
		legend.text = c(
			'(−∞, 5 %)',
			'[5 %, 20 %)',
			'[20 %, 40 %)',
			'[40 %, 60 %)',
			'[60 %, 80 %)',
			'[80 %, 100 %)',
			'[100 %, 120 %)',
			'[120 %, +∞)'
		)[legendOrder],
		args.legend = list(
			x = 104,
			y = -1.5,
			fill = colors[legendOrder],
			border = NA,
			bty = "n",
			ncol = 4,
			text.width = 22,
			x.intersp = 0.4,
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
inhLCH <- read.table('inh-tol/inh-tol-classes.txt', sep = '\t', header = TRUE, row.names = 1, nrows = 6)
inhLCH <- rbind(inhLCH, read.table('lch-tol/lch-tol-classes.txt', sep = '\t', header = TRUE, row.names = 1, nrows = 1))

# Reorder data
inhLCH <- as.matrix(t(inhLCH[rev(c(4, 5, 6, 1, 2, 3, 7)),]))

# Colours for vertical presentation plots
presentationColours = rev(c(
		"#C13AADFF",
		"#703ac1FF",
		"#3a69c1FF",
		"#3ac1b3FF",
		"#3ac14eFF",
		"#8bc13aFF",
		"#c1923aFF",
		"#C13A48FF"
	))

# 2D legend order
legendOrder <- matrix(1:8, nrow = 2, ncol = 4, byrow = T)

# # # # # # # # # # # # # # #
# Make Plot
# # # # # # # # # # # # # # #
inhLCHPlot(inhLCH, presentationColours, legendOrder, '../../fig/inh-lch-tol_presentation.svg')
