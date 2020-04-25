#!/bin/sh

# Velvet contigs information table
# Reads in contigs.fa produced by velvetg and outputs unsorted table with contig information
# Outputs one file called contigs.table in the same directory as the contigs.fa
#
# Author: Steven Koenig
# Created: 2013-02-06

E_MISSINGFILE=2
FILENAME="contigs.table"

if [ $# -eq 0 ]
then
	echo 'No filename given.'
	echo 'Usage: ./create_contig_table.sh filename'
	exit $E_MISSINGFILE
fi

FILEPATH=`echo $1 | rev | sed -r 's|^[^/]*/|/|' | rev`

if [ "$FILEPATH" = "$1" ]
then
	FILEPATH=""
fi

echo 'Node	Length	Coverage' > $FILEPATH$FILENAME
grep -E 'length_[0-9]+' $1 | sed -r 's/^>NODE_([0-9]+)_length_([0-9]+)_cov_([0-9]+\.[0-9]+)$/\1\t\2\t\3/' >> $FILEPATH$FILENAME

