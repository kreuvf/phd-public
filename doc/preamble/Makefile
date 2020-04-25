PRECOMMON = \
	pre-cmn-pythontex.tex \
	pre-cmn-csquotes.tex \
	pre-cmn-mhchem.tex \
	pre-cmn-siunitx.tex \
	pre-cmn-morewrites.tex \
	pre-cmn-nomencl.tex \
	pre-cmn-xfrac.tex \
	pre-cmn-gitinfo2.tex \
	pre-cmn-afterpage.tex \
	pre-cmn-pdflscape.tex \
	pre-cmn-caption.tex \
	pre-cmn-flafter.tex \
	pre-cmn-array.tex \
	pre-cmn-booktabs.tex \
	pre-cmn-multirow.tex \
	pre-cmn-longtable.tex \
	pre-cmn-enumitem.tex \
	pre-cmn-threeparttablex.tex \
	pre-cmn-listings.tex \
	pre-cmn-fixme.tex \
	pre-cmn-graphicx.tex \
	pre-cmn-xcolor.tex \
	pre-cmn-subfig.tex \
	pre-cmn-texshade.tex \
	pre-cmn-babel.tex \
	pre-cmn-hyphenat.tex \
	pre-cmn-xpatch.tex \
	pre-cmn-biblatex.tex \
	pre-cmn-varioref.tex \
	pre-cmn-hyperref.tex \
	pre-cmn-cleveref.tex \
	pre-cmn-newcmds.tex \
	pre-cmn-counters.tex \
	pre-cmn-hyphenation.tex
PRENICE = \
	pre-nice-class.tex \
	pre-nice-geom.tex \
	pre-nice-amsmath.tex \
	pre-nice-fontspec.tex \
	pre-nice-unicode-math.tex \
	pre-nice-redef.tex
PRESCS = \
	pre-scs-class.tex \
	pre-scs-geom.tex

_preamble-nice.tex: _pre-nice.tex _pre-common.tex
	cat _pre-nice.tex _pre-common.tex > ../$@

_preamble-scs.tex: _pre-scs.tex _pre-common.tex
	cat _pre-scs.tex _pre-common.tex > ../$@

_pre-nice.tex: $(PRENICE)
	cat $(PRENICE) > $@

_pre-scs.tex: $(PRESCS)
	cat $(PRESCS) > $@

_pre-common.tex: $(PRECOMMON)
	cat $(PRECOMMON) > $@

.PHONY: clean-intermediary _preamble-nice.tex _preamble-scs.tex _pre-nice.tex _pre-scs.tex _pre-common.tex

clean-intermediary:
	rm -f _pre-nice.tex _pre-scs.tex _pre-common.tex
