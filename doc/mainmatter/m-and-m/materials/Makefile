MATERIALSFIX = materials-intro.tex \
	chemicals.tex \
	consumables.tex \
	glassware.tex \
	equipment.tex \
	enzymes.tex \
	nucleotides.tex \
	sequences.tex \
	software.tex \
	microorganisms.tex
MATERIALSGEN = 
MATERIALS = $(MATERIALSFIX) $(MATERIALSGEN)

_materials.tex: $(MATERIALS)
	cat $(MATERIALS) > ../$@

.PHONY: clean-intermediary

clean-intermediary:
	echo 'Nothing to clean-intermediary in materials.'
