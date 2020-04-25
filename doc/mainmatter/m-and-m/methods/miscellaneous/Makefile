# Sequence is important here:
MISCELLANEOUS = miscellaneous-intro.tex \
	ph-calibration.tex \
	ph-determination.tex \
	buffer-capacity.tex \
	acid-analysis.tex \
	conductivity.tex \
	inhibitor-analysis.tex \
	uv-vis-abs-spectra.tex

_miscellaneous.tex: $(MISCELLANEOUS)
	cat $(MISCELLANEOUS) > ../$@

.PHONY: clean-intermediary

clean-intermediary:
	echo 'Nothing to clean-intermediary in miscellaneous.'
