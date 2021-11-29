.PHONY: enums_to_curateable curated_to_enums mixs_soil nmdc_biosample interleave_soil_biosample

# in linkml-model-enrichment repo
#   make sample-enum-mapping

# saves to enums_to_curateable.tsv by default
# yuck, some default output, some required/no default/some STDOUT
enums_to_curateable:
	poetry run enums_to_curateable \
		--modelfile organisms.yaml \
		--enum binomial_name_enum


# do some curation on enums_to_curateable.tsv and save as curated_organisms.txt
# Excel wants to call it "*.txt". I'm saving as UTF 16 so I can be sure about the encoding at import time.


curated_to_enums:
	poetry run curated_to_enums \
		--tsv_in curated_organisms.txt \
		--model_in organisms.yaml \
		--selected_enum binomial_name_enum

mixs_soil:
	poetry run linkml_to_dh_no_annotations \
		--model_yaml ../mixs-source/model/schema/mixs.yaml \
		--add_pattern_to_guidance \
		--model_class soil

nmdc_biosample:
	poetry run linkml_to_dh_no_annotations \
	--model_yaml ../nmdc-schema/src/schema/nmdc.yaml \
	--model_class biosample \
	--add_pattern_to_guidance

interleave_soil_biosample:
	poetry run interleave_classes \
		--model1 ../mixs-source/model/schema/mixs.yaml \
		--class1 soil \
		--model2 ../nmdc-schema/src/schema/nmdc.yaml \
		--class2 biosample
