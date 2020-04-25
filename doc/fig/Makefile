FIGS = \
	Molecule_phenol_600dpi.png \
	Molecule_guaiacol_600dpi.png \
	Molecule_syringol_600dpi.png \
	Molecule_p-coumaryl_alcohol_600dpi.png \
	Molecule_coniferyl_alcohol_600dpi.png \
	Molecule_sinapyl_alcohol_600dpi.png \
	Molecule_furfural_600dpi.png \
	Molecule_hydroxymethylfurfural_600dpi.png \
	Molecule_vanillin_600dpi.png \
	Molecule_syringaldehyde_600dpi.png \
	Molecule_acetic_acid_600dpi.png \
	Molecule_formic_acid_600dpi.png \
	Molecule_laevulinic_acid_600dpi.png \
	Molecule_4-hydroxybenzoic_acid_600dpi.png \
	Molecule_gallic_acid_600dpi.png \
	Molecule_2-deoxy-glucose_b-d-pyr_600dpi.png \
	Molecule_arabinose_a-l-fur_600dpi.png \
	Molecule_fucose_b-l-pyr_600dpi.png \
	Molecule_galactosamine_a-d_600dpi.png \
	Molecule_galactose_b-d-pyr_600dpi.png \
	Molecule_galacturonic_acid_b-d-pyr_600dpi.png \
	Molecule_glucosamine_a-d_600dpi.png \
	Molecule_glucose_b-d-pyr_600dpi.png \
	Molecule_glucuronic_acid_b-d-pyr_600dpi.png \
	Molecule_lignin_600dpi.png \
	Molecule_mannose_a-d-pyr_600dpi.png \
	Molecule_methyl_blue_600dpi.png \
	Molecule_n-acetyl-galactosamin_a-d_600dpi.png \
	Molecule_n-acetyl-glucosamine_a-d_600dpi.png \
	Molecule_rhamnose_a-l-pyr_600dpi.png \
	Molecule_ribose_b-d-pyr_600dpi.png \
	Molecule_sirofluor_600dpi.png \
	Molecule_xylose_b-d-pyr_600dpi.png \
	Molecule_xanthan_600dpi.png \
	Molecule_water_blue_600dpi.png \
	dasgip_layout_side_600dpi.png \
	dasgip_layout_top_600dpi.png \
	dilution_streaking_600dpi.png \
	xyl-hcs_glc_600dpi.png \
	xyl-hcs_glc_colour_vert_600dpi.png \
	xyl-hcs_xyl_600dpi.png \
	xyl-hcs_xyl_colour_vert_600dpi.png \
	inh-hcs_comp_600dpi.png \
	inh-hcs_inh-stats_600dpi.png \
	inh-tol_fur_600dpi.png \
	inh-tol_hmf_600dpi.png \
	inh-tol_van_600dpi.png \
	inh-tol_acet_600dpi.png \
	inh-tol_form_600dpi.png \
	inh-tol_laev_600dpi.png \
	inh-lch-tol_presentation_600dpi.png \
	lch-tol_lch_600dpi.png \
	strain_scm0_600dpi.png \
	lch-pf_block1_600dpi.png \
	lch-pf_block1_colour_600dpi.png \
	lch-pf_block2_600dpi.png \
	lch-pf_block2_colour_600dpi.png

figs: $(FIGS)

%_600dpi.png: %.svg
	inkscape -z -d 600 -b white -e $@ $^
	optipng $@

.PHONY: clean-intermediary clean-almost-all figs

clean-intermediary:
	echo 'Nothing to clean-intermediary in fig.'

clean-figures:
	rm -f $(FIGS)

clean-almost-all: clean-figures
