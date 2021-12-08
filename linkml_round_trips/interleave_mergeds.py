from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.dumpers import yaml_dumper
# Annotation
from linkml_runtime.linkml_model import (
    SchemaDefinition, ClassDefinition, SlotDefinition
)
from deepdiff import DeepDiff
# from pprint import pformat, pprint
import yaml
from linkml_runtime.loaders import yaml_loader

merged_sv = SchemaView("target/soil_biosample.yaml")

mixs_soil_class = "soil"
nmdc_biosample_class = "biosample"
source_names = ["MIxS", "NMDC"]
shared_base = "soil_biosample"
shared_schema_name = shared_base + "_schema"
shared_schema_id = "http://example.com/" + shared_base
shared_class_name = shared_base + "_class"
shared_schema_owner = shared_schema_id
dump_dest = "target/soil_biosample_interleaved.yaml"

all_res = ['classes', 'enums', 'prefixes', 'slots', 'subsets', 'types']

mixs_soil_ics = merged_sv.class_induced_slots(mixs_soil_class)
mixs_soil_ics_names = [i.name for i in mixs_soil_ics]
mixs_soil_ics_dict = dict(zip(mixs_soil_ics_names, mixs_soil_ics))
mixs_soil_ics_names.sort()

nmdc_biosample_ics = merged_sv.class_induced_slots(nmdc_biosample_class)
nmdc_biosample_ics_names = [i.name for i in nmdc_biosample_ics]
nmdc_biosample_ics_dict = dict(zip(nmdc_biosample_ics_names, nmdc_biosample_ics))
nmdc_biosample_ics_names.sort()

mixs_soil_only = list(set(mixs_soil_ics_names) - set(nmdc_biosample_ics_names))
mixs_soil_only.sort()
nmdc_biosample_only = list(set(nmdc_biosample_ics_names) - set(mixs_soil_ics_names))
nmdc_biosample_only.sort()
ms_nb_intersection = list(set(nmdc_biosample_ics_names).intersection(set(mixs_soil_ics_names)))
ms_nb_intersection.sort()
ms_nb_disjoint_union = mixs_soil_only + nmdc_biosample_only
ms_nb_disjoint_union.sort()
ms_nb_total_union = list(set(nmdc_biosample_ics_names).union(set(mixs_soil_ics_names)))
ms_nb_total_union.sort()

isd = SchemaDefinition(name=shared_schema_name, id=shared_schema_id)
ic = ClassDefinition(name=shared_class_name)

for i in ms_nb_total_union:
    # print(i)
    if i in mixs_soil_only:
        # slot_to_add = mixs_soil_ics_dict[i]
        isd.slots[i] = mixs_soil_ics_dict[i]
        ic.slots.append(i)
    elif i in nmdc_biosample_only:
        isd.slots[i] = nmdc_biosample_ics_dict[i]
        ic.slots.append(i)
    else:
        print(i)
        # want to compare and edit this as a dict
        from_mixs_slotdef = mixs_soil_ics_dict[i]
        from_mixs_yaml = yaml_dumper.dumps(from_mixs_slotdef)
        # print(from_mixs_yaml)
        from_mixs_yaml_dict = yaml.safe_load(from_mixs_yaml)
        # # print(from_mixs_yaml_dict)
        # # but how to get back into a SLotDefinition?
        # reloaded = yaml_loader.loads(from_mixs_yaml, SlotDefinition)
        # # print(reloaded)

        msd = yaml.safe_load(yaml_dumper.dumps(mixs_soil_ics_dict[i]))
        nbd = yaml.safe_load(yaml_dumper.dumps(nmdc_biosample_ics_dict[i]))

        uniondef = msd.copy()

        # diff = DeepDiff(msd, nbd)
        # pprint(diff)

        diff = DeepDiff(msd, nbd, view="tree")
        if 'values_changed' in diff:
            vc = diff['values_changed']
            # print("values_changed")
            for j in vc:
                current_path = j.path(output_format='list')
                # print(current_path)
                if current_path == ["owner"]:
                    # print("action: assert shared owner")
                    uniondef["owner"] = shared_schema_owner
                elif current_path == ['description']:
                    # print("action: combine conflicting descriptions")
                    desc_union = f"{source_names[0]}:{j.t1}|{source_names[1]}: {j.t2}"
                    uniondef["description"] = desc_union
                else:
                    print(f"unhandled values_changed in {current_path}")
        if 'type_changes' in diff:
            print("unhandled type_changes")
        #     vc = diff['type_changes']
        #     for j in vc:
        #         current_path = j.path(output_format='list')
        #         if current_path == ["required"]:
        #             # this is a dict change now
        #             if j.t1 or j.t2:
        #                 print("required true always wins")
        #                 uniondef["required"] = True
        #             else:
        #                 pass
        #         else:
        #             print(f"unhandled type_changes in {current_path}")

        # one of the iterable changes is irrelevant... which one? msd = 1, nbd = 2?
        # use msd as a base
        # ignore added?
        if 'iterable_item_added' in diff:
            print("unhandled iterable_item_added")
        #     # pass
        #     vc = diff['iterable_item_added']
        #     for j in vc:
        #         current_path = j.path(output_format='list')
        #         cp0 = current_path[0]
        #         if cp0 in uniondef:
        #             # this will always be the case since we're using an induced slot definition?
        #             uniondef[cp0].append(j.t2)
        #         else:
        #             print("unhandled empty list {cp0}")
        if 'iterable_item_removed' in diff:
            print("unhandled iterable_item_removed")
        if 'dictionary_item_added' in diff:
            # print("dictionary_item_added")
            vc = diff['dictionary_item_added']
            for j in vc:
                current_path = j.path(output_format='list')
                cp0 = current_path[0]
                val2 = j.t2
                # print(j.t1)
                if isinstance(val2, list):
                    if cp0 in uniondef:
                        pass
                        # print("already in there")
                    else:
                        uniondef[cp0] = []
                    for k in val2:
                        # print(f"one item to add: {cp0} {k}")
                        uniondef[cp0].append(k)
                    # pprint(uniondef)
                elif isinstance(val2, dict):
                    print("need dict handler")
                else:
                    # dangerous assumption ?
                    uniondef[cp0] = val2
        if 'dictionary_item_removed' in diff:
            pass
            # if this is a case where MIxS has a dict item but NMDC doesn't, not action required?
            # print("unhandled dictionary_item_removed")
        # could be other diff types?
        reloaded = yaml_loader.loads(uniondef, SlotDefinition)
        isd.slots[i] = reloaded
        ic.slots.append(i)

isd.classes[shared_class_name] = ic

# all_res = ['classes', 'enums', 'prefixes', 'subsets', 'types']
for i in all_res:
    print(i)
    source = merged_sv.schema
    dest = isd
    source_elements = source[i]
    sedn = list(source_elements.keys())
    dest_elements = dest[i]
    dedn = list(dest_elements.keys())
    to_move = list(set(sedn) - set(dedn))
    to_move.sort()
    print(to_move)
    for j in to_move:
        print(j)
        isd[i][j] = source_elements[j]

yaml_dumper.dump(isd, dump_dest)
