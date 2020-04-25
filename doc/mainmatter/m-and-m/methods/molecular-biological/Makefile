# Sequence is important here:
MOLECULARBIOLOGICAL = molecular-biological-intro.tex \
	gdna-extraction.tex \
	dna-concentration.tex \
	16s-rdna-pcr.tex

_molecular-biological.tex: $(MOLECULARBIOLOGICAL)
	cat $(MOLECULARBIOLOGICAL) > ../$@

.PHONY: clean-intermediary

clean-intermediary:
	echo 'Nothing to clean-intermediary in molecular-biological.'
