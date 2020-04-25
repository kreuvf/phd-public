# # # # # # # # # # # # # # # # # # # # 
# Generate graphs of LCHF0
# LCH-PF, three figures, each with six y-axes
# # # # # # # # # # # # # # # # # # # # 
# Plot Defaults
# # # # # # # # # # # # # # # # # # # #
# c(Fur): pch = 2 (triangle pointing upward)
# c(Glc): pch = 6 (triangle pointing downward)
# CDM:    pch = 20 (small circle, filled)
# D600:   pch = 1 (circle)
# Mp:     pch = 5 (diamond)

# # # # # # # # # # # # # # # # # # # #
# Create block 1 plot
# # # # # # # # # # # # # # # # # # # #
# R dimensions are in fucked-up units; 1 inch approx. 2.54 cm
svg('../../../fig/lch-pf_block1.svg', width = 7.0/2.54, height = 16.0/2.54, pointsize = 9)

# Create layout for stacked graphs
# Both plots should have same y-axes length --> heights adjusted, because top
# and middle graphs do not need space for x-axis labels
# c(P) not reliable, do not use
layout(matrix(c(1, 1, 2, 2, 3, 3), 3, 2, byrow = TRUE), heights = c(5.1, 5.1, 5.69))

# Load data
load("block1-plot-data.Rda")

# Top plot: CDM in g/l, Mp in 1E6 g/mol
# CDM
# paragraph
# 	mai: margin in inches (bottom, left, top, right),
# 	mgp: margin (axis title, axis labels, axis line)
par(mai = c(0.5/2.54, 1.1/2.54, 0, 1.1/2.54), mgp = c(3, 1, 0))
# pr = plot rows
pr <- complete.cases(blk1dat[, "CDM.0.5"])
plot((blk1dat[pr, 1]/3600), blk1dat[pr, "CDM.0.5"],
	type = "b", col = "#000000", pch = 20,
	axes = FALSE, xlim = c(0, (blk1dat[nrow(blk1dat), 1]/3600)), ylim = c(0, 10), ann = FALSE)
# Fake spread bars
arrows(
	(blk1dat[pr, 1]/3600), blk1dat[pr, "CDM.0.1"],
	(blk1dat[pr, 1]/3600), blk1dat[pr, "CDM.0.9"],
	length=0.02, angle=90, code=3)
# x: Time axis in hours since inoculation
# second call to fill up axis beyond last tick on the right side
# xm = x-axis maximum
xm <- max(round(blk1dat[, 1]/3600))
axis(side = 1, las = 1, labels = FALSE, at = seq(0, xm, by = 12))
axis(side = 1, las = 1, labels = FALSE, lwd.ticks = 0, at = seq(12*floor(xm / 12), xm, by = 0.1))
# y1: CDM in g/l
axis(side = 2, las = 1, at = seq(0, 10, by = 2))
mtext(side = 2, text = "CDM in g/l", line = 2.6)
# Mp
par(new = TRUE)
pr <- complete.cases(blk1dat[, "Mp.0.5"])
plot((blk1dat[pr, 1]/3600), (blk1dat[pr, "Mp.0.5"])/1E6,
	type = "b", col = "#000000", pch = 5,
	axes = FALSE, xlim = c(0, (blk1dat[nrow(blk1dat), 1]/3600)), ylim = c(0, 12), ann = FALSE)
# Fake spread bars
arrows(
	(blk1dat[pr, 1]/3600), blk1dat[pr, "Mp.0.1"]/1E6,
	(blk1dat[pr, 1]/3600), blk1dat[pr, "Mp.0.9"]/1E6,
	length=0.02, angle=90, code=3)
# y2: Mp in 1E6 g/mol
axis(side = 4, las = 1, at = seq(0, 12, by = 2))
mtext(side = 4, text = expression("M"[p]*" in 10"^6*" g/mol"), line = 3.5)

# Middle plot: D600 in d.u., c(Glc) in g/l
# D600
par(mai = c(0.5/2.54, 1.1/2.54, 0, 1.1/2.54), mgp = c(3, 1, 0))
pr <- complete.cases(blk1dat[, "D600.0.5"])
plot((blk1dat[pr, 1]/3600), blk1dat[pr, "D600.0.5"],
	type = "b", col = "#000000", pch = 1,
	axes = FALSE, xlim = c(0, (blk1dat[nrow(blk1dat), 1]/3600)), ylim = c(0, 10), ann = FALSE)
# Fake spread bars; do not attempt to draw zero-length arrows by drawing 1/100 length arrows
arrows(
	(blk1dat[pr, 1]/3600), blk1dat[pr, "D600.0.1"],
	(blk1dat[pr, 1]/3600), blk1dat[pr, "D600.0.9"]+0.01,
	length=0.02, angle=90, code=3)
# x: Time axis in hours since inoculation
# second call to fill up axis beyond last tick on the right side
xm <- max(round(blk1dat[, 1]/3600))
axis(side = 1, las = 1, labels = FALSE, at = seq(0, xm, by = 12))
axis(side = 1, las = 1, labels = FALSE, lwd.ticks = 0, at = seq(12*floor(xm / 12), xm, by = 0.1))
# y1: D600
axis(side = 2, las = 1, at = seq(0, 10, by = 2))
# d.u. = dimensionless unit
mtext(side = 2, text = "D600 in d.u.", line = 2.6)
# FermGlc
par(new = TRUE)
pr <- complete.cases(blk1dat[, "FermGlc.0.5"])
plot((blk1dat[pr, 1]/3600), blk1dat[pr, "FermGlc.0.5"],
	type = "b", col = "#000000", pch = 6,
	axes = FALSE, xlim = c(0, (blk1dat[nrow(blk1dat), 1]/3600)), ylim = c(0, 25), ann = FALSE)
# Fake spread bars
arrows(
	(blk1dat[pr, 1]/3600), blk1dat[pr, "FermGlc.0.1"],
	(blk1dat[pr, 1]/3600), blk1dat[pr, "FermGlc.0.9"],
	length=0.02, angle=90, code=3)
# y2: FermGlc in g/l
axis(side = 4, las = 1, at = seq(0, 25, by = 5))
mtext(side = 4, text = "c(Glc) in g/l", line = 2.97)

# Bottom plot: DO in %, CO2 in %
par(mai = c(1.0/2.54, 1.1/2.54, 0, 1.1/2.54), mgp = c(3, 1, 0))
# Plot grey (= CO2) spread lines first, then plot black (= DO) spread lines
# CO2 spread lines
plot((blk1dat[, 1]/3600), blk1dat[, "CO2.0.1"],
	type = "l", col = "#707070", lwd = 0.3,
	axes = FALSE, ylim = c(-1, 1), ann = FALSE)
par(new = TRUE)
plot((blk1dat[, 1]/3600), blk1dat[, "CO2.0.9"],
	type = "l", col = "#707070", lwd = 0.3,
	axes = FALSE, ylim = c(-1, 1), ann = FALSE)
# DO spread lines
par(new = TRUE)
plot((blk1dat[, 1]/3600), blk1dat[, "DO.0.1"],
	type = "l", col = "#000000", lwd = 0.3,
	axes = FALSE, ylim = c(0, 120), ann = FALSE)
par(new = TRUE)
plot((blk1dat[, 1]/3600), blk1dat[, "DO.0.9"],
	type = "l", col = "#000000", lwd = 0.3,
	axes = FALSE, ylim = c(0, 120), ann = FALSE)
# CO2 median line
par(new = TRUE)
plot((blk1dat[, 1]/3600), blk1dat[, "CO2.0.5"],
	type = "l", col = "#707070", lwd = 0.7,
	axes = FALSE, ylim = c(-1, 1), ann = FALSE)
# y2: CO2 in %
axis(side = 4, las = 1, at = seq(0, 1, by = 0.2))
mtext(side = 4, text = expression("CO"[2]*" in %"), line = 3.22, at = 0.5)
# DO median line
par(new = TRUE)
plot((blk1dat[, 1]/3600), blk1dat[, "DO.0.5"],
	type = "l", col = "#000000", lwd = 0.7,
	axes = FALSE, ylim = c(0, 120), ann = FALSE)
# x: Time axis in hours since inoculation
# second call to fill up axis beyond last tick on the right side
xm <- max(round(blk1dat[, 1]/3600))
axis(side = 1, las = 1, at = seq(0, xm, by = 12))
axis(side = 1, las = 1, labels = FALSE, lwd.ticks = 0, at = seq(12*floor(xm / 12), xm, by = 0.1))
# Redo values missing due to space constraints
# lwd = 0 to suppress redrawing of the axis line
# lwd.ticks = 0 to suppress redrawing of ticks
axis(side = 1, las = 1, lwd = 0, lwd.ticks = 0, at = c(24, 48, 72, 96, 120))
mtext(side = 1, text = "Time after inoculation in h", line = 2.7)
# y1
axis(side = 2, las = 1, at = seq(0, 100, by = 20))
mtext(side = 2, text = "Dissolved oxygen in %", line = 2.6, at = 50)

dev.off()

# # # # # # # # # # # # # # # # # # # #
# Create block 2 plot
# # # # # # # # # # # # # # # # # # # #

# R dimensions are in fucked-up units; 1 inch approx. 2.54 cm
svg('../../../fig/lch-pf_block2.svg', width = 7.0/2.54, height = 16.0/2.54, pointsize = 9)

# Create layout for stacked graphs
# Both plots should have same y-axes length --> heights adjusted, because top
# and middle graphs do not need space for x-axis labels
# c(P) not reliable, do not use
layout(matrix(c(1, 1, 2, 2, 3, 3), 3, 2, byrow = TRUE), heights = c(5.1, 5.1, 5.69))

# Load data
load("block2-plot-data.Rda")

# Top plot: CDM in g/l, c(Fur.) in 1E2 mg/l, Mp in 1E6 g/mol
# CDM
# paragraph
# 	mai: margin in inches (bottom, left, top, right),
# 	mgp: margin (axis title, axis labels, axis line)
par(mai = c(0.5/2.54, 1.1/2.54, 0, 1.1/2.54), mgp = c(3, 1, 0))
# pr = plot rows
pr <- complete.cases(blk2dat[, "CDM.0.5"])
plot((blk2dat[pr, 1]/3600), blk2dat[pr, "CDM.0.5"],
	type = "b", col = "#000000", pch = 20,
	axes = FALSE, xlim = c(0, (blk2dat[nrow(blk2dat), 1]/3600)), ylim = c(0, 10), ann = FALSE)
# Fake spread bars
arrows(
	(blk2dat[pr, 1]/3600), blk2dat[pr, "CDM.0.1"],
	(blk2dat[pr, 1]/3600), blk2dat[pr, "CDM.0.9"],
	length=0.02, angle=90, code=3)
# c(Fur.)
par(new = TRUE)
pr <- complete.cases(blk2dat[, "Fur.0.5"])
plot((blk2dat[pr, 1]/3600), 10*blk2dat[pr, "Fur.0.5"],
	type = "b", col = "#000000", pch = 2,
	axes = FALSE, xlim = c(0, (blk2dat[nrow(blk2dat), 1]/3600)), ylim = c(0, 10), ann = FALSE)
# Fake spread bars
arrows(
	(blk2dat[pr, 1]/3600), 10*blk2dat[pr, "Fur.0.1"],
	(blk2dat[pr, 1]/3600), 10*blk2dat[pr, "Fur.0.9"],
	length=0.02, angle=90, code=3)
# x: Time axis in hours since inoculation
# second call to fill up axis beyond last tick on the right side
# xm = x-axis maximum
xm <- max(round(blk2dat[, 1]/3600))
axis(side = 1, las = 1, labels = FALSE, at = seq(0, xm, by = 12))
axis(side = 1, las = 1, labels = FALSE, lwd.ticks = 0, at = seq(12*floor(xm / 12), xm, by = 0.1))
# y1: CDM in g/l, c(Fur.) in 1E2 mg/l
axis(side = 2, las = 1, at = seq(0, 10, by = 2))
mtext(side = 2, text = expression("CDM in g/l, c(Fur) in 10"^2*" mg/l"), line = 2.32)
# Mp
par(new = TRUE)
pr <- complete.cases(blk2dat[, "Mp.0.5"])
plot((blk2dat[pr, 1]/3600), (blk2dat[pr, "Mp.0.5"])/1E6,
	type = "b", col = "#000000", pch = 5,
	axes = FALSE, xlim = c(0, (blk2dat[nrow(blk2dat), 1]/3600)), ylim = c(0, 12), ann = FALSE)
# Fake spread bars
arrows(
	(blk2dat[pr, 1]/3600), blk2dat[pr, "Mp.0.1"]/1E6,
	(blk2dat[pr, 1]/3600), blk2dat[pr, "Mp.0.9"]/1E6,
	length=0.02, angle=90, code=3)
# y2: Mp in 1E6 g/mol
axis(side = 4, las = 1, at = seq(0, 12, by = 2))
mtext(side = 4, text = expression("M"[p]*" in 10"^6*" g/mol"), line = 3.5)

# Middle plot: D600 in d.u., c(Glc) in g/l
# D600
par(mai = c(0.5/2.54, 1.1/2.54, 0, 1.1/2.54), mgp = c(3, 1, 0))
pr <- complete.cases(blk2dat[, "D600.0.5"])
plot((blk2dat[pr, 1]/3600), blk2dat[pr, "D600.0.5"],
	type = "b", col = "#000000", pch = 1,
	axes = FALSE, xlim = c(0, (blk2dat[nrow(blk2dat), 1]/3600)), ylim = c(0, 10), ann = FALSE)
# Fake spread bars; do not attempt to draw zero-length arrows by drawing 1/100 length arrows
arrows(
	(blk2dat[pr, 1]/3600), blk2dat[pr, "D600.0.1"],
	(blk2dat[pr, 1]/3600), blk2dat[pr, "D600.0.9"] + 0.01,
	length=0.02, angle=90, code=3)
# x: Time axis in hours since inoculation
# second call to fill up axis beyond last tick on the right side
xm <- max(round(blk2dat[, 1]/3600))
axis(side = 1, las = 1, labels = FALSE, at = seq(0, xm, by = 12))
axis(side = 1, las = 1, labels = FALSE, lwd.ticks = 0, at = seq(12*floor(xm / 12), xm, by = 0.1))
# y1: D600
axis(side = 2, las = 1, at = seq(0, 10, by = 2))
# d.u. = dimensionless unit
mtext(side = 2, text = "D600 in d.u.", line = 2.6)
# FermGlc
par(new = TRUE)
pr <- complete.cases(blk2dat[, "FermGlc.0.5"])
plot((blk2dat[pr, 1]/3600), blk2dat[pr, "FermGlc.0.5"],
	type = "b", col = "#000000", pch = 6,
	axes = FALSE, xlim = c(0, (blk2dat[nrow(blk2dat), 1]/3600)), ylim = c(0, 25), ann = FALSE)
# Fake spread bars
arrows(
	(blk2dat[pr, 1]/3600), blk2dat[pr, "FermGlc.0.1"],
	(blk2dat[pr, 1]/3600), blk2dat[pr, "FermGlc.0.9"],
	length=0.02, angle=90, code=3)
# y2: FermGlc in g/l
axis(side = 4, las = 1, at = seq(0, 25, by = 5))
mtext(side = 4, text = "c(Glc) in g/l", line = 2.97)

# Bottom plot: DO in %, CO2 in %
par(mai = c(1.0/2.54, 1.1/2.54, 0, 1.1/2.54), mgp = c(3, 1, 0))
# Plot grey (= CO2) spread lines first, then plot black (= DO) spread lines
# CO2 spread lines
plot((blk2dat[, 1]/3600), blk2dat[, "CO2.0.1"],
	type = "l", col = "#707070", lwd = 0.3,
	axes = FALSE, ylim = c(-1, 1), ann = FALSE)
par(new = TRUE)
plot((blk2dat[, 1]/3600), blk2dat[, "CO2.0.9"],
	type = "l", col = "#707070", lwd = 0.3,
	axes = FALSE, ylim = c(-1, 1), ann = FALSE)
# DO spread lines
par(new = TRUE)
plot((blk2dat[, 1]/3600), blk2dat[, "DO.0.1"],
	type = "l", col = "#000000", lwd = 0.3,
	axes = FALSE, ylim = c(0, 120), ann = FALSE)
par(new = TRUE)
plot((blk2dat[, 1]/3600), blk2dat[, "DO.0.9"],
	type = "l", col = "#000000", lwd = 0.3,
	axes = FALSE, ylim = c(0, 120), ann = FALSE)
# CO2 median line
par(new = TRUE)
plot((blk2dat[, 1]/3600), blk2dat[, "CO2.0.5"],
	type = "l", col = "#707070", lwd = 0.7,
	axes = FALSE, ylim = c(-1, 1), ann = FALSE)
# y2: CO2 in %
axis(side = 4, las = 1, at = seq(0, 1, by = 0.2))
mtext(side = 4, text = expression("CO"[2]*" in %"), line = 3.22, at = 0.5)
# DO median line
par(new = TRUE)
plot((blk2dat[, 1]/3600), blk2dat[, "DO.0.5"],
	type = "l", col = "#000000", lwd = 0.7,
	axes = FALSE, ylim = c(0, 120), ann = FALSE)
# x: Time axis in hours since inoculation
# second call to fill up axis beyond last tick on the right side
xm <- max(round(blk2dat[, 1]/3600))
axis(side = 1, las = 1, at = seq(0, xm, by = 12))
axis(side = 1, las = 1, labels = FALSE, lwd.ticks = 0, at = seq(12*floor(xm / 12), xm, by = 0.1))
# Redo values missing due to space constraints
# lwd = 0 to suppress redrawing of the axis line
# lwd.ticks = 0 to suppress redrawing of ticks
axis(side = 1, las = 1, lwd = 0, lwd.ticks = 0, at = c(24, 48, 72, 96, 120))
mtext(side = 1, text = "Time after inoculation in h", line = 2.7)
# y1
axis(side = 2, las = 1, at = seq(0, 100, by = 20))
mtext(side = 2, text = "Dissolved oxygen in %", line = 2.6, at = 50)

dev.off()

