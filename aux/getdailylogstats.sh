#!/bin/bash
git log --date=short | grep -E '^Date:.*[0-9]{4,4}-[0-9]{2,2}-[0-9]{2,2}$' | sed -r -e 's/^Date:[^0-9]*([0-9]+-[0-9]+-[0-9]+)$/\1/' | uniq -c > log-stats-daily.txt
