# Sequence is important here:
APPENDICESFIXBEFORE = appendices-intro.tex
APPENDICESGEN = _supplements.tex
APPENDICESFIXAFTER = version.tex

APPENDICES = $(APPENDICESFIXBEFORE) $(APPENDICESGEN) $(APPENDICESFIXAFTER)

_appendices.tex: $(APPENDICES)
	cat $(APPENDICES) > ../$@

_supplements.tex:
	$(MAKE) -C supplements $@

.PHONY: clean-intermediary _supplements.tex

clean-intermediary:
	rm -f $(APPENDICESGEN)
	$(MAKE) -C supplements $@
