#!/bin/bash
sed \
	-r \
	-e '1d' \
	-e 's|\t| \& |g' \
	-e 's|^(.*)$|\1 \\\\|' \
	-e 's|^\\hline \\\\$|\\hline|' \
	-e 's|(X[12]\.[A-H])0([1-9])|\1\2|' \
	-e 's|NA|n.t.|g' \
	-e 's|X1\.([A-H][0-9]+)|\\xyli{\1}|' \
	-e 's|X2\.([A-H][0-9]+)|\\xylj{\1}|' \
highlights.txt > tbl-inh-hcs-highlights.tex
