.PHONY: enums_to_curateable curated_to_enums

# in linkml-model-enrichment repo
#   make sample-enum-mapping

# saves to curated_enums.txt by default
# yuck, some default output, some required/no default/some STDOUT
enums_to_curateable:
	poetry run enums_to_curateable \
		--modelfile ../linkml-model-enrichment/synbio_organism_mapped.yaml \
		--enum binomial_name_enum


# do some curation on enums_to_curateable.tsv and save as curated_enums.txt
# Excel wants to call it "*.txt". I'm saving as UTF 16 so I can be sure about the encoding at import time.

curated_to_enums:
	poetry run curated_to_enums \
		--tsv_in curated_enums.txt \
		--model_in ../linkml-model-enrichment/synbio_organism_mapped.yaml \
		--selected_enum binomial_name_enum

