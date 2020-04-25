#!/bin/sh
python hits.py hits.txt
sed -r -i \
	-e 's|\r||g' \
	-e 's|\tj|\ty|g' \
	-e 's|Stamm|Strain|g' \
	-e 's|Summe ohne Xylose|Sum|g' \
	-e '1s|([^\t\n\r]+)|{\1}|g' \
	-e 's,^Xyl1\.([A-H]([0-9]|1[0-2]))\t,\\xyli{\1}\t,g' \
	-e 's|\t| \& |g' \
	-e 's|^(.+)$|\1 \\\\|' hits_processed.txt

