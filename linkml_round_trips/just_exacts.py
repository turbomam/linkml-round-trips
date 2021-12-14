from linkml_runtime.linkml_model import SchemaDefinition, Prefix


# todo sid and def_expansion should really be an uri or curie
def just_exacts_schema(sname: str, sid: str, def_pref: str, def_expansion: str) -> SchemaDefinition:
    p = Prefix(prefix_prefix=def_pref, prefix_reference=def_expansion)
    sd = SchemaDefinition(name=sname, id=sid)
    sd.prefixes[def_pref] = p
    sd.default_prefix = def_pref
    return sd
