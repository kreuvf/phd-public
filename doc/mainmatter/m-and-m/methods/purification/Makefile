# Sequence is important here:
PURIFICATION = purification-intro.tex \
	cell-separation.tex \
	cff.tex \
	ht-eps-purification.tex \
	precipitation.tex

_purification.tex: $(PURIFICATION)
	cat $(PURIFICATION) > ../$@

.PHONY: clean-intermediary

clean-intermediary:
	echo 'Nothing to clean-intermediary in purification.'
