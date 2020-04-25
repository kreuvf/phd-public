1d # Delete first line
s|\t\t|\t-\t|g # Represent empty wells with a hyphen
s|\t\t|\t-\t|g # Represent empty wells with a hyphen (second run to get almost all)
s|\t$|\t-| # Represent trailing empty wells with a hypen
s|\t| \& |g # Replace every tab with " & "
s|(.)$|\1 \\\\| # Add " \\" at the end
s| EPS1\.([A-H][0-9]{1,2}) | \\epsi{\1} |g # Replace EPS1 syntax with special command
s| EPS2\.([A-H][0-9]{1,2}) | \\epsj{\1} |g # See above, for EPS2
