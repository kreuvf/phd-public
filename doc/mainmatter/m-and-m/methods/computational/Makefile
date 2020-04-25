# Sequence is important here:
COMPUTATIONAL = computational-intro.tex \
	16s-rdna-seq.tex

_computational.tex: $(COMPUTATIONAL)
	cat $(COMPUTATIONAL) > ../$@

.PHONY: clean-intermediary

clean-intermediary:
	echo 'Nothing to clean-intermediary in computational.'
