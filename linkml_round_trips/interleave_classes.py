from linkml_runtime.linkml_model import SchemaDefinition, ClassDefinition
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.utils.schemaview import SchemaView

interleaved_name = "interleaved"
interleaved_id = "http://example.com/interleaved"
interleaved_class_name = "interleaved_class"
interleaved_filename = "interleaved.yaml"

model1 = "../../mixs-source/model/schema/mixs.yaml"
class1 = "soil"

model2 = "../../nmdc-schema/src/schema/nmdc.yaml"
class2 = "biosample"

sv1 = SchemaView(model1)
slots1 = sv1.class_induced_slots(class1)
slotnames1 = [i.name for i in slots1]
slots_dict_1 = dict(zip(slotnames1, slots1))
slotnames1.sort()

sv2 = SchemaView(model2)
slots2 = sv2.class_induced_slots(class2)
slotnames2 = [i.name for i in slots2]
slots_dict_2 = dict(zip(slotnames2, slots2))
slotnames2.sort()

slot_names_only_1 = list(set(slotnames1) - set(slotnames2))
slot_names_only_1.sort()

slot_names_only_2 = list(set(slotnames2) - set(slotnames1))
slot_names_only_2.sort()

slot_names_intersection = list(set(slotnames1).intersection(set(slotnames1)))
slot_names_intersection.sort()

interleaved_sd = SchemaDefinition(name=interleaved_name, id=interleaved_id)

interleaved_class = ClassDefinition(name=interleaved_class_name)

# for i in slot_names_only_1:
#     print(i)
# print("\n")

for i in slot_names_only_1:
    print(i)
    # print(slots_dict_1[i])
    interleaved_class.slots.append(i)
    interleaved_sd.slots[i] = slots_dict_1[i]
print("\n")

# for i in slot_names_only_2:
#     print(i)
# print("\n")

# print(slots_dict_2)

# x = list(slots_dict_2.keys())
# for i in x:
#     print(x[i])

for i in slot_names_only_2:
    print(i)
    interleaved_sd.slots[i] = slots_dict_2[i]
    # if " " in i:
    #     print("WHITESPACE")
    #     print(slots_dict_2[i])
    # else:
    #     # pass
    #     print(slots_dict_2[i])
    #     # interleaved_class.slots.append(i)
    #     # interleaved_sd.slots[i] = slots_dict_2[i]
print("\n")

# print(interleaved_sd.slots)
# print(interleaved_class.slots)

# ----

yaml_dumper.dump(interleaved_sd, interleaved_filename)
