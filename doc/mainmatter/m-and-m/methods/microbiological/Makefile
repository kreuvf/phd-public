# Sequence is important here:
MICROBIOLOGICAL = microbiological-intro.tex \
	sterilization.tex \
	_agars-media.tex \
	96well-inoculation.tex \
	cultivation.tex \
	fermentation.tex \
	cryopreservation.tex \
	d600.tex

_microbiological.tex: $(MICROBIOLOGICAL)
	cat $(MICROBIOLOGICAL) > ../$@

_agars-media.tex:
	$(MAKE) -C agars-media $@

.PHONY: clean-intermediary _agars-media.tex

clean-intermediary:
	rm -f _agars-media.tex
	$(MAKE) -C agars-media $@