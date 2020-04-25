#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 16S Sequence Analysis Script
# 
# Author: Steven Koenig <steven.koenig.wzs@kreuvf.de>
# Licence: GNU General Public Licence, Version 3
# 
# Requirements: [[TO DO]]
# 
# Description:
# This script scans any directory given for *.ab1 files. All *.ab1 files found
# are expected to contain sequences of PCR products of the same region of
# interest in forward and reverse direction with enough overlap to assemble all
# into one long stretch of DNA.
# 
# In the first step all *.ab1 files are converted to *.fastq. Then, the *.fastq
# files are quality-trimmed and the resulting sequences are converted to FASTA
# format. Reverse sequences are converted to their reverse complement and all
# the sequences are passed to ClustalW for aligning. The raw FASTQ files and the
# quality-trimmed FASTQ files are deleted after script execution.
# 
# You may also give --no-delete to keep all generated intermediate files.
# 
# This script expects your files to be organized like that:
# Organism_0000
# ├── Org0000_fwd_0.ab1
# ├── Org0000_fwd_1.ab1
# ├── Org0000_fwd_2.ab1
# ├── Org0000_fwd_3.ab1
# ├── Org0000_rev_0.ab1
# ├── Org0000_rev_1.ab1
# └── Org0000_rev_2.ab1
# Organism_0001
# ├── Org0001_rev_0.ab1
# ├── Org0001_rev_1.ab1
# └── Org0001_rev_2.ab1
# Organism_0002
# ├── Org0002_fwd_0.ab1
# ├── Org0002_rev_0.ab1
# └── Org0002_rev_1.ab1
# 
# The long term aim is to re-implement DynamicTrim.pl in Python to kick out the
# SolexaQA dependency.

import os
import re
from Bio import SeqIO
from subprocess import call

# Check input
# No argument: exit with help
# One or more arguments: verify that every argument is a directory
# For every directory: verify that it contains at least one *.ab1
# One and only one *.ab1 file: warn about missing alignment, stop after trimming
# Only rev or only fwd *.ab1: warn

for file in os.listdir("."):
    if file.endswith(".ab1"):
        SeqIO.convert(file, "abi", re.findall('^(.*)(\.ab1)$', file)[0][0]+".fastq", "fastq")

records = list()

for file in os.listdir("."):
	if file.endswith(".fastq"):
		call(["DynamicTrim.pl", file, "-probcutoff", "0.05", "-sanger"])
		os.remove(file)
		os.rename(file + ".trimmed", file)
		os.remove(file + ".trimmed_segments")
		handle = open(file, "r")
		if re.findall('rev', file):
			record = SeqIO.read(handle, "fastq")
			rc_record = record.reverse_complement(id=record.id+"_rc")
			records.append(rc_record)
		else:
			records.append(SeqIO.read(handle, "fastq"))
		handle.close()
		os.remove(file)

handle = open("processed_sequences.fasta", "w")
SeqIO.write(records, handle, "fasta")
handle.close()

handle = open("processed_sequences.fasta", "r")
call(["clustalw", "-infile=processed_sequences.fasta", "-align", "-output=FASTA", "-outfile=alignment.fasta"])
handle.close()
os.remove(re.findall('^(.*)(\.fasta)$', "processed_sequences.fasta")[0][0]+".dnd")

print(call(["fastagrep.pl", "-w", "0", "''", "alignment.fasta"]))

