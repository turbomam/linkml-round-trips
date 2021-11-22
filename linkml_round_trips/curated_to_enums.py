import click
import pandas as pd
from linkml_runtime.utils.schemaview import SchemaView, Annotation
from linkml_runtime.dumpers import yaml_dumper


# overwrites by default?
@click.command()
@click.option('--tsv_in', type=click.Path(exists=True), required=True)
@click.option('--tsv_encoding', default="utf_16", show_default=True)
@click.option('--model_in', type=click.Path(exists=True), required=True)
@click.option('--curated_yaml', type=click.Path(), default="curated.yaml")
@click.option('--selected_enum', required=True)
def enums_to_curateable(tsv_in, model_in, selected_enum, tsv_encoding, curated_yaml):
    from_tsv = pd.read_csv(tsv_in, sep="\t", encoding=tsv_encoding)
    from_tsv.index = from_tsv['text']
    print(from_tsv)
    # check if an index appears more than once
    if from_tsv.index.is_unique:
        ft_dict = from_tsv.to_dict(orient="index")
    else:
        print("index is not unique")
        exit()

    from_model = SchemaView(model_in)
    mschema = from_model.schema

    menum = from_model.get_enum(selected_enum)
    me_pvs = menum.permissible_values
    mep_keys = list(me_pvs.keys())
    mep_keys.sort()

    ft_keys = [i for i in list(ft_dict.keys()) if i == str(i)]

    # ft_keys = [i['text'] for i in ft_dict if i['text'] == str(i['text'])]
    ft_keys.sort()
    # print(ft_keys)

    comparables = list(set(mep_keys).intersection(set(ft_keys)))
    comparables.sort()

    # {'text': 'bacteriophage.T7', 'title': 'Escherichia phage T7', 'meaning': 'NCBITaxon:10760',
    #  'match_val': 'Bacteriophage T7', 'match_type': 'hasExactSynonym', 'cosine': 0.0, 'curated_meaning': nan,
    #  'curated_match': nan, 'curated_type': nan, 'curation_notes': nan}

    for i in comparables:
        # # match on ??? against menum
        # # job 1: apply curations
        print(i)
        model_says = me_pvs[i]
        tsv_says = ft_dict[i]
        if not pd.isna(tsv_says['curated_meaning']) and not pd.isna(tsv_says['curated_match']) and not pd.isna(
                tsv_says['curated_type']):
            model_says.meaning = tsv_says['curated_meaning']
            model_says.title = tsv_says['curated_match']
            # todo delete them, don't set to empty strings
            model_says.annotations["match_val"] = ""
            model_says.annotations["match_type"] = ""
            model_says.annotations["cosine"] = ""
            model_says.annotations["curated"] = True
            print(model_says)
            me_pvs[i] = model_says
    menum.permissible_values = me_pvs
    dumped = yaml_dumper.dumps(menum)
    print(dumped)
    mschema.enums[selected_enum] = menum
    yaml_dumper.dump(mschema, curated_yaml)


if __name__ == '__main__':
    enums_to_curateable()
