NICE = _preamble-nice.tex _titlepage.tex _frontmatter.tex _mainmatter.tex _backmatter.tex
SCS = _preamble-scs.tex _titlepage.tex _frontmatter.tex _mainmatter.tex _backmatter.tex

# Git Data Faking
# Since the publicly available repository only exposes selected commits, the hashes do not match with the originally used ones. This also means that builds are not reproducible anymore.
# All the raw data (images, tex files) used in the thesis remain unchanged and the final thesis will yield a byte-identical file if the Git data are correct.
# Therefore, a static gitHeadInfo.gin will be copied over the one created by the hooks of the gitinfo2 package. The original data are backed up, so you do not have to check out again to get the actual gitHeadInfo.gin back. The original data get restored as part of the build process.

thesis-nice.pdf: figs _thesis-nice.tex
	xelatex _thesis-nice.tex
	pythontex _thesis-nice.tex
	makeindex _thesis-nice.nlo -s nomencl.ist -o _thesis-nice.nls
	biber _thesis-nice
	./build/fake-gitinfo2-data.sh
	SOURCE_DATE_EPOCH=`grep 'commudate' ../.git/gitHeadInfo.gin | grep --only-matching -E '[0-9]+'` \
		SOURCE_DATE_EPOCH_TEX_PRIMITIVES=1 \
		xelatex _thesis-nice.tex
	./build/restore-gitinfo2-data.sh
	mv _thesis-nice.pdf thesis-nice.pdf

#thesis-scs.pdf: _thesis-scs.tex

_thesis-nice.tex: $(NICE)
	cat $(NICE) > $@

#_thesis-scs.tex: $(SCS)
#	cat $(SCS) > $@

_preamble-nice.tex: 
	$(MAKE) -C preamble $@

_titlepage.tex:
	$(MAKE) -C titlepage $@

_frontmatter.tex:
	$(MAKE) -C frontmatter $@

_mainmatter.tex:
	$(MAKE) -C mainmatter $@

_backmatter.tex:
	$(MAKE) -C backmatter $@

figs:
	$(MAKE) -C fig $@

once: figs _thesis-nice.tex
	./build/fake-gitinfo2-data.sh
	SOURCE_DATE_EPOCH=`grep 'commudate' ../.git/gitHeadInfo.gin | grep --only-matching -E '[0-9]+'` \
		SOURCE_DATE_EPOCH_TEX_PRIMITIVES=1 \
		xelatex _thesis-nice.tex
	./build/restore-gitinfo2-data.sh
	mv _thesis-nice.pdf thesis-nice.pdf

thrice: figs _thesis-nice.tex
	xelatex _thesis-nice.tex
	pythontex _thesis-nice.tex
	makeindex _thesis-nice.nlo -s nomencl.ist -o _thesis-nice.nls
	biber _thesis-nice
	xelatex _thesis-nice.tex
	biber _thesis-nice
	./build/fake-gitinfo2-data.sh
	SOURCE_DATE_EPOCH=`grep 'commudate' ../.git/gitHeadInfo.gin | grep --only-matching -E '[0-9]+'` \
		SOURCE_DATE_EPOCH_TEX_PRIMITIVES=1 \
		xelatex _thesis-nice.tex
	./build/restore-gitinfo2-data.sh
	mv _thesis-nice.pdf thesis-nice.pdf

xfour: figs _thesis-nice.tex
	xelatex _thesis-nice.tex
	pythontex _thesis-nice.tex
	makeindex _thesis-nice.nlo -s nomencl.ist -o _thesis-nice.nls
	biber _thesis-nice
	xelatex _thesis-nice.tex
	biber _thesis-nice
	xelatex _thesis-nice.tex
	biber _thesis-nice
	./build/fake-gitinfo2-data.sh
	SOURCE_DATE_EPOCH=`grep 'commudate' ../.git/gitHeadInfo.gin | grep --only-matching -E '[0-9]+'` \
		SOURCE_DATE_EPOCH_TEX_PRIMITIVES=1 \
		xelatex _thesis-nice.tex
	./build/restore-gitinfo2-data.sh
	mv _thesis-nice.pdf thesis-nice.pdf

clean-figures:
	$(MAKE) -C fig $@

clean-tex:
	rm -f _thesis-nice.tex
	rm -f _thesis-nice.bbl \
	_thesis-nice.bcf \
	_thesis-nice.blg \
	_thesis-nice.ilg \
	_thesis-nice.lof \
	_thesis-nice.log \
	_thesis-nice.lol \
	_thesis-nice.lot \
	_thesis-nice.lox \
	_thesis-nice.mw \
	_thesis-nice.nlo \
	_thesis-nice.nls \
	_thesis-nice.out \
	_thesis-nice.run.xml \
	_thesis-nice.toc

clean-intermediary:
	rm -f $(NICE)
	rm -f $(SCS)
	$(MAKE) -C preamble $@
	$(MAKE) -C titlepage $@
	$(MAKE) -C frontmatter $@
	$(MAKE) -C mainmatter $@
	$(MAKE) -C backmatter $@
	rm -f pythontex-files-_thesis-nice/pythontex_data.pkl \
	pythontex-files-_thesis-nice/_thesis-nice.pytxmcr \
	pythontex-files-_thesis-nice/*.stdout \
	pythontex-files-_thesis-nice/_thesis-nice.pytxpyg \
	_thesis-nice.pytxcode \
	_thesis-nice.aux	
	if [ -d pythontex-files-_thesis-nice ] ; then rmdir pythontex-files-_thesis-nice ; fi

clean-almost-all: clean-intermediary clean-figures clean-tex

clean-all: clean-almost-all
	rm -f thesis-nice.pdf

.PHONY: once thrice xfour \
	clean-figures clean-tex \
	clean-intermediary clean-almost-all clean-all \
	_preamble-nice.tex _titlepage.tex _frontmatter.tex _mainmatter.tex _backmatter.tex
