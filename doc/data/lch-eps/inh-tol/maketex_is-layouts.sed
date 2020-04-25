1d # Delete first line
s|^\t|| # Remove the very first tab
s|\t[0-9]+|\t-|g # Remove non-strain wells, replace with empty sign
s|\tMedium|\t-|g # Remove medium wells, replace with empty sign
s|\tWasser|\t-|g # Remove water wells, replace with empty sign
s|\t| \& |g # Turn tabs into LaTeXy cell separators
s|(.)$|\1 \\\\| # Add " \\" at the end
s|([A-H])0([0-9])|\1\2|g # Remove leading zeros
s| Xyl1\.([A-H][0-9]{1,2}) | \\xyli{\1} |g # Replace Xyl1 name with special command
s| Xyl2\.([A-H][0-9]{1,2}) | \\xylj{\1} |g # See above, for Xyl2
