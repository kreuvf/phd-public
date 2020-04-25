# Sequence is important here:
BIOCHEMICAL = biochemical-intro.tex \
	agarose-gel-preparation.tex \
	agarose-gel-electrophoresis.tex \
	ethidium-bromide-stain.tex \
	agarose-gel-uv-imaging.tex \
	agarose-gel-band-cutting.tex \
	gel-extraction.tex \
	glucose-assay.tex

_biochemical.tex: $(BIOCHEMICAL)
	cat $(BIOCHEMICAL) > ../$@

.PHONY: clean-intermediary

clean-intermediary:
	echo 'Nothing to clean-intermediary in biochemical.'
