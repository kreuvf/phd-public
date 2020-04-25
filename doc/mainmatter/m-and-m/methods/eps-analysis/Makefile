# Sequence is important here:
EPSANALYSIS = eps-analysis-intro.tex \
	molar-mass.tex \
	rheometry.tex \
	monomer-composition.tex \
	periodate-test.tex \
	polymer-mass.tex

_eps-analysis.tex: $(EPSANALYSIS)
	cat $(EPSANALYSIS) > ../$@

.PHONY: clean-intermediary

clean-intermediary:
	echo 'Nothing to clean-intermediary in eps-analysis.'
