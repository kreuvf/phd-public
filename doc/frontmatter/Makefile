FRONTMATTER = \
	frontmatter-intro.tex \
	toc.tex \
	list-of-figures.tex \
	list-of-tables.tex \
	list-of-listings.tex \
	foreword.tex \
	acknowledgements.tex \
	dedication.tex

_frontmatter.tex: $(FRONTMATTER)
	cat $(FRONTMATTER) > ../$@

.PHONY: clean-intermediary _frontmatter.tex

clean-intermediary:
	echo 'Nothing to clean-intermediary in frontmatter.'
