thesis-presentation-full.pdf: 
	xelatex thesis-presentation-full.tex
	#pythontex thesis-presentation-full.tex
	#makeindex thesis-presentation-full.nlo -s nomencl.ist -o thesis-presentation-full.nls
	biber thesis-presentation-full
	./build/fake-gitinfo2-data.sh
	SOURCE_DATE_EPOCH=`grep 'commudate' ../.git/gitHeadInfo.gin | grep --only-matching -E '[0-9]+'` \
		SOURCE_DATE_EPOCH_TEX_PRIMITIVES=1 \
		xelatex thesis-presentation-full.tex
	./build/restore-gitinfo2-data.sh

once-full:
	./build/fake-gitinfo2-data.sh
	SOURCE_DATE_EPOCH=`grep 'commudate' ../.git/gitHeadInfo.gin | grep --only-matching -E '[0-9]+'` \
		SOURCE_DATE_EPOCH_TEX_PRIMITIVES=1 \
		xelatex thesis-presentation-full.tex
	./build/restore-gitinfo2-data.sh

thrice-full: 
	xelatex thesis-presentation-full.tex
	#pythontex thesis-presentation-full.tex
	#makeindex thesis-presentation-full.nlo -s nomencl.ist -o thesis-presentation-full.nls
	biber thesis-presentation-full
	xelatex thesis-presentation-full.tex
	biber thesis-presentation-full
	./build/fake-gitinfo2-data.sh
	SOURCE_DATE_EPOCH=`grep 'commudate' ../.git/gitHeadInfo.gin | grep --only-matching -E '[0-9]+'` \
		SOURCE_DATE_EPOCH_TEX_PRIMITIVES=1 \
		xelatex thesis-presentation-full.tex
	./build/restore-gitinfo2-data.sh

xfour-full: 
	xelatex thesis-presentation-full.tex
	#pythontex thesis-presentation-full.tex
	#makeindex thesis-presentation-full.nlo -s nomencl.ist -o thesis-presentation-full.nls
	biber thesis-presentation-full
	xelatex thesis-presentation-full.tex
	biber thesis-presentation-full
	xelatex thesis-presentation-full.tex
	biber thesis-presentation-full
	./build/fake-gitinfo2-data.sh
	SOURCE_DATE_EPOCH=`grep 'commudate' ../.git/gitHeadInfo.gin | grep --only-matching -E '[0-9]+'` \
		SOURCE_DATE_EPOCH_TEX_PRIMITIVES=1 \
		xelatex thesis-presentation-full.tex
	./build/restore-gitinfo2-data.sh

thesis-presentation-short.pdf: 
	xelatex thesis-presentation-short.tex
	#pythontex thesis-presentation-short.tex
	#makeindex thesis-presentation-short.nlo -s nomencl.ist -o thesis-presentation-short.nls
	biber thesis-presentation-short
	./build/fake-gitinfo2-data.sh
	SOURCE_DATE_EPOCH=`grep 'commudate' ../.git/gitHeadInfo.gin | grep --only-matching -E '[0-9]+'` \
		SOURCE_DATE_EPOCH_TEX_PRIMITIVES=1 \
		xelatex thesis-presentation-short.tex
	./build/restore-gitinfo2-data.sh

once-short: 
	./build/fake-gitinfo2-data.sh
	SOURCE_DATE_EPOCH=`grep 'commudate' ../.git/gitHeadInfo.gin | grep --only-matching -E '[0-9]+'` \
		SOURCE_DATE_EPOCH_TEX_PRIMITIVES=1 \
		xelatex thesis-presentation-short.tex
	./build/restore-gitinfo2-data.sh

thrice-short: 
	xelatex thesis-presentation-short.tex
	#pythontex thesis-presentation.tex
	#makeindex thesis-presentation.nlo -s nomencl.ist -o thesis-presentation.nls
	biber thesis-presentation-short
	xelatex thesis-presentation-short.tex
	biber thesis-presentation-short
	./build/fake-gitinfo2-data.sh
	SOURCE_DATE_EPOCH=`grep 'commudate' ../.git/gitHeadInfo.gin | grep --only-matching -E '[0-9]+'` \
		SOURCE_DATE_EPOCH_TEX_PRIMITIVES=1 \
		xelatex thesis-presentation-short.tex
	./build/restore-gitinfo2-data.sh

xfour-short: 
	xelatex thesis-presentation-short.tex
	#pythontex thesis-presentation-short.tex
	#makeindex thesis-presentation-short.nlo -s nomencl.ist -o thesis-presentation-short.nls
	biber thesis-presentation-short
	xelatex thesis-presentation-short.tex
	biber thesis-presentation-short
	xelatex thesis-presentation-short.tex
	biber thesis-presentation-short
	./build/fake-gitinfo2-data.sh
	SOURCE_DATE_EPOCH=`grep 'commudate' ../.git/gitHeadInfo.gin | grep --only-matching -E '[0-9]+'` \
		SOURCE_DATE_EPOCH_TEX_PRIMITIVES=1 \
		xelatex thesis-presentation-short.tex
	./build/restore-gitinfo2-data.sh

clean-tex:
	rm -f thesis-presentation-full.bbl \
	thesis-presentation-full.bcf \
	thesis-presentation-full.blg \
	thesis-presentation-full.ilg \
	thesis-presentation-full.lof \
	thesis-presentation-full.log \
	thesis-presentation-full.lol \
	thesis-presentation-full.lot \
	thesis-presentation-full.lox \
	thesis-presentation-full.mw \
	thesis-presentation-full.nav \
	thesis-presentation-full.nlo \
	thesis-presentation-full.nls \
	thesis-presentation-full.out \
	thesis-presentation-full.run.xml \
	thesis-presentation-full.snm \
	thesis-presentation-full.toc
	rm -f thesis-presentation-short.bbl \
	thesis-presentation-short.bcf \
	thesis-presentation-short.blg \
	thesis-presentation-short.ilg \
	thesis-presentation-short.lof \
	thesis-presentation-short.log \
	thesis-presentation-short.lol \
	thesis-presentation-short.lot \
	thesis-presentation-short.lox \
	thesis-presentation-short.mw \
	thesis-presentation-short.nav \
	thesis-presentation-short.nlo \
	thesis-presentation-short.nls \
	thesis-presentation-short.out \
	thesis-presentation-short.run.xml \
	thesis-presentation-short.snm \
	thesis-presentation-short.toc

clean-intermediary:
	rm -f thesis-presentation-full.aux	
	if [ -d pythontex-files-thesis-presentation-full ] ; then rmdir pythontex-files-thesis-presentation-full ; fi
	rm -f thesis-presentation-short.aux	
	if [ -d pythontex-files-thesis-presentation-short ] ; then rmdir pythontex-files-thesis-presentation-short ; fi

clean-almost-all: clean-intermediary clean-tex

clean-all: clean-almost-all
	rm -f thesis-presentation-full.pdf
	rm -f thesis-presentation-short.pdf

.PHONY: once-full thrice-full xfour-full \
	once-short thrice-short xfour-short \
	clean-tex \
	clean-intermediary clean-almost-all clean-all
