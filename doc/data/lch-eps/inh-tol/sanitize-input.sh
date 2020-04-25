#!/bin/bash
# Remove superfluous columns
# Turn commas into points
# Remove header
# Split coordinate into letter and number
# Sort
# Re-add better header
# Remove leading zeros

for inhtolraw in "$@"
do
	sed -r -i \
		-e 's|^ *([^\t]+)\t[^\t]+\t([^\t]+)\t.*$|\1\t\2|' \
		-e 's|,|.|' \
		-e '/^Well\tValue/d' \
		-e 's|^([A-H])([0-9]+)|\1\t\2|' \
		"$inhtolraw"
	sort "$inhtolraw" > "$inhtolraw.tmp"
	mv "$inhtolraw.tmp" "$inhtolraw"
	sed -r -i \
		-e '1s|^(.*)$|y\tx\tAttenuance at 600 nm\n\1|' \
		-e 's|0([1-9])\t|\1\t|' \
		"$inhtolraw"
done