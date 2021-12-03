from __future__ import print_function  # In case running on Python 2

from linkml_runtime.linkml_model import (
    SchemaDefinition,
    ClassDefinition,
    SlotDefinition,
    Annotation,
)
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.utils.schemaview import SchemaView
from strsimpy import Cosine

# from dataclasses import dataclass

from deepdiff import DeepDiff
from pprint import pprint


# # https://stackoverflow.com/a/53818532/3860847
# def recursive_compare(d1, d2, level='root'):
#     if isinstance(d1, dict) and isinstance(d2, dict):
#         if d1.keys() != d2.keys():
#             s1 = set(d1.keys())
#             s2 = set(d2.keys())
#             print('{:<20} + {} - {}'.format(level, s1 - s2, s2 - s1))
#             common_keys = s1 & s2
#         else:
#             common_keys = set(d1.keys())
#
#         for k in common_keys:
#             recursive_compare(d1[k], d2[k], level='{}.{}'.format(level, k))
#
#     elif isinstance(d1, list) and isinstance(d2, list):
#         if len(d1) != len(d2):
#             print('{:<20} len1={}; len2={}'.format(level, len(d1), len(d2)))
#         common_len = min(len(d1), len(d2))
#
#         for i in range(common_len):
#             recursive_compare(d1[i], d2[i], level='{}[{}]'.format(level, i))
#
#     else:
#         if d1 != d2:
#             print('{:<20} {} != {}'.format(level, d1, d2))


def compare_linkml_root_elem(elem_type, elem_name, elem1, elem2):
    if elem1 != elem2:
        print(f"NOT merging {elem_name}")
        diff = DeepDiff(elem1.__dict__, elem2.__dict__)
        pprint(diff)
        print("\n")


linkml1 = "target/mixs_soil.yaml"
linkml2 = "target/nmdc_biosample.yaml"

sv1 = SchemaView(linkml1)
# print(type(sv1))
sv2 = SchemaView(linkml2)
sd2 = sv2.schema

# print(type(sd2))

schema = sd2
dest = sv1.schema
all_res = ['classes', 'prefixes', 'slots', 'slots', 'types']
all_res.sort()
print(all_res)
# all_res = ["classes"]
for current_re in all_res:
    print(current_re.upper())
    for k, v in schema[current_re].items():
        if k not in dest[current_re]:
            dest[current_re][k] = v
        else:
            a = schema[current_re][k]
            b = dest[current_re][k]
            if a != b:
                # recursive_compare(a.__dict__, b.__dict__)
                compare_linkml_root_elem(current_re, k, a, b)

# # https://github.com/linkml/linkml-runtime/blob/d762126974e6a8752f7eae1c7a614150a7f346f8/linkml_runtime/utils/schemaview.py#L1173-L1194
# def merge_schema(sv: SchemaView, schema: SchemaDefinition) -> SchemaDefinition:
#     dest = sv.schema
#     print("PREFIXES")
#     for k, v in schema.prefixes.items():
#         if k not in dest.prefixes:
#             # print(f"merging prefix {k}")
#             dest.prefixes[k] = v
#         else:
#             a = schema.prefixes[k]
#             b = dest.prefixes[k]
#             if a != b:
#                 print(f"NOT merging {k}")
#                 diff = DeepDiff(a.__dict__, b.__dict__)
#                 pprint(diff)
#     print("CLASSES")
#     current_re = "classes"
#     for k, v in schema[current_re].items():
#         if k not in dest[current_re]:
#             # print(f"merging class {k}")
#             dest[current_re][k] = v
#         else:
#             a = schema[current_re][k]
#             b = dest[current_re][k]
#             if a != b:
#                 # print(f"NOT merging current_re {k}")
#                 # print(yaml_dumper.dumps(a))
#                 # print(yaml_dumper.dumps(b))
#                 # recursive_compare(a.__dict__, b.__dict__)
#                 compare_linkml_root_elem(k, a, b)
#     print("SLOTS")
#     for k, v in schema.slots.items():
#         if k not in dest.slots:
#             # print(f"merging slot {k}")
#             dest.slots[k] = v
#         else:
#             a = schema.slots[k]
#             b = dest.slots[k]
#             if a != b:
#                 print(f"NOT merging {k}")
#                 diff = DeepDiff(a.__dict__, b.__dict__)
#                 pprint(diff)
#     print("TYPES")
#     for k, v in schema.types.items():
#         if k not in dest.types:
#             # print(f"merging type {k}")
#             dest.types[k] = v
#         else:
#             a = schema.types[k]
#             b = dest.types[k]
#             if a != b:
#                 print(f"NOT merging {k}")
#                 diff = DeepDiff(a.__dict__, b.__dict__)
#                 pprint(diff)
#     print("ENUMS")
#     for k, v in schema.enums.items():
#         if k not in dest.types:
#             # print(f"merging enum {k}")
#             dest.enums[k] = v
#         else:
#             a = schema.enums[k]
#             b = dest.enums[k]
#             if a != b:
#                 print(f"NOT merging {k}")
#                 diff = DeepDiff(a.__dict__, b.__dict__)
#                 pprint(diff)
#     # sv.set_modified()
#     return dest
#
#
# merged = merge_schema(sv1, sd2)
#
# yaml_dumper.dump(merged, "target/merged.yaml")
