# # # # # # # # # # # # # # # # # # # # 
# Generate graphs of EPS aldose monomer composition
# LCH-PF, Strain Selection, four remaining strains
# # # # # # # # # # # # # # # # # # # # 

# # # # # # # # # # # # # # # # # # # # 
# Input data
#
# lpssd = LCH-PF Strain Selection Data
lpssd <- read.table('scm0-results.csv', sep = ';', header = TRUE, row.names = 1, nrows = 6)

# # # # # # # # # # # # # # # # # # # # 
# Process data
# Transpose the input
lpssd <- t(lpssd)

# ro = row order
# Glc, Man, Rha, Gal, GlcUA, GlcN, Rib, GalN, GlcNAc
# Reasoning
# Stack from top to bottom and start with most frequently found monomer
# Important: This does _not_ mean "most abundant".
# E. g. Glc goes first, because it is present in 5/5 polymers,
# then comes Man, present in only 4/5 polymers, ...
# If the amounts are the same, alphabetical order is used
ro = c(8, 1, 5, 9, 2, 3, 4, 6, 7)

# Calculate percentages
lpssd <- round(100 * lpssd / rep(colSums(lpssd), each = nrow(lpssd)),2)

# # # # # # # # # # # # # # # # # # # # 
# Output graph
#
# R dimensions are in fucked-up units; 1 inch approx. 2.53 cm
svg('../../../fig/strain_scm0.svg', width = 13.9/2.53, height = 6/2.53, pointsize = 9)
# paragraph
# 	margin (bottom, left, top, right),
# 	margin (axis title, axis labels, axis line)
par(mar = c(6.1, 5.5, 0, 1), mgp = c(2.5, 1, 0))

# Plot variables
# Colours to use
ctu = c("#606060", "#7C7C7C", "#989898", "#B4B4B4", "#D0D0D0", "#505050", "#505050", "#505050", "#505050")
# Densities to use (for hatched fill bars per inch); -1 = no hatched fill
dtu = c(-1, -1, -1, -1, -1, 23, 41, 23, 41)
# Angles to use (for hatched fill); 0 = ---; 45 = /; -45 = \
atu = c(0, 0, 0, 0, 0, 45, 45, -45, -45)

# Legend variables
# Horizontal legend is only possibly using columns such that 9 items in 2 rows are laid out like:
# 1 3 5 6 7 9
# 2 4 6 8       <-- shit
# New order: 1, 6, 2, 7, 3, 8, 4, 9, 5
lctu = c(ctu[1], "#505050", "#7C7C7C", "#505050", "#989898", "#505050", "#B4B4B4", "#505050", "#D0D0D0")
ldtu = c(-1, 23, -1, 41, -1, 23, -1, 41, -1)
latu = c(0, 45, 0, 45, 0, -45, 0, -45, 0)
# Legend text to use; lro = legend row order
lro = c(8, 3, 1, 4, 5, 6, 9, 7, 2)

# Start plot from top to bottom, need to reverse columns
# Matrix conversion done for barplot input
lpssdmat <- as.matrix(lpssd[ro,])
lpssdmat <- lpssdmat[, rev(seq_len(ncol(lpssdmat)))]

# Prepare column names (worst shit ever, took almost 2 hours to figure that shit out)
lpssdcols = colnames(lpssdmat)
lpssdcols = c(bquote(expression(italic(.(lpssdcols[1])))),
		bquote(expression(italic(" "[M]*"   Xyl2.B8")^top)), # ugly hack
		bquote(expression(italic(.(lpssdcols[3])))),
		bquote(expression(italic(.(lpssdcols[4])))),
		bquote(expression(italic(.(lpssdcols[5])))))

# Plot the stuff
barplot(lpssdmat,
	axes = FALSE,
	xlim = c(0, 100),
	xlab = "Monomer Percentage in %",
	names.arg = c(eval(lpssdcols[[1]]), eval(lpssdcols[[2]]), eval(lpssdcols[[3]]), eval(lpssdcols[[4]]), eval(lpssdcols[[5]])),
	legend.text = row.names(lpssd[lro,]),
	col = ctu,
	horiz = TRUE,
	border = NA,
	las = 2,
	density = dtu,
	angle = atu,
	args.legend = list(
		y = -2.4,
		x = 92,
		fill = lctu,
		density = ldtu,
		angle = latu,
		border = NA,
		ncol = 5,
		bty = "n",
		x.intersp = 1
	)
)
axis(side = 1,
	las = 1,
	at = seq(0, 100, by = 10)
)
dev.off()
