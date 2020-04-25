MAINMATTERFIX = mainmatter-intro.tex abstracts.tex
MAINMATTERGEN = _intro.tex _m-and-m.tex _lch-eps.tex _fun-pf.tex _appendices.tex
#MAINMATTERGEN = _intro.tex _m-and-m.tex _shz-and-scl.tex \
#	_kozakia.tex _curto.tex _lch-eps.tex
MAINMATTER = $(MAINMATTERFIX) $(MAINMATTERGEN)

_mainmatter.tex: $(MAINMATTER)
	cat $(MAINMATTER) > ../$@

_intro.tex:
	$(MAKE) -C intro $@

_m-and-m.tex:
	$(MAKE) -C m-and-m $@

#_kozakia.tex: _koz-disc.tex _koz-outlook.tex

#_curto.tex: _cur-disc.tex _cur-outlook.tex

_lch-eps.tex:
	$(MAKE) -C lch-eps $@

_fun-pf.tex:
	$(MAKE) -C fun-pf $@

#_shz-and-scl.tex: _fermen.tex _char.tex _sirofluor.tex _scl-disc.tex _scl-outlook.tex

_appendices.tex:
	$(MAKE) -C appendices $@

.PHONY: clean-intermediary _intro.tex _m-and-m.tex _lch-eps.tex _fun-pf.tex _appendices.tex

clean-intermediary:
	rm -f _intro.tex _m-and-m.tex _lch-eps.tex _fun-pf.tex _appendices.tex
	$(MAKE) -C intro $@
	$(MAKE) -C m-and-m $@
	$(MAKE) -C lch-eps $@
	$(MAKE) -C appendices $@
