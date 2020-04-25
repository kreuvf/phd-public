MANDMFIX = m-and-m-intro.tex
MANDMGEN = _materials.tex _methods.tex
MANDM = $(MANDMFIX) $(MANDMGEN)

_m-and-m.tex: $(MANDM)
	cat $(MANDM) > ../$@

_materials.tex:
	$(MAKE) -C materials

_methods.tex:
	$(MAKE) -C methods $@

.PHONY: clean-intermediary _materials.tex _methods.tex

clean-intermediary:
	rm -f $(MANDMGEN)
	$(MAKE) -C methods $@
	$(MAKE) -C materials $@
