METHODSFIX = 
METHODSGEN = _biochemical.tex _computational.tex _eps-analysis.tex \
	_microbiological.tex _molecular-biological.tex _purification.tex \
	_miscellaneous.tex
METHODS = $(METHODSFIX) $(METHODSGEN)

_methods.tex: $(METHODS)
	cat $(METHODS) > ../$@

_biochemical.tex:
	$(MAKE) -C biochemical $@

_computational.tex:
	$(MAKE) -C computational $@

_eps-analysis.tex:
	$(MAKE) -C eps-analysis $@

_microbiological.tex:
	$(MAKE) -C microbiological $@

_miscellaneous.tex:
	$(MAKE) -C miscellaneous $@

_molecular-biological.tex:
	$(MAKE) -C molecular-biological $@

_purification.tex:
	$(MAKE) -C purification $@

.PHONY: clean-intermediary _biochemical.tex _computational.tex _eps-analysis.tex \
	_microbiological.tex _miscellaneous.tex _molecular-biological.tex \
	_purification.tex

clean-intermediary:
	rm -f $(METHODSGEN)
	$(MAKE) -C biochemical $@
	$(MAKE) -C computational $@
	$(MAKE) -C eps-analysis $@
	$(MAKE) -C microbiological $@
	$(MAKE) -C miscellaneous $@
	$(MAKE) -C molecular-biological $@
	$(MAKE) -C purification $@
