.PHONY: curated_to_enums

curated_to_enums:
	poetry run curated_to_enums \
		--tsv_in curated_enums.txt \
		--model_in ../synbio-schema/handcrafted/model/synbio_organism.yaml \
		--selected_enum binomial_name_enum
