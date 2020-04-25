#!/bin/bash

RESULTS=`sed -n -r \
	-e '28,128p' blast-hits.txt | \
sed -r \
	-e 's_^([^ ]+\|)[^| ]+ _\1 _' \
	-e 's|  |\t|g' \
	-e 's_\|_\t_g'  \
	-e 's|\t\t|\t|g'`

PAENI=`echo "$RESULTS" | grep -E --count 'Paenibacillus'`
BACI=`echo "$RESULTS" | grep -E --count 'Bacillus'`
CINERIS=`echo "$RESULTS" | grep -E --count 'Paenibacillus cineris'`
FAVI=`echo "$RESULTS" | grep -E --count 'Paenibacillus favisporus'`
AZO=`echo "$RESULTS" | grep -E --count 'Paenibacillus azoreducens'`
echo "$RESULTS" | head -n10 > blast-summary.txt
echo "
Paenibacillus: $PAENI (cineris: $CINERIS, favisporus: $FAVI, azoreducens: $AZO); Bacillus: $BACI." >> blast-summary.txt