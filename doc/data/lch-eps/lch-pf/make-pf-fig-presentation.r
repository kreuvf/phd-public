# # # # # # # # # # # # # # # # # # # # 
# Generate coloured graphs of LCHF0
# LCH-PF, Figures for the presentation
# Three figures per block, all in one file
# Getting them to look the same, but in single files was too hard

# # # # # # # # # # # # # # # # # # # # 
# Plot Defaults
# # # # # # # # # # # # # # # # # # # #
# c(Fur): pch = 2 (triangle pointing upward)
# c(Glc): pch = 6 (triangle pointing downward)
# CDM:    pch = 20 (small circle, filled)
# D600:   pch = 1 (circle)
# Mp:     pch = 5 (diamond)

# Definitions
textcol = "#000000" # black
cdmcol = "#8bc13a" # bright green
mpcol = "#c13aad" # dark pink
glccol = "#703ac1" # purple
d600col = "#c1923a" # gold
co2col = "#c13a48" # red
docol = "#3a69c1" # water blue
furcol = "#3ac14e" # grass green

# # # # # # # # # # # # # # # # # # # #
# Create block 1 plot
# # # # # # # # # # # # # # # # # # # #
# R dimensions are in fucked-up units; 1 inch approx. 2.54 cm
svg('../../../fig/lch-pf_block1_colour.svg', width = 7.0/2.54, height = 16.0/2.54, pointsize = 9)

# Create layout for stacked graphs
# Both plots should have same y-axes length --> heights adjusted, because top
# and middle graphs do not need space for x-axis labels
# c(P) not reliable, do not use
layout(matrix(c(1, 1, 2, 2, 3, 3), 3, 2, byrow = TRUE), heights = c(5.1, 5.1, 5.69))

# Load data
load("block1-plot-data.Rda")


# Top plot
# CDM in g/l, Mp in 1E6 g/mol

# Graph 1: CDM

# paragraph
# 	mai: margin in inches (bottom, left, top, right),
# 	mgp: margin (axis title, axis labels, axis line)
par(
	mai = c(1.0/2.54, 1.1/2.54, 0, 1.1/2.54),
	mgp = c(3, 1, 0)
)

# Assign CDM data
# pr = plot rows
pr <- complete.cases(blk1dat[, "CDM.0.5"])

plot(
	(blk1dat[pr, 1]/3600),
	blk1dat[pr, "CDM.0.5"],
	type = "b",
	col = cdmcol,
	pch = 20,
	axes = FALSE,
	xlim = c(0, (blk1dat[nrow(blk1dat), 1]/3600)),
	ylim = c(0, 10),
	ann = FALSE
)

# Add fake spread bars
arrows(
	(blk1dat[pr, 1]/3600), blk1dat[pr, "CDM.0.1"],
	(blk1dat[pr, 1]/3600), blk1dat[pr, "CDM.0.9"],
	length = 0.02, angle = 90, code = 3, col = cdmcol
)

# Add y-axis 1: CDM in g/l
axis(
	side = 2,
	las = 1,
	at = seq(0, 10, by = 2)
)
mtext(
	side = 2,
	text = "CDM in g/l",
	line = 2.6,
	col = cdmcol
)

# Graph 2: Mp

# Overlay on current graph
par(new = TRUE)

# Assign Mp data
# pr = plot rows
pr <- complete.cases(blk1dat[, "Mp.0.5"])

plot(
	(blk1dat[pr, 1]/3600),
	(blk1dat[pr, "Mp.0.5"])/1E6,
	type = "b",
	col = mpcol,
	pch = 5,
	axes = FALSE,
	xlim = c(0, (blk1dat[nrow(blk1dat), 1]/3600)),
	ylim = c(0, 12),
	ann = FALSE
)

# Add fake spread bars
arrows(
	(blk1dat[pr, 1]/3600), blk1dat[pr, "Mp.0.1"]/1E6,
	(blk1dat[pr, 1]/3600), blk1dat[pr, "Mp.0.9"]/1E6,
	length = 0.02, angle = 90, code = 3, col = mpcol
)

# Add y-axis 2: Mp in 1E6 g/mol
axis(
	side = 4,
	las = 1,
	at = seq(0, 12, by = 2)
)
mtext(
	side = 4,
	text = expression("M"[p]*" in 10"^6*" g/mol"),
	line = 3.5,
	col = mpcol
)

# Add x-axis: Time axis in hours since inoculation
# Get max time value of block 1
xm <- max(round(blk1dat[, 1]/3600))
# Axis with ticks and labels
axis(
	side = 1,
	las = 1,
	at = seq(0, xm, by = 12)
)
# Another call to fill up axis beyond last tick on the right side
axis(
	side = 1,
	las = 1,
	labels = FALSE,
	lwd.ticks = 0,
	at = seq(12*floor(xm / 12), xm, by = 0.1)
)
# All values drawn, enough space; nothing to do
mtext(
	side = 1,
	text = "Time after inoculation in h",
	line = 2.7
)

# Middle plot
# D600 in d.u., c(Glc) in g/l

# Graph 1: D600

# paragraph
# 	mai: margin in inches (bottom, left, top, right),
# 	mgp: margin (axis title, axis labels, axis line)
par(
	mai = c(1.0/2.54, 1.1/2.54, 0, 1.1/2.54),
	mgp = c(3, 1, 0)
)

# Assign D600 data
# pr = plot rows
pr <- complete.cases(blk1dat[, "D600.0.5"])

plot(
	(blk1dat[pr, 1]/3600),
	blk1dat[pr, "D600.0.5"],
	type = "b",
	col = d600col,
	pch = 1,
	axes = FALSE,
	xlim = c(0, (blk1dat[nrow(blk1dat), 1]/3600)),
	ylim = c(0, 10),
	ann = FALSE
)

# Add fake spread bars
# Do not attempt to draw zero-length arrows by drawing 1/100 length arrows
arrows(
	(blk1dat[pr, 1]/3600), blk1dat[pr, "D600.0.1"],
	(blk1dat[pr, 1]/3600), blk1dat[pr, "D600.0.9"]+0.01,
	length = 0.02, angle = 90, code = 3, col = d600col
)

# Add y-axis 1: D600
axis(
	side = 2,
	las = 1,
	at = seq(0, 10, by = 2)
)
# d.u. = dimensionless unit
mtext(
	side = 2,
	text = "D600 in d.u.",
	line = 2.6,
	col = d600col
)

# Graph 2: FermGlc

# Overlay on current graph
par(new = TRUE)

# Assign FermGlc data
# pr = plot rows
pr <- complete.cases(blk1dat[, "FermGlc.0.5"])

plot(
	(blk1dat[pr, 1]/3600),
	blk1dat[pr, "FermGlc.0.5"],
	type = "b",
	col = glccol,
	pch = 6,
	axes = FALSE,
	xlim = c(0, (blk1dat[nrow(blk1dat), 1]/3600)),
	ylim = c(0, 25),
	ann = FALSE
)
# Add fake spread bars
arrows(
	(blk1dat[pr, 1]/3600), blk1dat[pr, "FermGlc.0.1"],
	(blk1dat[pr, 1]/3600), blk1dat[pr, "FermGlc.0.9"],
	length = 0.02, angle = 90, code = 3, col = glccol
)

# Add y-axis 2: FermGlc in g/l
axis(
	side = 4,
	las = 1,
	at = seq(0, 25, by = 5)
)
mtext(
	side = 4,
	text = "c(Glc) in g/l",
	line = 2.97,
	col = glccol
)

# Add x-axis: Time axis in hours since inoculation
# Get max time value of block 1
xm <- max(round(blk1dat[, 1]/3600))
# Axis with ticks and labels
axis(
	side = 1,
	las = 1,
	at = seq(0, xm, by = 12)
)
# Another call to fill up axis beyond last tick on the right side
axis(
	side = 1,
	las = 1,
	labels = FALSE,
	lwd.ticks = 0,
	at = seq(12*floor(xm / 12), xm, by = 0.1)
)
# All values drawn, enough space; nothing to do
mtext(
	side = 1,
	text = "Time after inoculation in h",
	line = 2.7
)

# Bottom plot
# DO in %, CO2 in %

# Graph 1: Bottom spread line of CO2

# paragraph
# 	mai: margin in inches (bottom, left, top, right),
# 	mgp: margin (axis title, axis labels, axis line)
par(
	mai = c(1.0/2.54, 1.1/2.54, 0, 1.1/2.54),
	mgp = c(3, 1, 0)
)

plot(
	(blk1dat[, 1]/3600),
	blk1dat[, "CO2.0.1"],
	type = "l",
	col = co2col,
	lwd = 0.3,
	axes = FALSE,
	ylim = c(-1, 1),
	ann = FALSE
)

# Graph 2: Top spread line of CO2

# Overlay on current graph
par(new = TRUE)

plot(
	(blk1dat[, 1]/3600),
	blk1dat[, "CO2.0.9"],
	type = "l",
	col = co2col,
	lwd = 0.3,
	axes = FALSE,
	ylim = c(-1, 1),
	ann = FALSE
)

# Graph 3: Bottom spread line of DO

# Overlay on current graph
par(new = TRUE)

plot(
	(blk1dat[, 1]/3600),
	blk1dat[, "DO.0.1"],
	type = "l",
	col = docol,
	lwd = 0.3,
	axes = FALSE,
	ylim = c(0, 120),
	ann = FALSE
)

# Graph 4: Top spread line of DO

# Overlay on current graph
par(new = TRUE)

plot(
	(blk1dat[, 1]/3600),
	blk1dat[, "DO.0.9"],
	type = "l",
	col = docol,
	lwd = 0.3,
	axes = FALSE,
	ylim = c(0, 120),
	ann = FALSE
)

# Graph 5: Median line of CO2

# Overlay on current graph
par(new = TRUE)

plot(
	(blk1dat[, 1]/3600),
	blk1dat[, "CO2.0.5"],
	type = "l",
	col = co2col,
	lwd = 0.7,
	axes = FALSE,
	ylim = c(-1, 1),
	ann = FALSE
)

# Add y-axis 2: CO2 in %
axis(
	side = 4,
	las = 1,
	at = seq(0, 1, by = 0.2)
)
mtext(
	side = 4,
	text = expression("CO"[2]*" in %"),
	line = 3.22,
	at = 0.5,
	col = co2col
)

# Graph 6: Median line of DO

# Overlay on current graph
par(new = TRUE)

plot(
	(blk1dat[, 1]/3600),
	blk1dat[, "DO.0.5"],
	type = "l",
	col = docol,
	lwd = 0.7,
	axes = FALSE,
	ylim = c(0, 120),
	ann = FALSE
)

# Add y-axis 1: DO in %
axis(
	side = 2,
	las = 1,
	at = seq(0, 100, by = 20)
)
mtext(
	side = 2,
	text = "Dissolved oxygen in %",
	line = 2.6,
	at = 50,
	col = docol
)

# Add x-axis: Time axis in hours since inoculation
# Get max time value of block 1
xm <- max(round(blk1dat[, 1]/3600))
# Axis with ticks and labels
axis(
	side = 1,
	las = 1,
	at = seq(0, xm, by = 12)
)
# Another call to fill up axis beyond last tick on the right side
axis(
	side = 1,
	las = 1,
	labels = FALSE,
	lwd.ticks = 0,
	at = seq(12*floor(xm / 12), xm, by = 0.1)
)
# All values drawn, enough space; nothing to do
mtext(
	side = 1,
	text = "Time after inoculation in h",
	line = 2.7
)

dev.off()

# # # # # # # # # # # # # # # # # # # #
# Create block 2 plot
# # # # # # # # # # # # # # # # # # # #

# R dimensions are in fucked-up units; 1 inch approx. 2.54 cm
svg('../../../fig/lch-pf_block2_colour.svg', width = 7.0/2.54, height = 16.0/2.54, pointsize = 9)

# Create layout for stacked graphs
# Both plots should have same y-axes length --> heights adjusted, because top
# and middle graphs do not need space for x-axis labels
# c(P) not reliable, do not use
layout(matrix(c(1, 1, 2, 2, 3, 3), 3, 2, byrow = TRUE), heights = c(5.1, 5.1, 5.69))

# Load data
load("block2-plot-data.Rda")


# Top plot
# CDM in g/l, c(Fur.) in 1E2 mg/l, Mp in 1E6 g/mol

# Graph 1: CDM

# paragraph
# 	mai: margin in inches (bottom, left, top, right),
# 	mgp: margin (axis title, axis labels, axis line)
par(
	mai = c(1.0/2.54, 1.1/2.54, 0, 1.1/2.54),
	mgp = c(3, 1, 0)
)

# Assign CDM data
# pr = plot rows
pr <- complete.cases(blk2dat[, "CDM.0.5"])

plot(
	(blk2dat[pr, 1]/3600),
	blk2dat[pr, "CDM.0.5"],
	type = "b",
	col = cdmcol,
	pch = 20,
	axes = FALSE,
	xlim = c(0, (blk2dat[nrow(blk2dat), 1]/3600)),
	ylim = c(0, 10),
	ann = FALSE
)

# Add fake spread bars
arrows(
	(blk2dat[pr, 1]/3600), blk2dat[pr, "CDM.0.1"],
	(blk2dat[pr, 1]/3600), blk2dat[pr, "CDM.0.9"],
	length = 0.02, angle = 90, code = 3, col = cdmcol
)

# Grapoh 2: c(Fur.)

# Overlay on current graph
par(new = TRUE)

# Assign Fur data
# pr = plot rows
pr <- complete.cases(blk2dat[, "Fur.0.5"])

plot(
	(blk2dat[pr, 1]/3600),
	10*blk2dat[pr, "Fur.0.5"],
	type = "b",
	col = furcol,
	pch = 2,
	axes = FALSE,
	xlim = c(0, (blk2dat[nrow(blk2dat), 1]/3600)),
	ylim = c(0, 10),
	ann = FALSE
)

# Add fake spread bars
arrows(
	(blk2dat[pr, 1]/3600), 10*blk2dat[pr, "Fur.0.1"],
	(blk2dat[pr, 1]/3600), 10*blk2dat[pr, "Fur.0.9"],
	length = 0.02, angle = 90, code = 3, col = furcol
)

# Add y-axis 1: CDM in g/l, c(Fur.) in 1E2 mg/l
axis(
	side = 2,
	las = 1,
	at = seq(0, 10, by = 2)
)
# Get different colours in one text by overlaying texts in different colours
mtext(
	side = 2,
	text = expression("CDM in g/l" * phantom(", c(Fur) in 10"^2*" mg/l")),
	line = 2.32,
	col = cdmcol
)
mtext(
	side = 2,
	text = expression(phantom("CDM in g/l, ") * "c(Fur) in 10"^2*" mg/l"),
	line = 2.32,
	col = furcol
)
mtext(
	side = 2,
	text = expression(phantom("CDM in g/l") * ", " * phantom("c(Fur) in 10"^2*" mg/l")),
	line = 2.32,
	col = textcol
)

# Graph 3: Mp

# Overlay on current graph
par(new = TRUE)

pr <- complete.cases(blk2dat[, "Mp.0.5"])

plot(
	(blk2dat[pr, 1]/3600),
	(blk2dat[pr, "Mp.0.5"])/1E6,
	type = "b",
	col = mpcol,
	pch = 5,
	axes = FALSE,
	xlim = c(0, (blk2dat[nrow(blk2dat), 1]/3600)),
	ylim = c(0, 12),
	ann = FALSE
)

# Add fake spread bars
arrows(
	(blk2dat[pr, 1]/3600), blk2dat[pr, "Mp.0.1"]/1E6,
	(blk2dat[pr, 1]/3600), blk2dat[pr, "Mp.0.9"]/1E6,
	length = 0.02, angle = 90, code = 3, col = mpcol
)

# Add y-axis 2: Mp in 1E6 g/mol
axis(
	side = 4,
	las = 1,
	at = seq(0, 12, by = 2)
)
mtext(
	side = 4,
	text = expression("M"[p]*" in 10"^6*" g/mol"),
	line = 3.5,
	col = mpcol
)

# Add x-axis: Time axis in hours since inoculation
# Get max time value of block 2
xm <- max(round(blk2dat[, 1]/3600))
# Axis with ticks and labels
axis(
	side = 1,
	las = 1,
	at = seq(0, xm, by = 12)
)
# Another call to fill up axis beyond last tick on the right side
axis(
	side = 1,
	las = 1,
	labels = FALSE,
	lwd.ticks = 0,
	at = seq(12*floor(xm / 12), xm, by = 0.1)
)
# R does not print certain values when it deems the remaining space too small
# Therefore: Redo values missing due to space constraints (they actually fit!)
# lwd = 0 to suppress redrawing of the axis line
# lwd.ticks = 0 to suppress redrawing of ticks
axis(
	side = 1,
	las = 1,
	lwd = 0,
	lwd.ticks = 0,
	at = c(24, 48, 72, 96, 120)
)
mtext(
	side = 1,
	text = "Time after inoculation in h",
	line = 2.7
)

# Middle plot
# D600 in d.u., c(Glc) in g/l

# Graph 1: D600

# paragraph
# 	mai: margin in inches (bottom, left, top, right),
# 	mgp: margin (axis title, axis labels, axis line)
par(
	mai = c(1.0/2.54, 1.1/2.54, 0, 1.1/2.54),
	mgp = c(3, 1, 0)
)

# Assign D600 data
# pr = plot rows
pr <- complete.cases(blk2dat[, "D600.0.5"])

plot(
	(blk2dat[pr, 1]/3600),
	blk2dat[pr, "D600.0.5"],
	type = "b",
	col = d600col,
	pch = 1,
	axes = FALSE,
	xlim = c(0, (blk2dat[nrow(blk2dat), 1]/3600)),
	ylim = c(0, 10),
	ann = FALSE
)

# Add fake spread bars
# Do not attempt to draw zero-length arrows by drawing 1/100 length arrows
arrows(
	(blk2dat[pr, 1]/3600), blk2dat[pr, "D600.0.1"],
	(blk2dat[pr, 1]/3600), blk2dat[pr, "D600.0.9"] + 0.01,
	length = 0.02, angle = 90, code = 3, col = d600col
)

# Add y-axis 1: D600
axis(
	side = 2,
	las = 1,
	at = seq(0, 10, by = 2)
)
# d.u. = dimensionless unit
mtext(
	side = 2,
	text = "D600 in d.u.",
	line = 2.6,
	col = d600col
)

# Graph 2: FermGlc

# Overlay on current graph
par(new = TRUE)

# Assign FermGlc data
# pr = plot rows
pr <- complete.cases(blk2dat[, "FermGlc.0.5"])

plot(
	(blk2dat[pr, 1]/3600),
	blk2dat[pr, "FermGlc.0.5"],
	type = "b",
	col = glccol,
	pch = 6,
	axes = FALSE,
	xlim = c(0, (blk2dat[nrow(blk2dat), 1]/3600)),
	ylim = c(0, 25),
	ann = FALSE
)
# Add fake spread bars
arrows(
	(blk2dat[pr, 1]/3600), blk2dat[pr, "FermGlc.0.1"],
	(blk2dat[pr, 1]/3600), blk2dat[pr, "FermGlc.0.9"],
	length = 0.02, angle = 90, code = 3, col = glccol
)

# Add y-axis 2: FermGlc in g/l
axis(
	side = 4,
	las = 1,
	at = seq(0, 25, by = 5)
)
mtext(
	side = 4,
	text = "c(Glc) in g/l",
	line = 2.97,
	col = glccol
)

# Add x-axis: Time axis in hours since inoculation
# Get max time value of block 2
xm <- max(round(blk2dat[, 1]/3600))
# Axis with ticks and labels
axis(
	side = 1,
	las = 1,
	at = seq(0, xm, by = 12)
)
# Another call to fill up axis beyond last tick on the right side
axis(
	side = 1,
	las = 1,
	labels = FALSE,
	lwd.ticks = 0,
	at = seq(12*floor(xm / 12), xm, by = 0.1)
)
# R does not print certain values when it deems the remaining space too small
# Therefore: Redo values missing due to space constraints (they actually fit!)
# lwd = 0 to suppress redrawing of the axis line
# lwd.ticks = 0 to suppress redrawing of ticks
axis(
	side = 1,
	las = 1,
	lwd = 0,
	lwd.ticks = 0,
	at = c(24, 48, 72, 96, 120)
)
mtext(
	side = 1,
	text = "Time after inoculation in h",
	line = 2.7
)

# Bottom plot
# DO in %, CO2 in %

# Graph 1: Bottom spread line of CO2

# paragraph
# 	mai: margin in inches (bottom, left, top, right),
# 	mgp: margin (axis title, axis labels, axis line)
par(
	mai = c(1.0/2.54, 1.1/2.54, 0, 1.1/2.54),
	mgp = c(3, 1, 0)
)

plot(
	(blk2dat[, 1]/3600),
	blk2dat[, "CO2.0.1"],
	type = "l",
	col = co2col,
	lwd = 0.3,
	axes = FALSE,
	ylim = c(-1, 1),
	ann = FALSE
)

# Graph 2: Top spread line of CO2

# Overlay on current graph
par(new = TRUE)

plot(
	(blk2dat[, 1]/3600),
	blk2dat[, "CO2.0.9"],
	type = "l",
	col = co2col,
	lwd = 0.3,
	axes = FALSE,
	ylim = c(-1, 1),
	ann = FALSE
)

# Graph 3: Bottom spread line of DO

# Overlay on current graph
par(new = TRUE)

plot(
	(blk2dat[, 1]/3600),
	blk2dat[, "DO.0.1"],
	type = "l",
	col = docol,
	lwd = 0.3,
	axes = FALSE,
	ylim = c(0, 120),
	ann = FALSE
)

# Graph 4: Top spread line of DO

# Overlay on current graph
par(new = TRUE)

plot(
	(blk2dat[, 1]/3600),
	blk2dat[, "DO.0.9"],
	type = "l",
	col = docol,
	lwd = 0.3,
	axes = FALSE,
	ylim = c(0, 120),
	ann = FALSE
)

# Graph 5: Median line of CO2

# Overlay on current graph
par(new = TRUE)

plot(
	(blk2dat[, 1]/3600),
	blk2dat[, "CO2.0.5"],
	type = "l",
	col = co2col,
	lwd = 0.7,
	axes = FALSE,
	ylim = c(-1, 1),
	ann = FALSE
)

# Add y-axis 2: CO2 in %
axis(
	side = 4,
	las = 1,
	at = seq(0, 1, by = 0.2)
)
mtext(
	side = 4,
	text = expression("CO"[2]*" in %"),
	line = 3.22,
	at = 0.5,
	col = co2col
)

# Graph 6: Median line of DO

# Overlay on current graph
par(new = TRUE)

plot(
	(blk2dat[, 1]/3600),
	blk2dat[, "DO.0.5"],
	type = "l",
	col = docol,
	lwd = 0.7,
	axes = FALSE,
	ylim = c(0, 120),
	ann = FALSE
)

# Add y-axis 1: DO in %
axis(
	side = 2,
	las = 1,
	at = seq(0, 100, by = 20)
)
mtext(
	side = 2,
	text = "Dissolved oxygen in %",
	line = 2.6,
	at = 50,
	col = docol
)

# Add x-axis: Time axis in hours since inoculation
# Get max time value of block 2
xm <- max(round(blk2dat[, 1]/3600))
# Axis with ticks and labels
axis(
	side = 1,
	las = 1,
	at = seq(0, xm, by = 12)
)
# Another call to fill up axis beyond last tick on the right side
axis(
	side = 1,
	las = 1,
	labels = FALSE,
	lwd.ticks = 0,
	at = seq(12*floor(xm / 12), xm, by = 0.1)
)
# R does not print certain values when it deems the remaining space too small
# Therefore: Redo values missing due to space constraints (they actually fit!)
# lwd = 0 to suppress redrawing of the axis line
# lwd.ticks = 0 to suppress redrawing of ticks
axis(
	side = 1,
	las = 1,
	lwd = 0,
	lwd.ticks = 0,
	at = c(24, 48, 72, 96, 120)
)
mtext(
	side = 1,
	text = "Time after inoculation in h",
	line = 2.7
)

dev.off()
