# # # # # # # # # # # # # # #
# Generate summary table for highlight strains
# # # # # # # # # # # # # # #

# # # # # # # # # # # # # # #
# Read in data
# isp = ISp data
# isr = ISr data
isp <- read.table(
	'ISp_highlights.txt', 
	sep = '\t', 
	header = TRUE, 
	na.strings = "n.a.",
	stringsAsFactors = FALSE,
	fileEncoding = "UTF-8", 
	encoding = "UTF-8")

isr <- read.table(
	'ISr_highlights.txt', 
	sep = '\t', 
	header = TRUE, 
	na.strings = "n.a.",
	stringsAsFactors = FALSE,
	fileEncoding = "UTF-8", 
	encoding = "UTF-8")
	
# Data looks like:
#> isp
#   ISp. Series Strain      Fur      HMF       Van
#1   A05    Fur X1.A10  38.9421   0.0000   45.0688
#2   B01    HMF X1.A10   8.1770   1.4065  516.1782
#3   A09    Van X1.A10   0.0000  -1.4914   52.3396

# # # # # # # # # # # # # # #
# Purge values of non-target inhibitors
# target inhibitor = inhibitor of the test series
# non-target inhibitor = other inhibitor which was also measured

# Add empty row for target inhibitor value
isp$Value <- rep(0, nrow(isp))
isr$Value <- rep(0, nrow(isr))

# Fill value column with the target inhibitor values
for (i in 1:nrow(isp)) {
	isp$Value[i] <- isp[i, isp[i, 2]]
}
for (i in 1:nrow(isr)) {
	isr$Value[i] <- isr[i, isr[i, 2]]
}

# Keep necessary columns (Series (2), Strain (3), Value (7))
isp <- isp[, c(2, 3, 7)]
isr <- isr[, c(2, 3, 7)]

# Change order: Series, Strain, Value -> Strain, Series, Value
isp <- isp[, c(2, 1, 3)]
isr <- isr[, c(2, 1, 3)]

# Set negative values to zero
isp[, 3] <- with(isp, ifelse(Value < 0, 0, Value))
isr[, 3] <- with(isr, ifelse(Value < 0, 0, Value))

# Use g/l (affects isp only, conversion from mg/l to g/l)
isp[, 3] <- isp[ ,3] / 1000

# Combine both data frames
# isa = IS all
isa <- rbind(isp, isr)

# Convert series to factors
isa$Series <- as.factor(isa$Series)

# Convert into wide format
isa <- as.data.frame(reshape(isa, idvar = "Strain", timevar = "Series", direction = "wide"))

# Sort by Strain
isa <- isa[order(isa$Strain),]

# Renumber rows
rownames(isa) <- NULL

# Get summary statistics
lq <- sapply(isa[, 2:7], function(x) quantile(x, 0.25, na.rm = TRUE))
md <- sapply(isa[, 2:7], function(x) quantile(x, 0.50, na.rm = TRUE))
uq <- sapply(isa[, 2:7], function(x) quantile(x, 0.75, na.rm = TRUE))

# Add new rows with lower quartile, median, upper quartile for comparability
# Split two lines instead of adding a c(..) which would coerce everything inside to character
isa[nrow(isa) + 1, 1] <- "Lower quartile"
isa[nrow(isa), 2:7] <- lq
isa[nrow(isa) + 1, 1] <- "Median"
isa[nrow(isa), 2:7] <- md
isa[nrow(isa) + 1, 1] <- "Upper quartile"
isa[nrow(isa), 2:7] <- uq

# Round all values to the second decimal
isa[, 2:7] <- round(isa[, 2:7], 2)

# Renumber rows
rownames(isa) <- NULL

# Better column names
colnames(isa) <- c("Strain", "Fur.", "HMF", "Van.", "Acet.", "Form.", "Laev.")

# Format everything as a string with two decimals for output
isa <- format(isa, nsmall = 2)

# Output file
# First part of the table
write.table(isa[1:(nrow(isa) - 3), ], file = "highlights.txt", sep = "\t", quote = FALSE, col.names = TRUE, row.names = FALSE)
# Single \hline for pretty LaTeX table
tblout <- file("highlights.txt", open = "at") # append in text mode
writeLines("\\hline", tblout)
close(tblout)
# Second part of the table (summary statistics)
write.table(isa[(nrow(isa)-2):(nrow(isa)), ], file = "highlights.txt", append = TRUE, sep = "\t", quote = FALSE, col.names = FALSE, row.names = FALSE)

